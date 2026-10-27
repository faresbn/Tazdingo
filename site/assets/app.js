"use strict";
// Every page: the theme toggle and the launch countdown. Front page: search across the
// ledger. Market pages: search, order, pages and a daily chart per item. The pages work
// without JavaScript; this adds speed and detail.

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

const STEADINESS = { steady: "Steady", moving: "Moving", volatile: "Volatile" };

function steadiness(value) {
  const span = el("span", value ? STEADINESS[value] : "Too new", `badge ${value || "unknown"}`);
  if (!value) span.title = "Fewer than three days of prices";
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
  const hasOption = (select, value) => [...select.options].some(option => option.value === value);
  const savedScope = params.get("scope"), savedOrder = params.get("order");
  scope.value = hasOption(scope, savedScope) ? savedScope : filter.value ? "all" : "current";
  order.value = hasOption(order, savedOrder) ? savedOrder : "name";
  if (filter.value) {
    section.scrollIntoView();  // a search from the home page lands on the results, not the highlights
  }
  const reset = section.querySelector("[data-reset-filters]");
  if (reset) reset.hidden = false;

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
      steadiest: (a, b) => (["steady", "moving", "volatile"].indexOf(a.volatility) + 1 || 9) - (["steady", "moving", "volatile"].indexOf(b.volatility) + 1 || 9),
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
    const query = new URLSearchParams();
    if (raw) query.set("q", raw);
    if (raw || scope.value !== "current") query.set("scope", scope.value);
    if (order.value !== "name") query.set("order", order.value);
    history_replace(query.size ? `?${query}` : "");
    if (reset) reset.disabled = !raw && scope.value === "current" && order.value === "name";
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
      link.dataset.foreverdb = `item:${item.id}`;
      if (item.url) {
        link.href = item.url;  // the item's own page: every scan price, chart and patterns
      } else {
        link.href = `https://foreverdb.net/item/${item.id}`;
        link.target = "_blank";
        link.rel = "noopener";
      }
      name.append(link, " ", el("span", item.id, "id"));
      const typical = el("td", null, "num"); typical.append(money(item.typical));
      const steady = el("td", null, "vol"); steady.append(steadiness(item.volatility));
      const latest = el("td", null, "num latest"); latest.append(money(item.price));
      const seen = el("td", niceDate(item.last_seen), "date");
      const listed = el("td", item.listed === null ? "" : item.listed.toLocaleString("en-GB"), "num listed");
      const trend = el("td", null, "trend");
      const line = spark(item.spark), pct = change(item.change);
      if (line) trend.append(line, " ");
      if (pct) trend.append(pct);
      row.append(name, typical, steady, latest, seen, listed, trend);
      tbody.append(row);
    }
    const pages = Math.max(1, Math.ceil(view.length / PAGE_SIZE));
    const shown = view.length ? `${start + 1}–${Math.min(start + PAGE_SIZE, view.length)} of ` : "";
    status.textContent = view.length
      ? `${shown}${view.length.toLocaleString("en-GB")} item${view.length === 1 ? "" : "s"}. Select a row for its daily prices.`
      : (scope.value === "current" ? "No recent items match. Choose “All recorded items” or reset the filters." : "No item matches. Try part of the name, or reset the filters.");
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
    cell.colSpan = 7;
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
      const id = row.dataset.key.replace(/^gr:/, "").split(":")[0];
      const compare = el("p", null, "detail-note");
      const link = el("a", "Compare with other players' scans on ForeverDB");
      link.href = `https://foreverdb.net/item/${id}`; link.target = "_blank"; link.rel = "noopener";
      compare.append(link);
      cell.append(compare);
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
  section.querySelector("form").addEventListener("reset", event => {
    event.preventDefault(); clearTimeout(timer);
    filter.value = ""; scope.value = "current"; order.value = "name";
    update(); filter.focus();
  });
  scope.addEventListener("change", () => update());
  order.addEventListener("change", () => update());
  update();
}


