# Auction House tools: what they measure and how, for Tazdingo's design

Research note, 27 October 2026. Web sources only. "Inferred" marks anything not directly published by the source. "Our data" means: per-upload `m` (minimum buyout at that scan, with the upload timestamp), per-day `l`/`h` (lowest and highest *minimum* buyout Auctionator saw that day), per-day `a` (the *highest* quantity available Auctionator saw that day), one realm and faction, no individual auctions, no sales, 3–4 uploads a day after launch.

## The 10 most useful ideas for our data, ranked

1. **A "usual price" from daily lows, aux-style.** aux condenses each day to that day's minimum buyout and takes the median of the last 11 daily values as market value. That is almost exactly our `l` series. A median of daily lows over 7–14 days (or an exponential moving average, as goldcap.gg uses) gives a baseline that a single troll listing can't move. Everything else below rests on this. Feasible today. ([aux](https://www.warcrafttavern.com/wow-classic/addons/aux/), [goldcap deals](https://goldcap.gg/deals))
2. **Deal flag = current price at or below a share of the usual price, with guards.** Tools agree on the shape: aux's `percent/60` filter (≤60% of value), goldcap's ≥30% discount, Hammerprice's adjustable 50–90%. They also agree on the guards: a minimum history depth, a *cap* on discount so one mispriced unit can't fake a huge deal, and a minimum quantity. Add a robust test: a modified z-score from the median absolute deviation (MAD), flagging ≤ −3.5. Feasible. Because the site is static and updates hours after a scan, frame these as "seen cheap at 14:05" rather than "buy now."
3. **Confidence tiers and "not enough data yet" gates.** goldcap tags each deal High, Medium or Low by history depth and liquidity, and hides Low by default. ForeverDB and The Undermine Journal hide sections until there's enough history: TUJ needs more than 8 entries for a median and at least 14 for a heat map. This is the honesty convention most worth copying. Feasible.
4. **Event studies: grouped, indexed price charts.** Saddlebag's Price Group Deltas plots each week's median minimum price as a percentage change from the start of the chart, and averages that across a group (ores, herbs, flasks). It exists to show what rose around a patch or raid release. auctionhouse.fyi's market index (top 50 items, value-weighted, 100 = start of range) does the same for the whole market. Feasible. This is the right tool for "what happens to flasks when a raid opens."
5. **Movers and market-state bands.** Saddlebag colours items by their change against a historic price: Spiking above +60%, Increasing +15 to +60%, Stable ±15%, Decreasing −15 to −60%, Crashing below −60%. goldcap's movers compare now with two days earlier; auctionhouse.fyi lists "new 7-day lows." Feasible.
6. **A daily low/high band chart, plus open/close, à la TUJ.** TUJ's daily chart is a candlestick (open, high, low, close) of hourly prices with a quantity range. Ours can draw the `l`–`h` band per day, open and close from the first and last upload's `m`, per-upload `m` as dots, and `a` as bars beneath. Feasible.
7. **Weekday and time-of-day profiles, normalised per item, pooled across items.** TUJ and Undermine Exchange draw weekday × hour heat maps (mean price per cell). AHPriceTracker and ProfitProphet do the same from personal scans. For us: divide each observation by that item's rolling median, then pool across many items. Partly feasible. It needs about 4+ weeks, and time-of-day is confounded by when the owner scans.
8. **Buy zone, sell zone and a flip estimate.** goldcap's flips mark the bottom quarter of the week's price range as the "buy zone" and the top quarter as "at the top." ProfitProphet gives buy/hold/sell signals from where the price sits in its observed range. Our flip estimate: expected resale (e.g. the 75th percentile of daily lows) × 0.95 (the AH cut), minus the deposit, minus the buy price, with volatility as risk. Feasible, but it carries no sell-through evidence, so label it "price spread, not proven demand."
9. **Supply signals from `a`.** Saddlebag's "Quantity Percent Remaining" is current quantity over average quantity, where low values hint at a shortage. Its shortage predictor pairs price at least 120% of average with quantity at most 50% of average. auctionhouse.fyi's "most active" ranks the biggest 3-day change in quantity listed. We can do these day over day with `a`. Feasible, but a weak proxy (see Q2).
10. **A per-item volatility marker and a suggested "good buy" price.** TUJ flags an item as volatile when standard deviation ÷ mean > 0.33, and suggests a price-alert threshold of mean − ½ × standard deviation. It shows that suggestion only with more than 8 history entries and at least 5 available. Feasible, and cheap to compute. A robust version would use median and MAD in place of mean and standard deviation.

### Not feasible with our data, and why

- **TSM DBMarket as published.** It trims the bottom 15–30% of *individual auctions* by volume, then removes values more than 1.5 standard deviations out. We only see the cheapest auction's price, not the book. We can approximate it with idea 1, but shouldn't call it that.
- **Sale rate, sold per day, market share or "market value" (sold/day × price), and gold per day** (TSM, Saddlebag, goldcap). These need sales records: TSM Accounting data collected across many users, or Blizzard's per-auction IDs to infer sales. TSM itself declined to publish a realm-level sale rate for lack of data.
- **Volume from vanished listings** (auctionhouse.fyi, goldcap inferred). This needs consecutive full order books with auction identities. Our `a` is a daily maximum and can't show intraday drops.
- **goldcap's buy and sell prices from completed sales** (the cheapest and dearest quarters of a day's sales). We have no sales.
- **Real-time sniping** (TSM Sniper re-scanning the last AH page, Saddlebag's Discord snipers). Our uploads arrive hours apart, so the site can only report deals after the fact.
- **Regional or cross-realm metrics** (DBRegion*, arbitrage, region medians) and **cross-player confirmation** (ForeverDB "confirmed by 2+ players"). We have one scanner on one realm and faction.
- **Order-book depth** ("price to buy X units," TUJ). We only have the single cheapest price.

---

## 1. Tool by tool

### TradeSkillMaster (TSM): AuctionDB price sources

| Metric | Shows | How computed (as published) | Data needed | Feasible for us? |
|---|---|---|---|---|
| **DBMinBuyout** | Cheapest auction now | The lowest auction on the realm as of the last pricing update; can be 30+ minutes stale ([TSM price sources](https://support.tradeskillmaster.com/custom-strings/which-price-sources-can-i-use-and-what-do-they-mean)) | Latest scan | **Yes**: this is our `m` |
| **DBMarket** | "Typical listing price" | Per scan: sort the auctions; after the first 15%, cut everything from the first ≥20% price jump; consider at most the lowest 30%; drop values more than 1.5 SD from that subset's mean; average the rest. Per day: simple average of the day's scan values. Final: weighted average of the last 14 days plus today, half-life "a little over 2 days" (exact weights only shown in a graph) ([TSM AuctionDB Market Value](https://support.tradeskillmaster.com/auctiondb-market-value)) | Every auction in every scan | **No** (needs the whole book). Approximate with a median or EMA of daily lows (inferred substitute) |
| **DBRecent** | Market value of the latest snapshot only | The same method as DBMarket on the most recent snapshot, with no time averaging ([TSM price sources](https://support.tradeskillmaster.com/custom-strings/which-price-sources-can-i-use-and-what-do-they-mean); [TSM blog](https://blog.tradeskillmaster.com/tsm-4-10-new-sources/)) | Full latest book | **No** |
| **DBHistorical** | Long-run level | 60-day average of DBMarket ([TSM price sources](https://support.tradeskillmaster.com/custom-strings/which-price-sources-can-i-use-and-what-do-they-mean)) | 60 days of DBMarket | **Analogue**: a 60-day median of daily lows once we have archived 60 days. Auctionator keeps 21, so we must archive each upload ourselves |
| **DBRegionMarketAvg / DBRegionHistorical** | Region-wide levels | Average of DBMarket across the region's realms; 60-day average of that (same page) | Many realms | **No** |
| **DBRegionSaleAvg** | Average actual sale price | From TSM Accounting data via the TSM Desktop App (same page) | Users' sale logs | **No** |
| **DBRegionSaleRate** | Share of postings that sell | "Sale Rate… averaged across all Auction Houses in your Region"; 0.4 = sells about 40% of the time ([TSM value sources](https://support.tradeskillmaster.com/custom-strings/which-value-sources-can-i-use-and-what-do-they-mean)) | Users' post and sale logs | **No** |
| **DBRegionSoldPerDay** | Units sold per AH per day | Average volume sold per AH per day in the region (same page) | Users' sale logs | **No** |
| **SaleRate / NumExpires** (personal) | Your own sell-through | From your own Accounting data. TSM added the personal version because for realm-level "there's just not enough data to provide something meaningful" ([TSM 4.10 blog](https://blog.tradeskillmaster.com/tsm-4-10-new-sources/)) | Your sales | **No** (the owner's own TSM/Accounting data could feed it later, but that's a different data source) |

**Deal-finding in TSM.** The default Shopping operation's maximum price is `dbmarket`, so it returns anything at or below market value ([TSM default operations](https://support.tradeskillmaster.com/en_US/addon/how-do-the-default-operations-work)). The **Sniper** operation repeats a search until stopped. In Classic it "repeatedly scans only the last page," where new posts appear. Its default maximum-price string is documented as "Coming Soon" ([TSM Sniper](https://support.tradeskillmaster.com/tsm-addon-documentation/tsm-addon-sniper-operations)). Community sniper strings cap the price with a share of market value and use `vendorsell` as a floor (e.g. `max(min(dbmarket…), vendorsell)`, [community pastebin](https://pastebin.com/ZGHtfhim); unofficial). The default Auctioning minimum price is `check(first(crafting,dbmarket,dbregionmarketavg), max(0.25*avg(crafting,dbmarket,dbregionmarketavg), 1.5*vendorsell))`, a useful reminder to floor prices at vendor value (cited in search results from the [TSM blog](https://blog.tradeskillmaster.com/2023/08/); the exact post wasn't fetched).

**Lesson for us (inferred).** TSM's robustness comes from looking at the *book*: trimming by volume, then by standard deviation. We can't do that inside one scan, so we get robustness *across time* instead: take medians over days and require a price to persist across scans.

### The Undermine Journal (TUJ) and Undermine Exchange (formerly Oribos Exchange)

The same author (Erorus) built all three. Oribos Exchange is the earlier name of Undermine Exchange: its front-end repo includes "migration pages for the former Oribos Exchange name" ([shatari-front](https://github.com/erorus/shatari-front)). TUJ's open-source code ([newsstand](https://github.com/erorus/newsstand)) is the best primary source on how a serious site presents AH history.

TUJ item page sections, from [`public/js/item.js`](https://raw.githubusercontent.com/erorus/newsstand/master/public/js/item.js):
- **Stats table:** available quantity; last seen (if none listed); current price; **median** (only if more than 8 history entries); mean; standard deviation with a **volatility marker "(!)" when SD ÷ mean > 0.33**; regional quantity, median and mean; vendor buy and sell prices; listing fee.
- **Snapshot chart:** price and quantity per snapshot (Highcharts Stock).
- **Daily summary:** a stock chart of daily prices with regional prices overlaid. From [`scripts/itemdaily.php`](https://raw.githubusercontent.com/erorus/newsstand/master/scripts/itemdaily.php), the monthly table stores **the price at the hour of the day's highest quantity**, plus that quantity.
- **Daily details:** a candlestick. The (currently disabled) daily SQL computes open (first non-null hourly price), close (last), low (min), high (max) and average, plus quantity min, average and max, from hourly price columns.
- **Price heat map and quantity heat map:** weekday rows × hour columns. Each cell is the **arithmetic mean** of all snapshots that fall in it. An empty cell takes the previous cell's value. The map is drawn only with **at least 14 entries**. Times are in the browser's local time zone.
- **Axis capping:** chart axes are capped at Q3 + 1.5 × IQR so outliers don't flatten the chart.
- **Market notifications:** types are quantity over/under, market price under/over, and "price to buy X units" under/over, scoped to one house or the region. The **suggested threshold is mean − SD/2**, offered only with more than 8 history entries, at least 5 available and regional quantity of at least 200.
- Hourly history is pruned after two weeks ([newsstand README](https://github.com/erorus/newsstand)).

Undermine Exchange (current, retail only) API ([API docs](https://undermine.exchange/api.html)):
- Snapshots are "roughly hourly." About 14 days of per-snapshot price and quantity are kept; daily history is kept indefinitely.
- A realm's daily record = **the maximum quantity seen that day and the price at that moment**. This is close to Auctionator's `a`.
- When quantity drops to zero, the previous price is carried forward, with a `seen` timestamp.
- The site has charts, heat maps and lists on item pages, and an "Only Below Vendor Price" filter ([site](https://undermine.exchange/)). Its metric formulas aren't published.

| TUJ/UE feature | Feasible for us? |
|---|---|
| Median, mean, SD, volatility flag (CV > 0.33) | **Yes**, from daily lows or per-upload `m` |
| Daily OHLC | **Yes, approximately.** `l`/`h` give low and high; open and close come from the first and last upload's `m` (inferred mapping) |
| Price at max-quantity moment | **Partly.** We know the day's max quantity `a`, but not which scan it came from unless `a` changed between uploads |
| Weekday × hour heat map (mean per cell) | **Partly.** 3–4 uploads a day at the owner's times leave most hour cells empty. Use weekday × time band (e.g. 4 bands), and fill nothing silently |
| Quantity heat map | **Weak**: `a` is a daily max, so there's no intraday quantity |
| Notification suggestion mean − ½SD with history and quantity guards | **Yes** |
| Regional columns, price-to-buy-X | **No** |

### Saddlebag Exchange

From its own guide ([market overview blog](https://saddlebagexchange.com/blog/wow/how-to-trade-using-our-wow-market-overview); [wiki copy](https://github-wiki-see.page/m/ff14-advanced-market-search/saddlebag-with-pockets/wiki/How-to-Trade-using-our-WoW-Market-Overview)):
- **Current Market Value** = TSM sales per day × current minimum price (it calls this "the current market share"). **Historic Market Value** = sales per day × TSM average price. Infeasible without sales. A supply-side substitute, `a` × usual price ("value listed"), measures *stock* rather than *trade*, and must be labelled so (inferred).
- **Percent Changed** = current price ÷ TSM average, with bands: **Spiking > +60%, Increasing +15…+60%, Stable ±15%, Decreasing −15…−60%, Crashing < −60%**. Feasible against our usual price.
- **Quantity Percent Remaining** = current quantity ÷ average quantity; low values suggest a possible shortage and price rise. Feasible with `a` ÷ trailing median of `a`.
- **Presentation:** a treemap-style "heat map" where box size = market value and colour = market state; a commodity quantity overview; a results table of the top 200; filters for minimum sale rate and average price.
- **Commodity Shortage Futures / shortage predictor:** defaults are minimum average price 20g, minimum sales per day 200, **current price ≥ 120% of average** and **current quantity ≤ 50% of average** ([DeepWiki summary of the code](https://deepwiki.com/ff14-advanced-market-search/saddlebag-with-pockets/5.5-shortage-predictor); third-party doc). The official wiki page is a stub ([wiki](https://github.com/ff14-advanced-market-search/saddlebag-with-pockets/wiki/How-to-trade-using-our-Commodity-Shortage-Futures)). The price and quantity tests are feasible; the sales-per-day test isn't.
- **Price Group Deltas** ([Saddlebag guide](https://saddlebagexchange.com/blog/guides/how-to-use-price-group-deltas); [wiki](https://github.com/ff14-advanced-market-search/saddlebag-with-pockets/wiki/How-to-Use-Price-Group-Deltas)):
  - each point = one week: the **median minimum price for the week** and average quantity
  - plotted as **Δ% from the first point**, with group averages and up to 10 groups per search
  - built "to find items whose prices rose around a patch, PvP season, raid release": buy before, sell after
  - the guide's own caveat: weekly medians "can hide prices that were higher right before or after raid nights"
  - example: an engineering-mount ore rose from about 0.01g to over 10g after release

  **Feasible**, and a strong fit.
- **Alerts and snipers** (price alerts, undercut alerts, a "Best AH Discount Deal Sniper," Discord price-spike alerts) are premium Discord features. Their logic isn't published ([Patreon](https://www.patreon.com/indopan/about)).
- I found **no published "price check" tool** for WoW. The nearest equivalent is the item page (minimum price, historic price, market value, sales per day, percent change).

### goldcap.gg (retail; hourly Blizzard snapshots)

From its pages ([home](https://goldcap.gg/), [deals](https://goldcap.gg/deals), [flips](https://goldcap.gg/flips)):
- **Deals:**
  - The anchor is an **exponential moving average of daily prices** once a few days exist; otherwise the snapshot's "robust market value," then the median.
  - The home feed shows **≥30% under market**.
  - Profit per unit = **0.95 × anchor − buy**. Daily profit multiplies that by the smaller of the units listed at or below the buy price and one day of what the market absorbs, which it calls "a ceiling, not a forecast: buying out the cheap end moves the price."
  - Guards: minimum fair value and margin; a **cap on discount** to stop "a single mispriced listing from faking a huge discount"; a **liquidity gate** (the item must actually be selling).
  - **Confidence:** High = several days of history in a liquid market; Medium = a healthy snapshot without depth; Low = thin, shown only under "Show all."
- **Movers:** the current hour against two days earlier, as a percentage.
- **Flips:** buy = average price of the **cheapest quarter of a day's sold units**, sell = the **dearest quarter**. Profit = sell × 0.95 − buy. "Gold a day" assumes you capture 1 in 10 of daily sales and is "a yardstick, not a promise." "Solid" flips need both prices on at least 2 days and a price that **swings rather than trends**; the rest are "Risky." The buy zone is the bottom quarter of the week's range, "at the top" the top quarter.
- **Price alerts:** a target price, then a Discord message when a listing drops below it.
- How goldcap infers "sales" isn't published. It probably uses listings disappearing between hourly snapshots, which the retail API's auction IDs allow (inferred).

Feasible for us: an EMA or median anchor, % discount, 0.95 × anchor profit, discount cap, confidence tiers, movers versus 48h earlier, buy and top zones from the price range, and "swings rather than trends" as a flip-quality test (e.g. low autocorrelation or no significant slope over 14 days; inferred implementation). Not feasible: anything built on sold units.

### auctionhouse.fyi (WoW: Forever; player scans)

A direct peer for WoW: Forever, built on player-uploaded scans like ours ([home](https://auctionhouse.fyi/), [method](https://auctionhouse.fyi/how-auction-house-prices-work), [about](https://auctionhouse.fyi/about)). It covers six markets (Normal, PvP and RP, each with Alliance and Horde).
- **Lowest price** = the lowest buyout per unit at the newest scan. **Listed** = units up at that scan.
- **Daily price = the last scan of the UTC day**; the chart also shows the day's lowest. Ranges are 1, 7, 30 and 90 days.
- **New 7-day lows** = "at or under the lowest daily close of the last 7 days."
- **Most active** = "biggest change in quantity listed over 3 days."
- **Market index** = "the 50 most traded items, value-weighted," 100 = start of range.
- **Volume** estimated from consecutive order books, where "listings that vanish before expiring count as sold." It's labelled as an estimate that can be wrong.
- **Missing data:** "No observation yet" (never scanned) is kept distinct from "None listed" (a complete scan found none); "missing observations are not treated as zero."

Feasible for us: everything except volume, which needs order books. Our index would be weighted by price × `a` ("value listed"), not by trade (inferred).

### ForeverDB auction house pages (WoW: Forever)

([AH hub](https://foreverdb.net/auction-house); [item example](https://foreverdb.net/item/2589))
- Prices come from players' ForeverDB addon scans, at most every 15 minutes; no seller or bidder names are recorded.
- **Confirmed** = two or more players agree; with three or more, "a price far from the others is left out" (the threshold isn't published).
- "Biggest movers" and "Craft for profit" use only confirmed prices and stay hidden with "Not enough days of confirmed prices yet."
- Item pages show lowest buyout per unit, the count listed and realm (faction), labelled "from one player's scan on [date]." The price history is "the median, else the lowest buyout," with the number of days with scans stated.
- We can't cross-confirm between players. The analogue is **persistence**: a price seen in two or more uploads, or matching the day's `l` (inferred).

### Classic-era addons with personal-scan methods (closest to our situation)

- **aux** (Classic): the daily value is the **day's minimum buyout**. Market value is the **median of the last 11 daily values**; older days weigh less, but this barely matters inside a month. The `percent/60` filter finds auctions at ≤60% of value ([Warcraft Tavern on aux](https://www.warcrafttavern.com/wow-classic/addons/aux/)). **Our closest template; feasible exactly.**
- **FlipScout:** compares current prices with the **median of recent historical scans**, with user minimum *and maximum* discount filters ("max" removes outliers and bad data), and shows time since last seen. "The more you scan, the more accurate" ([CurseForge](https://www.curseforge.com/wow/addons/flipscout)).
- **Hammerprice** (Forever): deals are listings under 50–90% of market value; market value = network price, else this account's 14-day weighted history ([CurseForge](https://www.curseforge.com/wow/addons/hammerprice)).
- **AHPriceTracker:** a weekday × hourly-slot grid of average prices for tracked items ([CurseForge](https://www.curseforge.com/wow/addons/ahpricetracker)).
- **ProfitProphet:** a day × hour price heatmap "from your own scan history"; buy/hold/sell signals from where the price sits in its observed range ([CurseForge](https://www.curseforge.com/wow/addons/profitprophet)).
- **Auctioneer:** needs "a few days- at the very least" of scans before its price recommendations are reasonable ([CurseForge](https://www.curseforge.com/wow/addons/auctioneer)).
- **Forever Stocks:** AH price "after the 5% cut" against vendor price, with a minimum-gain percentage; prices older than 30 minutes must be rescanned before posting ([CurseForge](https://www.curseforge.com/wow/addons/foreverstonks)).

**Fees.** The faction AH cut is 5% ([warcraft.wiki.gg Auction House](https://warcraft.wiki.gg/wiki/Auction_House)). Classic neutral houses took 15% ([Talk:Auction House](https://warcraft.wiki.gg/wiki/Talk:Auction_House); addon notes). The deposit scales with vendor sell price × duration; modern rates are 15/30/60% of vendor price for 12/24/48h (same wiki page). Forever addons expose 12/24/48h durations (Forever Stocks), but **the exact Forever deposit rates are unverified** and should be read from the game or client data before we compute net profit.

---

## 2. Q1: robust deal / underpriced detection

**Methods published by tools**
- **Percent of a baseline:** aux ≤60%; goldcap ≥30% off an EMA; Hammerprice 50–90%; TSM Shopping ≤ DBMarket; Saddlebag "Crashing" < −60%. All of these work against a *time-smoothed* baseline.
- **Mean minus k standard deviations:** TUJ suggests mean − 0.5σ as an alert price.
- **Robust z-score:** none of the WoW tools publishes one. Statistically, the modified z-score Mᵢ = 0.6745 × (xᵢ − median) ÷ MAD, flagging |Mᵢ| > 3.5, is the standard robust test (Iglewicz & Hoaglin, via [NIST handbook](https://itl.nist.gov/div898/handbook/eda/section3/eda35h.htm)). It resists the very outliers it's hunting, unlike mean and SD (NIST notes the ordinary z-score is bounded by (n−1)/√n for small n). Caveat: MAD = 0 when over half the values are equal, which is common for a stable item at a round price. Fall back to an IQR or percentage rule ([metricgate](https://metricgate.com/calculator/robust-z-score-modified)).

**Recommended rule for us (inferred design, from the above):**
- baseline B = median of daily `l` over the last 14 days (at least 7 days with data; else "provisional")
- discount d = 1 − m ÷ B
- flag if d ≥ 30% **and** modified z ≤ −3.5 (or, when MAD = 0, m ≤ 0.7 × B)
- tier: **High** = 14+ days of history, item present on 80%+ of days, d persists across 2 consecutive uploads or equals the day's `l`; **Medium** = 7–13 days; **Low** = fewer, hidden by default

**Guards and pitfalls**

| Pitfall | Why it bites our data | Guard |
|---|---|---|
| **Single cheap unit** | `m` is the cheapest *auction*, regardless of size; one unit at a low price sets `m` (inferred from Auctionator's definition) | Require `a` above a floor (TUJ uses ≥5 available); show "at least one unit," never "stock at this price"; cap the discount (goldcap, FlipScout max-discount) e.g. > 85% off → "check: possible misprice" |
| **Troll / bait listings** | Very high listings don't affect `m`, but they inflate `h` | Never use `h` as "market"; build the baseline from `l` and medians |
| **Stale prices** | Auctionator keeps the old `m` for items absent from a scan (inferred); Undermine Exchange explicitly carries prices forward when quantity is 0 | Store per-item "last seen in scan" and only flag items seen in the *latest* upload; show scan age everywhere (TSM: DBMinBuyout "30 minutes or more" stale) |
| **Already gone** | Our site updates hours after a scan; cheap listings are bought fast | Word it as "seen at X at 14:05," not "available"; keep a log of past deals with whether the next upload still showed them (inferred) |
| **Thin history at launch** | No baseline for the first days, and prices drift fast after a launch | Gate as ForeverDB does ("not enough days yet"); use a short window (3–7 days) and label it "provisional" |
| **Below vendor price** | Real but rare; a genuine deal if vendor sell > m | Highlight separately (Undermine "Only Below Vendor Price" filter); always true profit if you can buy it |
| **Partial scans** | Auctionator also records prices from ordinary searches (inferred), so `l`/`h` may include observations from moments we never received | Treat `l` as "lowest seen that day," not "lowest at scan times"; prefer per-upload `m` for timing analysis |
| **Trend, not dip** | A falling market makes everything look cheap against a 14-day median | Compare against a short EMA too; skip if the 3-day median is also below the threshold (inferred). goldcap's flips likewise prefer items whose price "swings rather than trends" |

## 3. Q2: investment and flip scoring, and sell-through proxies

**Published formulas**
- goldcap deal profit per unit = 0.95 × anchor − buy, multiplied by min(units at or below the buy price, one day of absorption). It's "a ceiling, not a forecast."
- goldcap flip profit = sell (dearest-quarter sales) × 0.95 − buy (cheapest-quarter sales). "Gold a day" = profit × 10% of daily units sold. "Solid" needs at least 2 days and a swinging price.
- Saddlebag ranks by sold/day × price ("market share").
- TSM users weight by DBRegionSaleRate and DBRegionSoldPerDay in custom strings (sources above).
- Auctionworthy (Classic, Auctionator-based) cost = 24h deposit + vendor price + 5% cut if sold ([CurseForge](https://www.curseforge.com/wow/addons/auctionworthy)).

**Feasible score for us (inferred design):**
```
buy      = current m (or B for "buy at usual price")
resale   = P75 of daily l over 14 days        # a typical "good day" floor price
net      = resale × 0.95 − deposit(vendor price, duration) − buy
ROI      = net ÷ buy
risk     = CV of daily l (TUJ volatile if > 0.33) and downside = buy − P10(daily l)
presence = share of days the item was listed  # a crude liquidity floor
score    = ROI × presence, shown only if presence ≥ 0.8 and history ≥ 14 days
```
For **investments** (buy now, sell later), compare the current price with the same item's level on comparable past weeks. After a few weeks this means the same weekday; at an event, the post-event level from Price Group Deltas.

**Sell-through proxies without sales: how honest each is**

| Proxy | How | Strength |
|---|---|---|
| **Price recovery after a dip** | When `m` is low at upload t and back near B at t+1 (within hours), the cheap auctions vanished | **Weak to moderate.** They vanish by purchase, cancel or expiry. The shortest duration (12h on Forever, if confirmed) caps how often expiry can explain a fast vanish, but we never know when it was posted. Count "recoveries within 12h" as an indicator, not sales (inferred) |
| **Day-over-day drop in `a`** | `a` today < `a` yesterday | **Weak.** `a` is the day's maximum, so more uploads mean a higher `a`, and new posts offset sales. Normalise by number of observations and use 3-day changes (as auctionhouse.fyi's "most active" does) |
| **Presence ratio** | Days listed ÷ days observed | **Weak** on demand, but useful for spotting items that never appear |
| **Gap between `l` and `h` within a day** | A wide gap means the cheapest listing changed a lot during the day, i.e. turnover at the bottom | **Weak.** Undercutting also causes it (inferred) |
| **Owner's own sales** | If the owner's TSM or Auctionator records his sales | **Strong but personal**, and a different data source (out of scope) |

We should not publish "sold per day." Any liquidity label should say "listing activity."

## 4. Q3: intraday and weekday patterns

**How tools measure them.** TUJ, Undermine Exchange, AHPriceTracker and ProfitProphet all bucket price observations into weekday × hour cells and take the mean. TUJ requires at least 14 entries and fills empty cells from the previous cell. Saddlebag's weekly medians deliberately smooth out intraweek swings. **No tool I found publishes a cross-item, normalised index of time effects.** That is our opportunity, but it's our own design (inferred):
1. For each item and upload, r = m ÷ (that item's centred 7-day median of `m`). This removes trend and price level.
2. Pool r across items within a category (e.g. flasks, herbs, cloth) by weekday, and by scan-time band (e.g. 00–06, 06–12, 12–18, 18–24 server time). Use the median of r and count n.
3. Show a cell only with n ≥ 20 item-observations from ≥ 3 distinct weeks (inferred threshold). Draw it as a heat map of % deviation, with n in the tooltip.

**How much data.** Each weekday occurs once a week, so per item a weekday effect has about 4 samples after a month. That's too few to separate a 5–10% effect from noise unless we pool across items (inferred). Rough guide: **weekday profiles after 4 weeks, pooled by category; per-item weekday profiles after about 8 weeks; time-of-day only for the bands the owner actually scans.** Our scan times are self-selected (the owner scans when he plays), so time-of-day differences can reflect *when* he scans as much as the market. Label the chart this way.

**Known or claimed patterns (Classic/Vanilla-style) — sources disagree:**
- **Weekend.** Almar's Classic guide: buy Monday/Tuesday, sell Friday/Saturday. Sunday into Monday brings a flood of supply and undercutting; the best buying window is roughly 3–8am Monday; prices recover through Monday evening ([Almar's Guides](https://almarsguides.com/WoW/Farming/Classic/AuctionHouse/)). The Warcraft Wiki says the opposite for materials: weekends "can favor buying materials" (supply is high), weekdays selling ([Auction guide](https://warcraft.wiki.gg/wiki/Auction_guide)). **Conflicting claims, so this is exactly what our data should test.**
- **Time of day.** Activity peaks around 6–9pm server time and is lowest around 6am; raid-related demand peaks around 8–10pm on raid evenings (Warcraft Wiki, unmeasured).
- **Reset day / raid nights.** Guides say to buy potions and flasks over the weekend and sell after the Tuesday reset, and that demand for flasks spikes just before reset as raids prepare. Sources are gold-seller and SEO sites ([IGVault copy](https://ozguryazilim.itu.edu.tr/qa.back/606/igvault-wow-fast-way-how-to-make-gold-burning-crusade-classic)), so **weak**. A TBC Classic forum anecdote: flasks up about 10g on Tuesday, back down Wednesday (search summary; source not fetched). US reset is Tuesday, EU Wednesday. WoW: Forever's reset day and raid lockout timings should be checked against Blizzard's posts (not verified here).
- **Maintenance.** Auctions keep expiring during downtime; quiet Monday/Tuesday is partly due to maintenance (Warcraft Wiki).

## 5. Q4: event effects (raid openings, content phases, new realms)

The evidence here is **thin and mostly anecdotal or commercially biased**. I found no published measured study.
- **Phase-dependent value.** Elemental Earth gains as Ahn'Qiraj approaches and spikes on release; Elemental Fire holds value through Molten Core/BWL, then fades in AQ/Naxx (Almar's Guides).
- **Pre-release stockpiling.** Gold-seller guides advise buying herbs and flasks before a phase opens and selling launch week, claiming "200–500% ROI" with no data ([MMOGAH](https://www.mmogah.com/news/wow-classic-20th-anniversary/best-items-to-flip-for-gold-before-phase-6-in-classic-anniversary)). Treat it as a hypothesis, not a fact.
- **Demand ramps more slowly than expected.** A Wowhead commenter (Legion era) argued most players can't play in a new raid's first two days, so consumables see a "slow sustained" market rather than a day-one spike. Gem prices came back down once most players had what they needed (search summaries of [Wowhead comments](https://www.wowhead.com/classic/news=277482); comment text not fetched directly).
- **Release-driven spikes do happen.** Saddlebag's example ore went from about 0.01g to over 10g after the engineering-mount release, and its tool exists to study exactly this (Price Group Deltas guide).
- **Supply shocks crash prices.** A mistaken vendor flooded the AH with Nexus Crystals at a Season of Discovery raid release ([Icy Veins](https://wp-prod.icy-veins.com/tier-2-and-rank-13-ptr-gold-vendor-on-live-season-of-discovery-aq-raid-release-and-very-easy-raid-bosses-from-the-wrong-version/)).
- **New realm launch.** On fresh realms, gold is scarcer and early effort is worth more ([Icy Veins, Wrath fresh realms](https://www.icy-veins.com/wotlk-classic/wrath-of-the-lich-king-fresh-start-realms-explained)). Realm-locked Classic markets are "thin, volatile, and highly sensitive to a handful of active players" ([Ten Ton Hammer](https://www.tentonhammer.com/articles/what-a-realmless-classic-economy-means-for-gold)). Materials "spike for two weeks, then crater" after an expansion launch (retail; [IPLocation blog](https://www.iplocation.net/blog/why-wows-economy-is-broken-in-2026-and-how-to-profit-from-it), weak source). In the first weeks, raw materials are in high demand and low supply, and early AH volatility is high ([community post](https://docs.fincra.com/discuss/69843e7a0d9e67b5a21332dd), weak source). Season of Discovery's start was hard for gold-makers mainly because AH data tooling was missing ([Wowhead economy wrap-up 305](https://fr.wowhead.com/news/tradeskillmaster-and-season-of-discovery-wowhead-economy-weekly-wrap-up-305-336539)). **For Forever (inferred):** expect early prices for low-level materials (copper, linen, light leather, low herbs) to be high and falling as supply grows. High-level materials and raid consumables will have little or no price history until players reach them, then a demand ramp before the first raid opens. All of that is a hypothesis for our data to confirm.

**How to measure it (inferred design):** an event marker on the timeline (launch, first raid open, each reset), plus a Price Group Deltas-style chart. Each group's median of (weekly median `m` ÷ its value in the week before the event), shown from 2 weeks before to 4 weeks after. Annotate n items and n days.

## 6. Q5: presentation and honesty conventions

**Charts and tables used**
- **Price history:** snapshot line chart with price and quantity on twin axes (TUJ, Highcharts Stock); range selectors 1/7/30/90 days, with daily close plus daily lowest (auctionhouse.fyi); candlestick OHLC with a quantity range (TUJ daily details).
- **Heat maps:** weekday × hour for price and for quantity (TUJ, Undermine Exchange, AHPriceTracker, ProfitProphet); a treemap sized by value and coloured by market state (Saddlebag).
- **Indexed comparisons:** Δ% from start, per item and per group average (Saddlebag Price Group Deltas); market index with base 100 (auctionhouse.fyi).
- **Lists:** deals as cards with buy, market and discount (goldcap); movers and gainers/losers; new 7-day lows; most active; results table limited to the top N (Saddlebag top 200).
- **Stats panel:** current, median, mean, SD with a volatility marker, last seen, vendor price, listing fee (TUJ).
- **Alerts:** quantity over/under, price under/over, price to buy X (TUJ); a target price pushed to Discord (goldcap, Saddlebag). For a static site, the equivalent is a published "watchlist hits" list per upload (inferred).

**Honesty conventions worth adopting**
- **Label estimates as estimates:** goldcap's "a ceiling, not a forecast" and "a yardstick, not a promise"; auctionhouse.fyi calls volume an estimate that "can be wrong"; Undermine Exchange data are listing prices, not completed sales (noted by the DealScryer addon, [CurseForge](https://www.curseforge.com/wow/addons/dealscryer)).
- **Show data age and provenance on every number:** ForeverDB's "from one player's scan on [date]"; TSM notes that DBMinBuyout can be 30+ minutes stale; auctionhouse.fyi's "latest scan" timestamp.
- **Keep "never observed" separate from "none listed,"** and never treat missing as zero (auctionhouse.fyi).
- **Gate sections until there's enough history:** ForeverDB's "not enough days of confirmed prices yet"; TUJ's minimums of more than 8 and at least 14 entries.
- **Confidence tiers, with low confidence hidden by default** (goldcap).
- **Cap chart axes at Q3 + 1.5 × IQR** so one troll listing doesn't flatten the chart (TUJ). Show the capped point as an arrow (inferred).
- **Disclaim affiliation** (auctionhouse.fyi "Not affiliated with Blizzard Entertainment"). For Tazdingo this must be done in its impersonal voice.

## Gaps and things to verify

- TSM's exact 14-day weights (published only as a graph) and the Sniper default string ("Coming Soon").
- WoW: Forever's deposit percentages, auction durations (12/24/48h per Forever addons) and reset day. Check in game or in client data before computing net profit.
- Whether Auctionator updates `m`/`l`/`h` from ordinary searches as well as full scans, and whether `m` is left stale for items missing from a scan. Check in Auctionator's source (`Auctionator/Source/Database`), not done here.
- goldcap.gg's sales-inference method and "robust market value" definition (not published).
- OribosExchange.com didn't respond (connection refused). It now redirects into Undermine Exchange per the shatari-front repo.
- No measured, published study of Classic weekday or raid-release price effects was found. Everything in §4–5 apart from the tool methods is guide lore.
