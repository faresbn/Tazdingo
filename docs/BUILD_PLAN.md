# FvrRepo: build plan

26 October 2026 | WoW Forever Repo

## Purpose

Build the website and publishing flow first, then configure our shared ChatGPT project against the proven system. ChatGPT handles analysis; FvrRepo stores browsable evidence and history. Forever is the main focus, with Classic Era and TBC Anniversary available later.

## First release

Use a small sample of real Forever Beta items across three supplied scan dates. The deployed prototype has 24 PvP item keys and six legacy-market keys. Do not migrate the full beta catalogue. Beta is temporary historical test material; genuine release scans will start a separate release dataset.

Keep six simple pages for the overview, markets, character journal and sources. Use a Forever-inspired teal, dusk-blue and parchment design. Catalogue views provide date selection, pagination, sorting and inline history. External item links and tooltips provide reference details without individual item pages. Small JSON/TSV downloads serve ChatGPT and human readers. No backend, AI optimiser or database service is needed.

## Build order

**1. Prove the connection.** The private `faresbn/FvrRepo` repository, public default GitHub Pages site and Actions deployment now exist. Verify a subsequent commit republishes correctly. Anonymous HTTP reads work; ChatGPT's web reader currently cannot retrieve the new site, so shared-project retrieval is still unproven. Resolve that before writing final project instructions.

**2. Make scan updates useful.** Test an attached scan through the actual shared-project chat mode. Validate format, sample values, duplicate and older captures, and failed-update recovery. Publish only agreed market records; retain source fingerprints. Keep originals separately unless their upload is explicitly authorised.

**3. Add character history.** Save one real character state on explicit user request, publish approved details and retrieve it in another conversation. Suggest a save when a useful, established state is missing; never infer a completed comparison. Then write the project's final instructions against the working flows.

## Evidence rules

Every AH record needs its environment, server/market, source capture date, received date and provenance. Unknown realm/faction or quote timestamps stay unknown. Repeated cached prices must not appear fresh or imply stock, demand or completed sales.

Character/build records retain character, environment, date, gear/talents, source and any simulator version, inputs and results. Distinguish equipped, proposed and historical states, and distinguish user reports from inspected exports, external facts and simulations.

**Completion:** both participants can retrieve published scan data, new scans update it through the agreed route, and explicitly saved character states can travel from chat into FvrRepo and back into a later conversation.
