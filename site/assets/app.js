"use strict";
// Market pages: search, order, pages and a daily chart per item. The table is
// already in the HTML for readers without JavaScript; this replaces it with the
// full list from prices.json. Journal page: filter entries by kind.

const PAGE_SIZE = 50;
const SVG = "http://www.w3.org/2000/svg";

function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined && text !== null) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function svgEl(tag, attrs) {
  const node = document.createElementNS(SVG, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  return node;
}

function money(copper) {
  const span = el("span", null, "money");
  if (copper === null || copper === undefined) return span;
  const gold = Math.floor(copper / 10000), silver = Math.floor((copper % 10000) / 100), cop = copper % 100;
  const parts = [];
  if (gold) parts.push(el("span", `${gold.toLocaleString("en-GB")}g`, "g"));
  if (gold || silver) parts.push(el("span", `${silver}s`, "s"));
  parts.push(el("span", `${cop}c`, "c"));
  parts.forEach((part, i) => { if (i) span.append(" "); span.append(part); });
  return span;
}

function niceDate(iso) {
  if (!iso) return "not seen";
  const [y, m, d] = iso.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" });
}

function change(pct) {
  if (pct === null || pct === undefined) return null;
  const word = pct > 0 ? "up" : pct < 0 ? "down" : "flat";
  const text = pct >= 200 ? `×${Math.round((pct + 100) / 100)}` : `${pct > 0 ? "+" : ""}${pct}%`;
  return el("span", text, `change ${word}`);
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b), mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : Math.floor((sorted[mid - 1] + sorted[mid]) / 2);
}

function spark(values) {
  let points = values.map((v, i) => [i, v]).filter(([, v]) => v !== null);
  if (points.length < 2) return points.length ? el("span", "one day", "spark-none") : null;
  const ceiling = 4 * [...points.map(p => p[1])].sort((a, b) => a - b)[Math.floor(points.length / 2)];
  points = points.map(([i, v]) => [i, Math.min(v, ceiling)]);  // clip troll listings
  const low = Math.min(...points.map(p => p[1])), high = Math.max(...points.map(p => p[1]));
  const span = (high - low) || 1, width = 84, height = 22;
  const coords = points.map(([i, v]) => [+(i * width / (values.length - 1)).toFixed(1), +(height - 2 - (v - low) / span * (height - 4)).toFixed(1)]);
  const svg = svgEl("svg", { class: "spark", viewBox: `0 0 ${width} ${height}`, width, height, "aria-hidden": "true" });
  svg.append(svgEl("path", { d: coords.map(([x, y], n) => `${n ? "L" : "M"}${x},${y}`).join(" ") }));
  const [x, y] = coords[coords.length - 1];
  svg.append(svgEl("circle", { cx: x, cy: y, r: 2 }));
  return svg;
}

function detailChart(days) {
  // days: [[iso, low, high, listed], ...]
  const width = 640, height = 170, left = 8, right = 8, top = 22, bottom = 26;
  const ceiling = 4 * median(days.map(d => d[1]));  // listings far above the usual price would flatten the chart
  const clipped = days.filter(d => d[2] > ceiling).length;
  days = days.map(d => [d[0], Math.min(d[1], ceiling), Math.min(d[2], ceiling), d[3]]);
  const lows = days.map(d => d[1]), highs = days.map(d => d[2]);
  const min = Math.min(...lows), max = Math.max(...highs), span = (max - min) || 1;
  const x = i => left + (days.length === 1 ? (width - left - right) / 2 : i * (width - left - right) / (days.length - 1));
  const y = v => top + (1 - (v - min) / span) * (height - top - bottom);
  const svg = svgEl("svg", { class: "detail-chart", viewBox: `0 0 ${width} ${height}`, role: "img",
    "aria-label": `Daily lowest price from ${niceDate(days[0][0])} to ${niceDate(days[days.length - 1][0])}` });
  if (days.length > 1) {
    const band = days.map((d, i) => `${x(i)},${y(d[2])}`).concat(days.map((d, i) => `${x(i)},${y(d[1])}`).reverse());
    svg.append(svgEl("polygon", { class: "band", points: band.join(" ") }));
    svg.append(svgEl("polyline", { class: "line", points: days.map((d, i) => `${x(i)},${y(d[1])}`).join(" ") }));
  } else {
    svg.append(svgEl("circle", { cx: x(0), cy: y(lows[0]), r: 4, fill: "currentColor" }));
  }
  svg.append(svgEl("line", { class: "axis", x1: left, x2: width - right, y1: height - bottom + 4, y2: height - bottom + 4 }));
  const label = (text, attrs) => { const t = svgEl("text", attrs); t.textContent = text; svg.append(t); };
  label(niceDate(days[0][0]), { x: left, y: height - 6 });
  if (days.length > 1) label(niceDate(days[days.length - 1][0]), { x: width - right, y: height - 6, "text-anchor": "end" });
  const coin = c => { const g = Math.floor(c / 10000), s = Math.floor(c % 10000 / 100); return g ? `${g}g ${s}s` : s ? `${s}s ${c % 100}c` : `${c % 100}c`; };
  label(`high ${coin(max)}`, { x: width - right, y: 14, "text-anchor": "end" });
  label(`low ${coin(min)}`, { x: left, y: 14 });
  svg.dataset.clipped = clipped;
  return svg;
}

