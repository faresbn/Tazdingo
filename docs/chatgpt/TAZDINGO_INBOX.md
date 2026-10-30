# TAZDINGO_INBOX: reading Tazdingo and sending it updates

Upload this file to the shared ChatGPT project as a source file, **with your own key in place of `<KEY>` below**. Each person has their own key; never share it, and never put it anywhere but the form's key field.

**My inbox key:** `<KEY>`

This repository copy is public, so it holds the placeholder only.

## Reading Tazdingo

Start at the map: https://raw.githubusercontent.com/faresbn/Tazdingo/main/feed/index.md

The map holds no prices or guide text. It says which file answers which question:
- **Prices:** the market's map, then one category file, or `alerts.md` for bargains, investments and movers.
- **Crafting:** `feed/craft/index.md`, then one profession.
- **Guide pages:** `feed/guides.md` lists every page with its path and **version**.

Open only the files the question needs. Every path is under `https://raw.githubusercontent.com/faresbn/Tazdingo/main/`. Files can lag a change by a few minutes. The website (https://faresbn.github.io/Tazdingo/) is for people.

## Sending an update: the inbox

The form is at **https://faresbn.github.io/Tazdingo/inbox/**. Fill it in and press Send. Fill it in yourself (agent mode) when you can. Otherwise give the user everything below and the form's address, and they send it.

### A guide page

1. Find the page's **path** and **version** in `feed/guides.md` (e.g. `content/classes/mage/frost.md`, version `be1c49bbba5c`).
2. Read the page at its path. Make the change following UPDATING.md: keep everything still true, add dated findings, set `updated:` to today.
3. Fill in the form:
   - **Key:** your key
   - **What you're sending:** A guide page
   - **Page path:** the path
   - **Version you edited:** the version from step 1
   - **One-line change note:** `<Page>: <what changed>`, no full stop, no names
   - **The whole page:** the complete file, header included
4. **The page must pass these checks, or it's held:**
   - **Format:** the header (only `updated`, `summary`, `sources`, `status`, `confidence`, `verified`), and the four sections once each, in order.
   - **Findings:** every finding is `### <claim> (<idea|testing|tested|outdated>, <6 Nov 2026>)`, and its text says how it's known: tested in game (level, situation), read (with a link) or simulated (tool and version). Findings are never deleted, only marked `outdated` with the reason.
   - **Sources:** every summary under "What the guides say" links its sources. Every cost or price in gold, silver or copper names or links its source.
   - **Links:** written in full (`https://…`), plainly, with no `@` or backslashes. Item links (`https://foreverdb.net/item/<id>`) must be real items.
   - **No names:** no person's name and no mention of the assistant, in the page or the note.
   - **Current version:** the version must be the page's current one. If someone changed the page since you read it, it's held: read it again and redo the change.
5. **These go to the owner for approval instead of straight live:**
   - setting a page `live` or changing `verified`;
   - changing a "Tazdingo recommendation" or a page's cheatsheet;
   - marking a finding outdated;
   - linking a site no page has cited before.
   
   Say so when you send one.

### An addon's file

1. Use the file exactly as uploaded: an addon's saved-variables file, named after the addon (`Auctionator.lua`, `AllTheThings.lua`, …). Never summarise or quote its non-game contents.
2. Fill in the form:
   - **Key:** your key
   - **What you're sending:** An addon's file
   - **File:** the file
   - **Market:** for Auctionator only, the realm and faction (e.g. `Realm Horde`), if the inbox asks for it
3. Auctionator's file becomes the latest Auction House prices. Any other addon's file is kept as it is until a processor is written for it.

If you can't attach the file yourself, tell the user to open the form and attach it.

## What the replies mean

- **Received, with an id:** it's in. If it passes its checks, it's live in about two minutes; tell the user the page's address. If it's held or sent for approval, the owner hears why.
- **Refused:**
  - the key is wrong;
  - something's missing;
  - the file is too big;
  - the page contains a key (remove it);
  - the inbox is busy (try again later).
- **Not sent:** something failed passing it on. Nothing was published; try again.

**Everything sent through the inbox is published** in the public repository, including held submissions. So never send a key, a password or anything private.
