---
updated: 2026-10-27
summary: Problems players have hit, what Blizzard has said about each, and any workaround.
sources: Blizzard's forums (known-issues threads, staff posts and player threads), ForeverDB and foreverchanges.pro, checked 27 October 2026
---

## At a glance

- **No launch thread yet:** Blizzard's known-issues list is the beta's, last updated on 8 October. The beta closed on 23 October.
- **Biggest player report:** some Macs freeze or restart when a character enters the world. Players' fix: set Secondary Lighting to Fair.
- **Your beta setup won't appear:** the live game is a new install. Copy your settings across.
- **Economy holds:** Blizzard's anti-gold-buying system can temporarily lock trade, mail and the Auction House, with false positives possible.
- **Beta-only bugs may be gone:** items below say when they were last reported; check again after launch.

## What the guides say

### Tazdingo recommendation

**Match the symptom and report date before applying a workaround.** An old Beta report does not prove a launch bug, and a later fix for a similar symptom does not prove every case is resolved. Prefer specific [official fixes](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-%E2%80%93-updated-october-26/2360696) over an older issue list. Change one setting at a time and retain a copy of working settings before replacing or resetting files. Player workarounds remain unconfirmed unless the same case has been reproduced; no launch-client testing is recorded here.

Blizzard keeps one known-issues thread and edits it in place: [US forums](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-known-issues-october-8/2352687), [EU forums](https://eu.forums.blizzard.com/en/wow/t/wow-forever-beta-known-issues-8-october/629369). Staff posts also collect on [Wowhead's blue tracker](https://www.wowhead.com/forever/blue-tracker). Blizzard said that after the beta it would spend a few days on priority issues and the game service before launch ([forum post](https://us.forums.blizzard.com/en/wow/t/thank-you-for-testing-the-wow-forever-beta/2390465)).

### macOS: the game freezes the Mac on entering the world

- **Who:** Apple silicon Macs (M1 to M5), mostly on macOS 26 and 27, though players also reported it on older versions. One player saw the same on Linux.
- **What:** the loading bar finishes, then the screen hangs. WindowServer stops responding and the Mac returns to its login screen, and sometimes restarts after a kernel panic. Some players also saw a green tint and black textures.
- **Status:** reported by players from 17 September; no staff reply in the [players' thread](https://us.forums.blizzard.com/en/wow/t/macos-27-and-forever-windowserver-crash/2352734) as of 27 October. Blizzard's builds of [22 September](https://us.forums.blizzard.com/en/wow/t/beta-client-update-september-22/2358655) ("Fixed some display issues and stability issues on Macs") and 24 September (Mac water and display fixes, [development notes](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-%E2%80%93-updated-october-26/2360696)) followed. Afterwards one player could raise every setting to maximum, while another said the fix didn't fully work.
- **Workaround players report:** set Secondary Lighting to Fair in the graphics settings; several players say this fixed it, though two said it didn't help them. Set Shadow Quality to Low for the green tint. Failing that, lower the overall graphics quality before entering the world. None of this is confirmed by Blizzard.

### Your beta interface, keybinds and addon settings are missing

- **Who:** anyone who played the beta.
- **What:** the live game installs into its own `_forever_` folder with a fresh `WTF` folder, so nothing set up in the beta's `_classic_beta_` folder appears ([ForeverDB](https://foreverdb.net/launch/beta)).
- **Status:** expected behaviour; Blizzard hasn't said whether anything from the beta carries over.
- **Workaround:** with the game closed, copy the files you want from the beta's `WTF\Account\<account>` folder to the same place under `_forever_`; per-character files only fit if the names match. A [player's guide](https://us.forums.blizzard.com/en/wow/t/wow-forever-moving-your-beta-setup-to-live-macros-keybinds-ui-chat-and-addon-settings/2386497) lists where each setting lives; another player confirmed it worked on the stress test servers on 22 October. Edit Mode layouts can also be copied with the layout menu's Share button and imported on live.

### Addon settings reset after logging out

- **Who:** some addon users.
- **What:** addons forget their settings between sessions.
- **Status:** conflicting reports. [foreverchanges.pro](https://foreverchanges.pro/addons) says players saw it fixed from the 24 September build (1.60.1.70009). An addon author on [Blizzard's forums](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-addon-feedback/2385926) reported on 18 October that saved settings still didn't persist when tested on 7 October. Not acknowledged by Blizzard.
- **Workaround:** none confirmed. Log out normally rather than closing the game, and check after launch.

### Macros won't save, or the New button does nothing

- **Who:** some players in the beta, including several using the gamepad interface.
- **What:** macros, their names or icons don't save, or no button appears to drag to a bar.
- **Status:** player reports from 21 September to 5 October ([thread](https://us.forums.blizzard.com/en/wow/t/when-will-the-macro-panel-work/2372745)); not acknowledged by Blizzard.
- **Workaround players report:** press New first, then choose the name and icon, then type the macro. Character-specific macros worked for one player when general ones didn't. Log out to make sure macros save. As a last resort, close the game, back up the macro cache files, then move the originals out of your `WTF\Account\<account>` folder so the game makes fresh ones.

### The game crashes after closing the Options menu (gamepad interface)

- **Who:** players using the gamepad interface.
- **What:** opening Options in the world and then closing it froze and crashed the client.
- **Status:** two player reports, 4 and 5 October ([thread](https://us.forums.blizzard.com/en/wow/t/option-menu-crashes-game-macros-dont-save/2372230)). Separately, Blizzard listed on 1 October that switching to or from the gamepad interface resets your Edit Mode layout to the default.
- **Workaround:** none reported. Save an Edit Mode share string before switching interfaces.

### Temporary Economy Hold on your account

- **Who:** accounts the system suspects of buying or selling gold for real money.
- **What:** trade, mail, guild banks and the Auction House are restricted while Blizzard investigates.
- **Status:** Blizzard, 13 October: a new system that may give false positives. A hold is lifted automatically if cleared and leaves no permanent strike ([forum post](https://us.forums.blizzard.com/en/wow/t/temporary-economy-holds-for-rmt/2381433)).
- **Workaround:** none needed for normal play. Don't accept gold from strangers; Blizzard is adding a warning to trades with strangers ([forum post](https://us.forums.blizzard.com/en/wow/t/actions-taken-against-botting-and-rmt/2368705)).

### Grouping moves you to another copy of the world

- **Who:** players forming or changing groups.
- **What:** creating a group or changing its members can move you to a different world instance (layer). Players also reported layer changes when crossing zone borders.
- **Status:** on Blizzard's known-issues list since 24 September, not marked resolved; Blizzard said it was working on improvements. Player report of zone-border layering: [thread](https://us.forums.blizzard.com/en/wow/t/why-doesnt-the-known-issues-include-the-game-breaking-layering-problems/2379626), 11 October.
- **Workaround:** none given.

### Stuck on "Retrieving character list"

- **Who:** anyone logging in during maintenance or a service problem.
- **What:** the realm accepts your login but doesn't send your characters.
- **Status:** usually on Blizzard's side ([ForeverDB](https://foreverdb.net/launch/beta-errors)).
- **Workaround:** check the server status and Blizzard's posts. Your `_forever_\Logs\Connection.log` shows where the login stopped.

### Older items on Blizzard's beta list

- **Who:** varies.
- **What:** items Blizzard listed and hasn't marked fixed: enemies can parry and block from behind if you stand very close; the full install is larger than intended; queuing Heroic Strike, Cleave or Raptor Strike disables the spell queue window; Faerie Fire and similar debuffs were reported to cause no threat; the character pane doesn't show level, class or titles.
- **Status:** listed between 17 September and 1 October in the [beta known issues](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-known-issues-october-8/2352687); launch status unknown.
- **Workaround:** Blizzard's only advice is to avoid standing too close to enemies until the parry bug is fixed.

### Resolved in later notes: Demoralizing Shout threat

The older list says this shout generated no threat. The [2 October development notes](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-%E2%80%93-updated-october-26/2360696/5) explicitly fix it. Do not treat the older list as the current rule. The same notes confirm that absorbs are ignored when calculating Warrior and Druid Rage.

## Field findings

Nothing recorded yet.

## Read more

- [Blizzard forums: Beta known issues (US)](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-known-issues-october-8/2352687): Blizzard's own list, edited in place
- [Blizzard forums: Beta development notes](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-%E2%80%93-updated-october-26/2360696): what each build fixed
- [Blizzard forums: Mac WindowServer crash thread](https://us.forums.blizzard.com/en/wow/t/macos-27-and-forever-windowserver-crash/2352734): player reports and settings that helped
- [Blizzard forums: Moving your beta setup to live](https://us.forums.blizzard.com/en/wow/t/wow-forever-moving-your-beta-setup-to-live-macros-keybinds-ui-chat-and-addon-settings/2386497): where each setting is stored
- [Blizzard forums: Temporary Economy Holds](https://us.forums.blizzard.com/en/wow/t/temporary-economy-holds-for-rmt/2381433): how the anti-gold-buying hold works
- [ForeverDB: Beta errors](https://foreverdb.net/launch/beta-errors): reading your connection log
- [foreverchanges.pro: Addons](https://foreverchanges.pro/addons): small addons that patched beta bugs
- [Wowhead: Blue tracker](https://www.wowhead.com/forever/blue-tracker): every staff post in one place