async function marketBrowser(section) {
  const config = JSON.parse(section.dataset.config);
  const tbody = document.getElementById("rows");
  const status = document.getElementById("status");
  const filter = document.getElementById("filter");
  const scope = document.getElementById("scope");
  const order = document.getElementById("order");
  const pager = document.getElementById("pager");
  let items = [], view = [], page = 0, history = null, open = null;

  try {
    const response = await fetch(config.prices);
    if (!response.ok) throw new Error();
    const data = await response.json();
    const cols = data.columns;
    items = data.rows.map(row => Object.fromEntries(cols.map((c, i) => [c, row[i]])));
  } catch {
    status.textContent = "Showing the list built into this page. Reload to search and sort every item.";
    return;
  }
  document.getElementById("partial-note")?.remove();  // the full list is loaded now
  const params = new URLSearchParams(location.search);
  filter.value = params.get("q") || "";
  if (filter.value) {
    scope.value = "all";
    section.scrollIntoView();  // a search from the home page lands on the results, not the highlights
  }

  function matches(item, terms, id) {
    if (id !== null) return item.id === id;
    const name = item.name.toLowerCase();
    return terms.every(term => name.includes(term));
  }

  function update(resetPage = true) {
    const raw = filter.value.trim();
    const link = raw.match(/item[=/](\d+)/i);
    const id = link ? Number(link[1]) : /^\d+$/.test(raw) ? Number(raw) : null;
    const terms = raw.toLowerCase().split(/\s+/).filter(Boolean);
    view = items.filter(item => (scope.value === "all" || item.current) && matches(item, terms, id));
    const sorters = {
      name: (a, b) => a.name.localeCompare(b.name, "en-GB"),
      listed: (a, b) => (b.listed ?? -1) - (a.listed ?? -1),
      "price-high": (a, b) => b.typical - a.typical,
      "price-low": (a, b) => a.typical - b.typical,
      change: (a, b) => Math.abs(b.change ?? 0) - Math.abs(a.change ?? 0),
    };
    if (terms.length && id === null && order.value === "name") {
      // With a search, the item you most likely mean comes first: "linen" puts Linen Cloth above Barbaric Linen Vest.
      const query = terms.join(" ");
      const rank = item => {
        const name = item.name.toLowerCase();
        return name === query ? 0 : name.startsWith(query) ? 1 : (` ${name}`).includes(` ${query}`) ? 2 : 3;
      };
      view.sort((a, b) => rank(a) - rank(b) || (b.listed ?? 0) - (a.listed ?? 0) || sorters.name(a, b));
    } else {
      view.sort(sorters[order.value]);
    }
    if (resetPage) page = 0;
    const query = raw ? `?q=${encodeURIComponent(raw)}` : "";
    history_replace(query);
    render();
  }

  function history_replace(query) {
    try { window.history.replaceState(null, "", location.pathname + query + location.hash); } catch { /* file:// previews */ }
  }

  function render() {
    tbody.replaceChildren();
    open = null;
    const start = page * PAGE_SIZE;
    for (const item of view.slice(start, start + PAGE_SIZE)) {
      const row = el("tr");
      row.dataset.key = item.key;
      row.tabIndex = 0;  // keyboard: Tab to a row, Enter or Space opens its daily prices
      row.setAttribute("aria-expanded", "false");
      const name = el("th");
      name.scope = "row";
      const link = el("a", item.name);
      link.href = `https://foreverdb.net/item/${item.id}`;
      link.dataset.foreverdb = `item:${item.id}`;
      link.target = "_blank";
      link.rel = "noopener";
      name.append(link, " ", el("span", item.id, "id"));
      const typical = el("td", null, "num"); typical.append(money(item.typical));
      const latest = el("td", null, "num latest"); latest.append(money(item.price));
      const seen = el("td", niceDate(item.last_seen), "date");
      const listed = el("td", item.listed === null ? "" : item.listed.toLocaleString("en-GB"), "num listed");
      const trend = el("td", null, "trend");
      const line = spark(item.spark), pct = change(item.change);
      if (line) trend.append(line, " ");
      if (pct) trend.append(pct);
      row.append(name, typical, latest, seen, listed, trend);
      tbody.append(row);
    }
    const pages = Math.max(1, Math.ceil(view.length / PAGE_SIZE));
    const shown = view.length ? `${start + 1}–${Math.min(start + PAGE_SIZE, view.length)} of ` : "";
    status.textContent = view.length
      ? `${shown}${view.length.toLocaleString("en-GB")} item${view.length === 1 ? "" : "s"}. Select a row for its daily prices.`
      : (scope.value === "current" ? "Nothing seen in the last two weeks matches. Try “Every item ever seen”." : "No item matches. Try part of the name, or the item ID.");
    pager.hidden = pages < 2;
    pager.replaceChildren();
    if (pages > 1) {
      const prev = el("button", "Previous"), next = el("button", "Next");
      prev.type = next.type = "button";
      prev.disabled = page === 0;
      next.disabled = page >= pages - 1;
      prev.addEventListener("click", () => { page--; render(); section.scrollIntoView(); });
      next.addEventListener("click", () => { page++; render(); section.scrollIntoView(); });
      pager.append(el("span", `Page ${page + 1} of ${pages}`), prev, next);
    }
  }

  function closeDetail() {
    if (!open) return null;
    open.previousElementSibling.classList.remove("open");
    open.previousElementSibling.setAttribute("aria-expanded", "false");
    open.remove();
    const key = open.dataset.for;
    open = null;
    return key;
  }

  async function toggle(row) {
    if (closeDetail() === row.dataset.key) return;  // selecting the open row closes it
    const detail = el("tr", null, "detail");
    detail.dataset.for = row.dataset.key;
    const cell = el("td");
    cell.colSpan = 6;
    cell.append(el("p", "Loading daily prices…", "detail-note"));
    detail.append(cell);
    row.after(detail);
    row.classList.add("open");
    row.setAttribute("aria-expanded", "true");
    open = detail;
    try {
      if (!history) {
        const response = await fetch(config.history);
        if (!response.ok) throw new Error();
        history = (await response.json()).history;
      }
      const days = history[row.dataset.key] || [];
      cell.replaceChildren();
      if (!days.length) { cell.append(el("p", "No daily records for this item.", "detail-note")); return; }
      const busiest = days.reduce((a, b) => ((b[3] ?? 0) > (a[3] ?? 0) ? b : a));
      const chart = detailChart(days), clipped = Number(chart.dataset.clipped);
      cell.append(chart, el("p",
        `${days.length} day${days.length === 1 ? "" : "s"} of records. The line is each day's cheapest listing; the band shows how far that day's cheapest listing rose.` +
        (busiest[3] ? ` Most listed: ${busiest[3].toLocaleString("en-GB")} on ${niceDate(busiest[0])}.` : "") +
        (clipped ? ` ${clipped} day${clipped === 1 ? "" : "s"} with listings far above the usual price are cut off at the top.` : ""), "detail-note"));
    } catch {
      cell.replaceChildren(el("p", "The daily history didn't load. Check your connection and select the row again.", "detail-note"));
    }
  }

  tbody.addEventListener("keydown", event => {
    const row = event.target.closest("tr[data-key]");
    if (row && event.target === row && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      toggle(row);
    }
  });
  tbody.addEventListener("click", event => {
    if (event.target.closest("a")) return;
    const row = event.target.closest("tr[data-key]");
    if (row) toggle(row);
  });
  let timer;
  filter.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(update, 120); });
  section.querySelector("form").addEventListener("submit", event => { event.preventDefault(); update(); });
  scope.addEventListener("change", () => update());
  order.addEventListener("change", () => update());
  update();
}

function journalFilter(group) {
  const entries = [...document.querySelectorAll(".entries .entry")];
  const buttons = [...group.querySelectorAll("button")];
  const choose = kind => {
    buttons.forEach(b => b.setAttribute("aria-pressed", String(b.dataset.filter === kind)));
    entries.forEach(e => { e.hidden = kind !== "all" && e.dataset.type !== kind; });
  };
  buttons.forEach(b => b.addEventListener("click", () => choose(b.dataset.filter)));
  choose("all");
}

const browserSection = document.getElementById("prices");
if (browserSection) marketBrowser(browserSection);
const kindGroup = document.querySelector(".kind-filter");
if (kindGroup) journalFilter(kindGroup);