function themeToggle(button) {
  const order = ["auto", "light", "dark"], labels = { auto: "Auto", light: "Light", dark: "Dark" };
  const describe = { auto: "follows your device", light: "light", dark: "dark" };
  let theme = "auto";
  try { theme = localStorage.getItem("theme") || "auto"; } catch { /* private mode: stay on auto */ }
  const apply = () => {
    if (theme === "auto") delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = theme;
    button.querySelector(".theme-label").textContent = labels[theme];
    button.setAttribute("aria-label", `Colour theme: ${describe[theme]}. Select to change.`);
  };
  button.addEventListener("click", () => {
    theme = order[(order.indexOf(theme) + 1) % order.length];
    try { theme === "auto" ? localStorage.removeItem("theme") : localStorage.setItem("theme", theme); } catch { /* not remembered */ }
    apply();
  });
  apply();
}

function countdown(node) {
  // The build writes the count as of its own run; this counts to the moment servers open from
  // the visitor's clock, with the same rule as countdown_text in scripts/pages.py.
  const opens = Date.parse(document.body.dataset.launch);
  if (Number.isNaN(opens)) return;
  const plural = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`;
  function tick() {
    const seconds = (opens - Date.now()) / 1000;
    const days = Math.floor(seconds / 86400), hours = Math.floor(seconds / 3600);
    node.textContent = seconds <= 0 ? `Day ${Math.floor(-seconds / 86400) + 1} of Forever`
      : days ? `Forever opens in ${plural(days, "day")}`
      : hours ? `Forever opens in ${plural(hours, "hour")}` : "Forever opens within the hour";
  }
  tick();
  setInterval(tick, 60000);
}

function localTimes() {
  // Scan times are written in UTC; show them in the visitor's own time as well.
  const format = new Intl.DateTimeFormat(undefined, { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
  document.querySelectorAll("time[data-local-time]").forEach(node => {
    const moment = new Date(node.getAttribute("datetime"));
    if (!Number.isNaN(moment.getTime())) node.title = `${format.format(moment)} your time`;
  });
  const offset = -new Date().getTimezoneOffset() / 60;
  const label = offset === 0 ? "; your time is UTC" : `; your time is UTC${offset > 0 ? "+" : "−"}${Math.abs(offset)}`;
  document.querySelectorAll("[data-utc-offset]").forEach(node => { node.textContent = label; });
}

function siteSearch(form) {
  const input = form.querySelector("input"), list = document.getElementById("lookup-results");
  const status = document.getElementById("lookup-status");
  let entries = null, pending = null, matches = [], request = 0;
  async function load() {
    if (entries) return entries;
    if (!pending) pending = fetch(`${document.body.dataset.base}search.json`).then(response => {
      if (!response.ok) throw new Error();
      return response.json();
    }).then(data => { entries = data; return data; }).catch(() => null).finally(() => { pending = null; });
    return pending;
  }
  function close() { request++; list.hidden = true; }
  async function show() {
    const turn = ++request;
    const query = input.value.trim().toLowerCase();
    if (query.length < 2) { close(); matches = []; status.textContent = ""; return false; }
    const all = await load();
    if (turn !== request || query !== input.value.trim().toLowerCase() || !form.contains(document.activeElement)) return false;
    if (!all) { close(); return null; }
    list.replaceChildren();
    const rank = ([title, , kind]) => {
      const t = title.toLowerCase();
      const base = t === query ? 0 : t.startsWith(query) ? 1 : (` ${t}`).includes(` ${query}`) ? 2 : t.includes(query) ? 3 : 9;
      return base * 2 + (kind === "Item" ? 1 : 0);  // pages before items at the same closeness
    };
    matches = all.map(e => [rank(e), e]).filter(([r]) => r < 18).sort((a, b) => a[0] - b[0] || a[1][0].localeCompare(b[1][0])).slice(0, 8).map(([, e]) => e);
    for (const [title, url, kind] of matches) {
      const li = el("li"), a = el("a", title);
      a.href = url;
      li.append(a, el("span", kind, "kind"));
      list.append(li);
    }
    if (!matches.length) list.append(el("li", "No matches. Try part of a class, profession or item name.", "search-empty"));
    list.hidden = false;
    status.textContent = matches.length ? `${matches.length} suggestions. Use the down arrow to browse.` : "No matching suggestions.";
    return true;
  }
  input.addEventListener("focus", () => { if (input.value.trim().length >= 2) show(); else load(); });
  input.addEventListener("input", show);
  input.addEventListener("keydown", async event => {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      if (list.hidden) await show();
      list.querySelector("a")?.focus();
    }
  });
  list.addEventListener("keydown", event => {
    const links = [...list.querySelectorAll("a")], index = links.indexOf(document.activeElement);
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      const next = index + (event.key === "ArrowDown" ? 1 : -1);
      if (next < 0 || next >= links.length) input.focus(); else links[next].focus();
    }
  });
  form.addEventListener("keydown", event => {
    if (event.key === "Escape" && !list.hidden) { event.preventDefault(); event.stopPropagation(); input.focus(); close(); }
  });
  form.addEventListener("focusout", () => window.setTimeout(() => { if (!form.contains(document.activeElement)) close(); }, 0));
  document.addEventListener("click", event => { if (!form.contains(event.target)) close(); });
  form.addEventListener("submit", async event => {
    if (input.value.trim().length < 2) return;
    event.preventDefault();
    const shown = await show();
    if (shown === null) { form.submit(); return; }  // preserve item-price search if the index is unavailable
    if (!shown) return;
    if (matches.length && matches[0][0].toLowerCase() === input.value.trim().toLowerCase()) {
      location.href = matches[0][1];
    } else list.querySelector("a")?.focus();
  });
}

function readingTools() {
  const narrow = window.matchMedia("(max-width: 860px)");
  const panels = [...document.querySelectorAll(".reading-tools")];
  const apply = () => panels.forEach(panel => { panel.open = !narrow.matches; });
  apply(); narrow.addEventListener("change", apply);
}

function menus() {
  // One state for every way in: each menu opens by its button (click, tap, Enter or Space) and, with
  // a mouse on a wide screen, by hovering. Leaving closes it after a short delay, so the pointer can
  // cross the gap to the panel. Escape or a click elsewhere closes it, and the phone menu too.
  const header = document.querySelector(".masthead");
  const items = [...document.querySelectorAll("[data-menu]")];
  const hover = window.matchMedia("(min-width: 861px) and (hover: hover)");
  const toggleOf = item => item.querySelector(".menu-toggle");
  const set = (item, open) => { item.classList.toggle("open", open); toggleOf(item).setAttribute("aria-expanded", String(open)); };
  const closeAll = except => items.forEach(item => { if (item !== except) set(item, false); });
  const opener = document.querySelector(".nav-open");
  const showNav = shown => {
    if (!opener) return;
    header.classList.toggle("nav-shown", shown);
    opener.setAttribute("aria-expanded", String(shown));
    opener.textContent = shown ? "Close" : "Menu";
  };
  let timer;
  const hoverOpened = new WeakSet();
  items.forEach(item => {
    toggleOf(item).addEventListener("click", event => {
      clearTimeout(timer);
      const keepHovered = event.detail > 0 && hoverOpened.has(item);
      const open = keepHovered || !item.classList.contains("open");
      hoverOpened.delete(item);
      closeAll(item); set(item, open);
    });
    item.addEventListener("mouseenter", () => { if (!hover.matches) return; clearTimeout(timer); if (!item.classList.contains("open")) hoverOpened.add(item); closeAll(item); set(item, true); });
    item.addEventListener("mouseleave", () => {
      hoverOpened.delete(item);
      if (!hover.matches || item.contains(document.activeElement)) return;  // keep a keyboard user's menu open
      clearTimeout(timer);
      timer = setTimeout(() => set(item, false), 250);
    });
    item.addEventListener("focusout", () => window.setTimeout(() => {
      if (!item.contains(document.activeElement) && (!hover.matches || !item.matches(":hover"))) set(item, false);
    }, 0));
  });
  document.addEventListener("keydown", event => {
    if (event.key !== "Escape") return;
    const active = items.find(item => item.classList.contains("open"));
    if (active) { set(active, false); toggleOf(active).focus(); return; }
    if (header.classList.contains("nav-shown")) { showNav(false); opener.focus(); }
  });
  document.addEventListener("click", event => {
    if (event.target.closest(".masthead")) return;
    closeAll();
    showNav(false);
  });
  if (opener) opener.addEventListener("click", () => showNav(!header.classList.contains("nav-shown")));
}

menus();
readingTools();
document.querySelectorAll("[data-theme-toggle]").forEach(themeToggle);
document.querySelectorAll("[data-countdown]").forEach(countdown);
localTimes();
const lookupForm = document.querySelector("form.lookup");
if (lookupForm) siteSearch(lookupForm);
const browserSection = document.getElementById("prices");
if (browserSection) marketBrowser(browserSection);

// Both news views share the same verified feed. All remote strings become text nodes.
function newsReader(widget) {
  const button = widget.querySelector('[data-news-refresh]');
  const status = widget.querySelector('[data-news-status]');
  const holder = widget.querySelector('[data-news-list]');
  const limit = Number(widget.dataset.newsLimit) || 5;
  let running = false, newest = Date.parse(widget.dataset.newsVerifiedAt) || 0;
  const stamp = iso => {
    const d = new Date(iso);
    return Number.isFinite(d.getTime()) ? d.toLocaleString('en-GB', {timeZone:'UTC',day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'})+' UTC' : 'not yet verified';
  };
  const valid = p => {
    try {
      const u = new URL(p.url);
      return p.classifier_version === 1 && ['forever','mixed'].includes(p.kind)
        && u.protocol === 'https:' && u.hostname === 'us.forums.blizzard.com'
        && u.pathname.startsWith('/en/wow/t/') && !u.username && !u.password
        && typeof p.title === 'string' && Number.isFinite(Date.parse(p.posted));
    } catch { return false; }
  };
  async function refresh(manual) {
    if (running) return;
    running = true; button.disabled = true;
    button.textContent = 'Checking…'; button.setAttribute('aria-busy', 'true');
    if (manual) status.textContent = 'Checking Blizzard articles…';
    try {
      const response = await fetch(widget.dataset.newsEndpoint, {cache:'no-store',credentials:'omit',signal:AbortSignal.timeout(90000)});
      if (response.status === 429) throw new Error('Please wait a minute before checking again. Saved news is still shown.');
      if (!response.ok) throw new Error('Refresh unavailable. Showing the last verified news.');
      const data = await response.json();
      if (data.classifier_version !== 1 || !Array.isArray(data.posts)) throw new Error('The news response could not be verified. Saved news is still shown.');
      if (data.status === 'unavailable') throw new Error('Blizzard could not be checked. Showing the last verified news.');
      const verified = Date.parse(data.last_successful_refresh || data.fetched);
      if (!Number.isFinite(verified) || verified < newest) throw new Error('Keeping the more recent verified news already shown.');
      newest = verified;
      const records = data.posts.filter(valid).filter(p=>widget.dataset.newsScope !== 'forever' || p.kind === 'forever').slice(0,limit);
      const list = el('ol',null,'blue-list');
      for (const post of records) {
        const row=el('li'); const link=el('a',post.title,'blue-title');
        link.href=post.url; link.target='_blank'; link.rel='noopener'; row.append(link);
        if (post.kind === 'mixed') row.append(el('span','Mixed roundup','badge mixed'));
        if (widget.dataset.newsExcerpts === 'true' && post.section) row.append(el('span',post.section,'blue-meta'));
        row.append(el('span',`${post.author || 'Blizzard'} · ${stamp(post.posted)}${post.reply ? ' · reply' : ''}`,'blue-meta'));
        if (widget.dataset.newsExcerpts === 'true' && post.excerpt) row.append(el('p',post.excerpt,'blue-excerpt'));
        list.append(row);
      }
      holder.replaceChildren(records.length ? list : el('p','No verified Forever news available yet.','empty'));
      status.textContent = `Last verified check: ${stamp(data.last_successful_refresh || data.fetched)}${data.cached ? ' · shared five-minute cache' : ''}${data.status === 'partial' ? ' · some articles could not be verified' : ''}.`;
    } catch (error) { if (manual) status.textContent = error.message; }
    finally { running=false; button.disabled=false; button.textContent='Refresh news'; button.removeAttribute('aria-busy'); }
  }
  button.addEventListener('click',()=>refresh(true));
  refresh(false);
  window.setInterval(()=>{if(document.visibilityState==='visible')refresh(false);},300000);
}
document.querySelectorAll('[data-news-widget]').forEach(newsReader);
