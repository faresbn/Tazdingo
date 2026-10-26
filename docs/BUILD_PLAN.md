# FvrRepo: build plan

26 October 2026 | Implementation started | FvrRepo: WoW Forever Repo

## Purpose

Build the website and its publishing flow first, then configure Fares and Mike's shared ChatGPT project to use it. FvrRepo is a browsable collection of shared Warcraft evidence and history. ChatGPT handles the analysis. Forever is the main focus; Classic Era and TBC Anniversary remain supported.

Forever Beta data is temporary historical material for building and testing the site. Beta support is not part of the future project's scope, and those prices will never become release prices.

## Two connected flows

**Auction House.** Upload an Auctionator scan in chat; validate it and commit the authorised market records privately to GitHub. Keep original-file fingerprints and preserve originals separately until their upload is explicitly approved. GitHub Actions publishes readable pages and downloadable records. ChatGPT retrieves those records for price lookups, reputation routes, profession planning and crafting analysis.

**Characters and comparisons.** Capture character/environment details and selected gear, build or simulation comparisons from project conversations. Save dated records to GitHub and publish the approved information on FvrRepo. Later conversations retrieve those records as history, rather than relying on chat memory or treating an old snapshot as current. Save only when the user explicitly requests a character-state save. Suggest one when a useful, sufficiently established state has no record yet; do not infer that a comparison is completed.

Both flows use the same repository and publishing process. Verify uploads through the actual chat mode you intend to use; if only Work supports writes, resolve that limitation early.

## The website

Start with Home, AH and Characters & Comparisons. Use a simple, mobile-friendly design inspired by the official Forever brand and website: teal, dusk-blue and parchment tones, with original decorative artwork. Use an interactive catalogue with capture-date selection, inline history and external item tooltips; no individual item pages. Keep small price partitions and separate history downloads. Generate browsing views and downloads from the same records, so humans and ChatGPT use the same evidence. Keep sources and limitations alongside the relevant records.

There is no AI optimiser, application backend or separate database service. The private repository holds originals and processing code; the Pages site publishes the agreed information and is publicly readable.

## Records we need to trust

**AH history:** identify the game environment, server/market, capture/download date, upload date and source scan. Preserve successive scans and available per-item observation dates. Repeated uploads or retained quotes must not look like fresh observations. Cached minimum prices do not establish current stock, completed sales or demand.

**Character/build history:** identify the player/character, environment, date, source and relevant gear/talents. Comparisons retain their question, inputs, actual results and simulator version where applicable. Distinguish user-reported details, inspected exports, externally verified facts and simulated results; do not label everything verified. Separate equipped, proposed and historical configurations.

Preserve original evidence privately, publish approved details, and retain the data behind saved conclusions. Parse Lua without executing it, check extraction against its source, and leave the previous working site available if an update fails.

## Build order

**1. Prove the connection.** Create the private FvrRepo repository and configure Pages. Publish a small labelled test dataset. Verify both participants can retrieve the correct records through ChatGPT without your GitHub connection. Test an attached-file update and confirm the changed public result.

**2. Make AH updates useful.** Build and test with a small selection of real beta items across the three scan dates. Do not migrate the complete beta catalogue. Test duplicates, older scans and failed updates. Establish the website's actual retrieval contract: record formats, direct URLs, market/date identification and publication revisions. Add older captures when useful rather than requiring a complete archive migration.

**3. Add the conversation-to-history flow.** Save one real character snapshot and comparison from chat, publish the approved record, then retrieve it in another conversation. Once these flows work, write the shared project's final instructions and workflows against the established system. After launch, validate the first genuine release scan and begin release history separately.

## Test material

Three original beta Auctionator exports are now supplied, dated 6, 10 and 17 October. Use them to test parsing, separate markets and history. A character snapshot can follow when we reach the second flow; no character state should be invented for the test site.

**Done means:** new scans update the website through the agreed route; both participants can use its data without replacing Project Sources; and character/build records can travel from a conversation into FvrRepo and back into a later conversation with their provenance intact.
