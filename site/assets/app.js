"use strict";
const PAGE_SIZE = 10;
const browser = document.querySelector("#market-browser");
if (browser) {
  const config = JSON.parse(browser.dataset.config);
  const input = document.querySelector("#item-search");
  const selection = document.querySelector("#partition-select");
  const counter = document.querySelector("#search-count");
  const tableBody = document.querySelector("#market-table tbody");
  const previous = document.querySelector("#previous-page");
  const next = document.querySelector("#next-page");
  const cache = new Map();
  let records = [];
  let page = 0;
  let request = 0;
  let partIndex = 0;
  let globalMode = false;
  let isLookup = false;
  const dateSelect = document.querySelector("#capture-select");
  const sortSelect = document.querySelector("#sort-select");
  const dataset = () => dateSelect.value === "latest" ? config : config.snapshots.find(s=>s.source_sha256.startsWith(dateSelect.value));
  const element = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  const price = copper => {
    if (!Number.isSafeInteger(copper) || copper < 0) throw new Error("Unsupported price value.");
    return `${Math.floor(copper/10000).toLocaleString("en-GB")}g ${Math.floor(copper%10000/100)}s ${copper%100}c`;
  };
  async function read(url, expectedRevision = config.revision) {
    if (!cache.has(url)) {
      const response = await fetch(url);
      if (!response.ok) throw new Error("Could not load this data partition.");
      const data = await response.json();
      if (data.revision !== expectedRevision) throw new Error("New records have been published. Reload this page to continue.");
      cache.set(url, data);
    }
    return cache.get(url);
  }
  function render() {
    tableBody.replaceChildren();
    const start = page*PAGE_SIZE;
    for (const record of records.slice(start,start+PAGE_SIZE)) {
      const row = element("tr");
      const first = element("td");
      const link = element("a",`Item ${record.item_key}`);
      const itemId=record.item_key.split(":")[0];
      link.href = `https://foreverdb.net/item/${itemId}`;
      link.dataset.foreverdb = `item:${itemId}`;
      link.target = "_blank"; link.rel = "noopener";
      first.append(link);
      row.append(first,element("td",price(record.unit_price_copper),"price"),element("td",config.capture_sources[record.source].capture_date));
      const state = element("td"); state.append(element("span","Cached quote","status"));
      const last = element("td");
      const detail = element("a","History ↗");
      detail.href=`${config.market_html}?item=${encodeURIComponent(record.item_key)}#item-detail`;
      detail.dataset.itemKey=record.item_key;
      last.append(detail); row.append(state,last); tableBody.append(row);
    }
    previous.disabled = isLookup || (page === 0 && (globalMode || partIndex === 0));
    next.disabled = isLookup || ((page+1)*PAGE_SIZE >= records.length && (globalMode || partIndex === dataset().partitions.length-1));
    const offset = globalMode || isLookup ? 0 : dataset().partitions.slice(0,partIndex).reduce((n,p)=>n+p.records,0);
    const total = isLookup ? records.length : (dataset().item_count ?? dataset().rows);
    counter.textContent = records.length ? `Showing ${offset+start+1}–${offset+Math.min(start+PAGE_SIZE,records.length)} of ${total.toLocaleString("en-GB")} items.` : "No record for that exact item key.";
  }
  async function show(part,key,lastPage=false) {
    const token = ++request;
    try {
      counter.textContent = "Loading a small data partition…";
      const data = await read(part.json,dataset().revision);
      if (token !== request) return;
      records = key ? data.records.filter(r=>r.item_key===key) : data.records;
      globalMode=false; isLookup=!!key;
      partIndex=dataset().partitions.findIndex(p=>p.id===part.id);
      page=lastPage ? Math.floor((records.length-1)/PAGE_SIZE) : 0;
      selection.value=part.id; render();
      document.querySelector("#item-detail").hidden = true;
      if (key && records.length) await historyFor(part,key,token);
    } catch (error) { if(token===request) counter.textContent=error.message; }
  }
  async function historyFor(part,key,token) {
    const itemId=Number(key.split(":")[0]);
    const historyPart=config.partitions.find(p=>itemId>=p.first_item_id && itemId<=p.last_item_id);
    const data=await read(historyPart.history_json);
    if (token!==request) return;
    const body=document.querySelector("#history-rows"); body.replaceChildren();
    for (const record of [...data.history[key]].reverse()) {
      const source=data.capture_sources[record.source];
      const row=element("tr");
      row.append(element("td",source.capture_date),element("td",price(record.unit_price_copper),"price"),element("td",record.latest_daily_source_code ?? "Unknown"),element("td",record.source));
      body.append(row);
    }
    document.querySelector("#detail-title").textContent=`Item ${key} · capture history`;
    document.querySelector("#detail-download").href=historyPart.history_json;
    document.querySelector("#item-detail").hidden=false;
  }
  function lookup(key) {
    const linked=key.match(/(?:foreverdb\.net\/item\/|wowhead\.com\/[^\s]*?item(?:=|%3d)|classicdb\.ch\/\?item=)(\d+)/i);
    if(linked) key=linked[1];
    if(!key){show(dataset().partitions[0]);return;}
    if (!/^\d+(?::[\d:-]+)?$/.test(key)) { counter.textContent="Enter an exact numeric item key, for example 2589."; return; }
    const id=Number(key.split(":")[0]);
    const part=dataset().partitions.find(p=>id>=p.first_item_id && id<=p.last_item_id);
    if (!part) { counter.textContent="No record for that item in this market."; return; }
    input.value=key;
    window.history.replaceState(null,"",`${config.market_html}?item=${encodeURIComponent(key)}#item-detail`);
    show(part,key);
  }
  document.querySelector("#item-form").addEventListener("submit",event=>{event.preventDefault();lookup(input.value.trim());});
  input.addEventListener("input",()=>{if(!input.value){sortSelect.value="item";show(dataset().partitions[0]);}});
  dateSelect.addEventListener("change",()=>{input.value="";sortSelect.value="item";show(dataset().partitions[0]);});
  sortSelect.addEventListener("change",async()=>{
    input.value="";
    if(sortSelect.value==="item"){show(dataset().partitions[0]);return;}
    const token=++request;
    try{
      counter.textContent="Loading the complete quote set for this sort…";
      const data=await read(dataset().quotes_json || config.latest_json,dataset().revision);
      if(token!==request)return;
      records=[...data.records].sort((a,b)=>sortSelect.value==="price-low" ? a.unit_price_copper-b.unit_price_copper : b.unit_price_copper-a.unit_price_copper);
      page=0;globalMode=true;isLookup=false;render();
    }catch(error){if(token===request)counter.textContent=error.message;}
  });
  previous.addEventListener("click",()=>{if(page>0){page--;render();}else if(!globalMode && partIndex>0){show(dataset().partitions[partIndex-1],null,true);}});
  next.addEventListener("click",()=>{if((page+1)*PAGE_SIZE<records.length){page++;render();}else if(!globalMode && partIndex+1<dataset().partitions.length){show(dataset().partitions[partIndex+1]);}});
  tableBody.addEventListener("click",event=>{const link=event.target.closest("a[data-item-key]");if(link){event.preventDefault();lookup(link.dataset.itemKey);}});
  const initial=new URLSearchParams(location.search).get("item");
  if (initial) lookup(initial); else show(config.partitions[0]);
}
