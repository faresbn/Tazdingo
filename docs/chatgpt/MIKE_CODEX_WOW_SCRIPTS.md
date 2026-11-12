# Tazdingo's automatic updates on a co-player's Windows PC: instructions for Codex

**Reader:** Codex (CLI or desktop app) on a co-player's Windows 11 Home PC, working with that co-player. Read this whole file before doing anything, then do the steps with them, one at a time, and stop to ask whenever a step needs their answer or their hands.

**Address of this file:** https://raw.githubusercontent.com/faresbn/Tazdingo/main/docs/chatgpt/MIKE_CODEX_WOW_SCRIPTS.md (the repository is public: reading it needs no account).

## What this gives the co-player

- **Auction House scans, automatically (part 1).** After every scan, when they `/reload` or log out, their PC sends the scan to Tazdingo by itself, and a few minutes later a Windows notification says the prices are published, or why not. Their scans join the same price history as Fares's (one market per realm and faction) on https://faresbn.github.io/Tazdingo/ and in the feed ChatGPT reads.
- **Their characters and combat logs (part 2), three times a day.** Their own characters' progression and their finished combat logs go to their own branch of the repository, `logs-<their GitHub username>`, for discussing performance with ChatGPT and uploading instance runs to Warcraft Logs.

## What runs on Fares's Mac (so you know the whole system)

A watcher script in the game's SavedVariables folder, run by macOS (launchd), with Claude Code doing the repository work:

| When | What it does |
|---|---|
| Every save of `Auctionator.lua` | Imports the scan (`scripts/ingest.py --push`: a scan record, tests, build, commit, push) and confirms the website published it |
| 06:00, 14:00, 22:00 | Refreshes ForeverDB's public data; reads the account's own characters from `ForeverDB.lua` (`scripts/characters.py`, labels such as "Orc Warlock", never names); files finished combat logs on the repository's `logs` branch (`scripts/combat_logs.py`) |
| Before every job | Clears iCloud's duplicate "name 2.ext" files (`scripts/icloud_janitor.py`) |

It sends macOS notifications when a job finishes or fails. Fares's Mac writes to GitHub with his own account.

**This PC does less, on purpose:**
- **Scans go through the inbox,** which takes an addon's file with a **personal inbox key** and does the import on GitHub's side (`.github/workflows/inbox.yml` runs the same `ingest.py`). So this PC never writes to `main`, and never collides with the Mac's commits. Part 1 is a small PowerShell script; **no AI runs on each update**.
- **Characters and combat logs go to the co-player's own branch** with `scripts/combat_logs.py --branch logs-<username> --characters`, the same script the Mac uses. That needs their GitHub account, invited to the repository by Fares. The branch is rebuilt as one commit and force-pushed each time, so GitHub keeps no history of old logs. Per character below level 60 it keeps the last 14 days or the last 10 logs, whichever is more; level-60 characters are skipped entirely (their logs go to Warcraft Logs by hand); game logs over a week old are deleted from the game's folder only once the pushed branch has them.
- **ForeverDB's public data is refreshed by the Mac alone.** Don't run `foreverdb_data.py`, `item_names.py` or `foreverdb_api.py` here.

## Ground rules for Codex

1. **Never see, type or store the inbox key yourself.** The co-player types it into the prompt in step 4. Don't echo it, log it, paste it into a file, a command line you show, or this conversation.
2. **Send only `Auctionator.lua` through the inbox.** Everything sent there is **published** in the public repository, held submissions included. Never send `ForeverDB.lua`, `OneForAll.lua`, combat logs, screenshots or anything with a key or password in it.
3. **Write to GitHub only through `combat_logs.py`, and only to `logs-<username>`.** It refuses any other branch. Never push to `main`, never force-push anything else, never commit `ForeverDB.lua` or `OneForAll.lua`, and don't change the repository's settings.
4. **The copy of the repository in `%LOCALAPPDATA%\Tazdingo\repo` is read-only.** Don't edit or commit in it: the scripts run `git pull` on it, and a local change would stop that.
5. Keep everything in `%LOCALAPPDATA%\Tazdingo`. That folder isn't synced by OneDrive, which, like iCloud on the Mac, can make conflicting "file 2" copies.
6. Ask before anything outside these steps.

## When you're blocked: say what access you need

Fares has given you full control of the co-player's GitHub account for this work. When something stops you, **don't work around it and don't give up quietly**. Stop and tell Fares and the co-player, in plain words: what you were doing, what blocked it (with the exact message), and **exactly what they need to do or allow** so you can carry on. Then wait. For example:

- **Codex's own sandbox or approval mode** blocks the network, writing outside the workspace, or running a command: say which setting or approval to change (for example, allow network access, add `%LOCALAPPDATA%\Tazdingo` as a writable folder, or approve the command), and why.
- **A Windows prompt** (User Account Control for an install, a SmartScreen warning): say what will appear and that the co-player must click it themselves.
- **PowerShell won't run scripts** ("running scripts is disabled"): the scheduled tasks already pass `-ExecutionPolicy Bypass`. For running a script by hand, suggest `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` and ask first.
- **GitHub refuses a push** (403, "permission denied", or a sign-in window): the invitation may be unaccepted, or Git signed in as a different account. Say which, and what to click on github.com.
- **A file or folder can't be read or deleted** (the game's `Logs` folder, `SavedVariables`): say which path, and ask the co-player to check its permissions or close the game.

Never weaken security to get past a block (disable antivirus, change system-wide policies, store a password or key in plain text) without asking, and never put the inbox key anywhere but step 4's prompt.

## Before you start: what the co-player needs

- **A personal inbox key from Fares**, sent privately (not in a shared chat or project). Without it the inbox refuses the file.
- **Their realm and faction.** If they play on **CAMWOW EU5 Realm 2 PvP, Horde**, the inbox already knows that market and needs nothing more. Otherwise note it as `Realm Faction` (for example `Realm Alliance`) for step 5.
- **Their WoW account folder.** It's under `C:\Program Files (x86)\World of Warcraft\_forever_\WTF\Account\`, unless the game is installed elsewhere. If there's more than one account folder, ask which one they play on.
- **For part 2:** their GitHub account (Fares sets it up), the invitation to `faresbn/Tazdingo` accepted, and the **ForeverDB** addon installed (its file gives the characters' labels and levels).

# Part 1: Auction House scans

## Install

Run each step in **Windows PowerShell** as the co-player (not as administrator), and check its result before the next.

### 1. Tools: Python and Git

```powershell
winget install -e --id Python.Python.3.13 --accept-source-agreements --accept-package-agreements
winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements
```

Then close and reopen PowerShell, and check both: `py -3 --version` (3.12 or newer) and `git --version`. Windows 11 already includes `curl.exe`.

### 2. A read-only copy of the repository

```powershell
New-Item -ItemType Directory -Force "$env:LOCALAPPDATA\Tazdingo" | Out-Null
git clone --depth 1 https://github.com/faresbn/Tazdingo.git "$env:LOCALAPPDATA\Tazdingo\repo"
```

This needs no account. The script uses it only to read a scan's time with Tazdingo's own parser (`scripts/ingest.py`, `scripts/market_store.py`), so it reads the file exactly as the import will.

### 3. Find Auctionator's file

```powershell
Get-ChildItem "C:\Program Files (x86)\World of Warcraft\_forever_\WTF\Account\*\SavedVariables\Auctionator.lua" | Select-Object FullName, LastWriteTime
```

Pick the account the co-player plays on. Its `SavedVariables` folder (without the file name) is `$SavedVariables` in step 5. If nothing is found, the game is elsewhere or Auctionator hasn't saved yet: ask them to scan the Auction House once and `/reload`.

Check that the file parses (expect a number, the scan's time in seconds, then the market key, usually `['PvP']`):

```powershell
$f = "<the Auctionator.lua path from above>"
py -3 -c "import sys; sys.path.insert(0, r'$env:LOCALAPPDATA\Tazdingo\repo\scripts'); from pathlib import Path; import market_store, ingest; c = market_store.read_all_markets(Path(sys.argv[1])); print(ingest.scan_time(c), list(c['markets']))" $f
```

### 4. The key, typed by the co-player

Tell the co-player to run this and paste their key when asked. It's saved encrypted with Windows' own protection (DPAPI), readable only by their Windows user:

```powershell
Read-Host "Paste your Tazdingo inbox key" -AsSecureString | ConvertFrom-SecureString | Set-Content "$env:LOCALAPPDATA\Tazdingo\inbox-key.dat"
```

### 5. The script

Save this as `%LOCALAPPDATA%\Tazdingo\tazdingo-scan.ps1`. Fill in `$SavedVariables` (step 3) and `$Market` (empty on CAMWOW EU5 Realm 2 PvP Horde, otherwise `Realm Faction`):

```powershell
# tazdingo-scan.ps1: send each new Auctionator scan to the Tazdingo inbox, then report the outcome.
# Run every 2 minutes by Task Scheduler; it does nothing unless Auctionator.lua changed and holds a new scan.
$SavedVariables = 'C:\Program Files (x86)\World of Warcraft\_forever_\WTF\Account\<ACCOUNT>\SavedVariables'
$Market = ''   # '' on CAMWOW EU5 Realm 2 PvP (Horde); otherwise 'Realm Faction'

$Base     = Join-Path $env:LOCALAPPDATA 'Tazdingo'
$Repo     = Join-Path $Base 'repo'
$ScanFile = Join-Path $SavedVariables 'Auctionator.lua'
$Log      = Join-Path $Base 'update.log'
$Seen     = Join-Path $Base 'last-file-time.txt'   # the file's last write time when last looked at
$Sent     = Join-Path $Base 'last-scan.txt'        # the newest scan time already sent
$KeyFile  = Join-Path $Base 'inbox-key.dat'
$Endpoint = 'https://tazdingo-inbox.fact-special-2007.chatgpt.site/submit'
$Results  = 'https://raw.githubusercontent.com/faresbn/Tazdingo/main/inbox/results'

function Log($text) { Add-Content -Path $Log -Value ("{0:yyyy-MM-dd HH:mm:ss} {1}" -f (Get-Date), $text) }
function Notify($title, $text) {
  try {
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    $lines = $xml.GetElementsByTagName('text')
    $lines.Item(0).AppendChild($xml.CreateTextNode($title)) | Out-Null
    $lines.Item(1).AppendChild($xml.CreateTextNode($text)) | Out-Null
    $app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show([Windows.UI.Notifications.ToastNotification]::new($xml))
  } catch { Log "notification failed: $_" }
}

# One run at a time: Task Scheduler skips a run while the last one is still waiting for its result.
if (-not (Test-Path $ScanFile)) { exit 0 }
$written = (Get-Item $ScanFile).LastWriteTimeUtc
if (((Get-Date).ToUniversalTime() - $written).TotalSeconds -lt 20) { exit 0 }   # WoW may still be writing it
if ((Test-Path $Seen) -and ((Get-Content $Seen) -eq [string]$written.Ticks)) { exit 0 }   # unchanged

git -C $Repo pull -q 2>$null   # keep the parser current; a failure here is harmless
$read = "import sys; sys.path.insert(0, r'$Repo\scripts'); from pathlib import Path; import market_store, ingest; print(ingest.scan_time(market_store.read_all_markets(Path(sys.argv[1]))))"
$scan = & py -3 -c $read $ScanFile 2>&1 | Select-Object -Last 1
if ($LASTEXITCODE -ne 0) { Log "Auctionator.lua not readable: $scan"; Set-Content $Seen $written.Ticks; exit 0 }
$last = if (Test-Path $Sent) { [int64](Get-Content $Sent) } else { 0 }
if ([int64]$scan -le $last) { Log 'Auctionator.lua saved, no new scan in it'; Set-Content $Seen $written.Ticks; exit 0 }

$secure = Get-Content $KeyFile | ConvertTo-SecureString
$key = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure))
$form = @('--form-string', "key=$key", '--form-string', 'kind=lua', '-F', "file=@$ScanFile;filename=Auctionator.lua",
          '--form-string', 'message=Auction House scan from a co-player')
if ($Market) { $form += @('--form-string', "market=$Market") }
$answer = & curl.exe -sS --max-time 120 -H 'Accept: application/json' @form $Endpoint
$key = $null
try { $reply = $answer | ConvertFrom-Json } catch { $reply = $null }
if (-not $reply -or -not $reply.ok) {
  $why = if ($reply) { $reply.message } else { "no answer from the inbox ($answer)" }
  Log "not sent: $why"; Notify 'Tazdingo: scan not sent' $why
  exit 1   # not marked as seen: the next run tries again
}
$id = [regex]::Match($reply.message, 'Submission (\S+) is in').Groups[1].Value
Set-Content $Sent $scan; Set-Content $Seen $written.Ticks
Log "sent the scan of $([DateTimeOffset]::FromUnixTimeSeconds([int64]$scan).UtcDateTime) UTC as $id"

for ($i = 1; $i -le 20; $i++) {   # GitHub processes it in about two minutes
  Start-Sleep -Seconds 30
  try { $result = (Invoke-WebRequest -UseBasicParsing "$Results/$id.json?try=$i").Content | ConvertFrom-Json } catch { continue }
  if ($result.outcome -in @('applied', 'held', 'review')) {
    Log "$id $($result.outcome): $($result.detail)"
    if ($result.outcome -eq 'applied') { Notify 'Tazdingo: scan published' $result.detail }
    else { Notify "Tazdingo: scan $($result.outcome)" "$($result.detail) (Fares is told)" }
    exit 0
  }
}
Log "$id sent; no result after 10 minutes"
Notify 'Tazdingo: scan sent' "No result yet after 10 minutes: see inbox/results/$id.json in the repository"

```

How it decides: it does nothing while the file is unchanged, or while WoW may still be writing it. When the file changes, it reads the newest scan time with Tazdingo's parser and sends the file only if that's newer than the last scan it sent. **That matters:** WoW rewrites `Auctionator.lua` on every reload, scan or no scan, and the inbox keeps every file it's sent (about 0.5 MB each, in the public repository). The key is decrypted only for the request (`--form-string`, so it's never read as a file name) and never written anywhere.

### 6. Run it every two minutes

```powershell
$script = "$env:LOCALAPPDATA\Tazdingo\tazdingo-scan.ps1"
$action = New-ScheduledTaskAction -Execute 'conhost.exe' -Argument "--headless powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$script`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 2)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 20)
Register-ScheduledTask -TaskName 'Tazdingo scan' -Action $action -Trigger $trigger -Settings $settings -Description 'Sends each new Auctionator scan to the Tazdingo inbox'
```

`conhost --headless` keeps a window from flashing up every two minutes. The Mac reacts to each save at once; a two-minute check is simpler on Windows and costs nothing when the file hasn't changed.

### 7. Test it

1. Run it once by hand: `powershell -NoProfile -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\Tazdingo\tazdingo-scan.ps1"`, then read `%LOCALAPPDATA%\Tazdingo\update.log`. With a scan in the file that hasn't been sent, it sends it and waits for the result: a notification within a few minutes.
2. In the game: scan the Auction House, `/reload`, and wait up to two minutes plus the inbox's two. Expect **"Tazdingo: scan published"**.
3. `/reload` again without scanning. The log should say "no new scan in it", and nothing is sent.

# Part 2: characters and combat logs

### 8. The GitHub account and invitation

Fares sets up the co-player's GitHub account and invites it to `faresbn/Tazdingo` (on github.com: the repository's **Settings → Collaborators → Add people**). Signed in as the co-player, accept the invitation (it's emailed, and shown at https://github.com/faresbn/Tazdingo/invitations). Note the account's **username**: their branch is `logs-<username>`, in lower case (for example `logs-mikesmith`).

Set Git's name and email for this PC (use the account's private address: on github.com, **Settings → Emails**, "Keep my email addresses private" shows `<number>+<username>@users.noreply.github.com`):

```powershell
git -C "$env:LOCALAPPDATA\Tazdingo\repo" config user.name "<username>"
git -C "$env:LOCALAPPDATA\Tazdingo\repo" config user.email "<number>+<username>@users.noreply.github.com"
```

### 9. Combat logging in the game

Instance runs are only worth uploading with **advanced combat logging**: in the game, **Options → Gameplay → Network** (or System → Network) → **Advanced Combat Logging**, on. Then type `/combatlog` in chat at the start of each session; the game writes `WoWCombatLog-<date>_<time>.txt` into `_forever_\Logs`. If the co-player already uses an addon that turns logging on by itself, leave it.

### 10. The first run, by hand

```powershell
$repo = "$env:LOCALAPPDATA\Tazdingo\repo"
$game = "C:\Program Files (x86)\World of Warcraft\_forever_"            # the game folder (step 3)
$sv   = "$game\WTF\Account\<ACCOUNT>\SavedVariables"                    # as in step 5
py -3 "$repo\scripts\combat_logs.py" "$game\Logs" "$sv\ForeverDB.lua" --out "$env:LOCALAPPDATA\Tazdingo\logs-branch" --branch logs-<username> --characters --no-push
```

`--no-push` files everything into `%LOCALAPPDATA%\Tazdingo\logs-branch` without touching GitHub or deleting anything. It prints what it filed, what's still being written (a log changed in the last 30 minutes waits), and anything skipped at level 60. Look at `README.md` and `characters.md` there with the co-player: characters appear under labels like "Troll Mage", never names.

Then the same command without `--no-push`. The first time, **Git Credential Manager** opens a browser window to sign in to GitHub: sign in as the co-player's account. It creates the branch, force-pushes it, and prints `"published": "<commit>"`. Check it at https://github.com/faresbn/Tazdingo/tree/logs-<username>.

### 11. Three times a day

Save this as `%LOCALAPPDATA%\Tazdingo\tazdingo-logs.ps1`, with the same paths as step 10:

```powershell
# tazdingo-logs.ps1: file this player's characters and finished combat logs on their branch, three times a day.
$Branch = 'logs-<username>'
$Game   = 'C:\Program Files (x86)\World of Warcraft\_forever_'
$SV     = "$Game\WTF\Account\<ACCOUNT>\SavedVariables"

$Base = Join-Path $env:LOCALAPPDATA 'Tazdingo'
$Repo = Join-Path $Base 'repo'
$Log  = Join-Path $Base 'update.log'
function Log($text) { Add-Content -Path $Log -Value ("{0:yyyy-MM-dd HH:mm:ss} {1}" -f (Get-Date), $text) }
function Notify($title, $text) {
  try {
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    $lines = $xml.GetElementsByTagName('text')
    $lines.Item(0).AppendChild($xml.CreateTextNode($title)) | Out-Null
    $lines.Item(1).AppendChild($xml.CreateTextNode($text)) | Out-Null
    $app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show([Windows.UI.Notifications.ToastNotification]::new($xml))
  } catch { Log "notification failed: $_" }
}

git -C $Repo pull -q 2>$null
$output = & py -3 "$Repo\scripts\combat_logs.py" "$Game\Logs" "$SV\ForeverDB.lua" --out (Join-Path $Base 'logs-branch') --branch $Branch --characters 2>&1
$code = $LASTEXITCODE
Add-Content -Path $Log -Value $output
if ($code -eq 0) {
  $published = ($output | Select-String '"published": "([^"]+)"').Matches.Groups[1].Value
  if ($published -and $published -ne 'unchanged') { Notify 'Tazdingo: logs published' "Branch $Branch updated ($published)" }
  Log 'logs: done'
} else {
  Log 'logs: failed (see above)'
  Notify 'Tazdingo: logs not filed' 'See %LOCALAPPDATA%\Tazdingo\update.log'
}
```

Register it at the Mac's times:

```powershell
$script = "$env:LOCALAPPDATA\Tazdingo\tazdingo-logs.ps1"
$action = New-ScheduledTaskAction -Execute 'conhost.exe' -Argument "--headless powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$script`""
$triggers = @('06:00', '14:00', '22:00') | ForEach-Object { New-ScheduledTaskTrigger -Daily -At $_ }
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 1)
Register-ScheduledTask -TaskName 'Tazdingo logs' -Action $action -Trigger $triggers -Settings $settings -Description 'Files characters and combat logs on this player''s Tazdingo branch'
```

`-StartWhenAvailable` runs a missed time once the PC is on again.

### 12. Tell Fares the branch

Give Fares (or his Claude Code) the branch name. It's added to `data/game.json` as `"co_players": [{"branch": "logs-<username>"}]`, and from then on `feed/index.md`, the map ChatGPT reads first, points to the branch's `README.md` (the guide to its logs) and `characters.md`.

## What the notifications mean

| Notification | Meaning | Do |
|---|---|---|
| Scan published | The inbox applied it; the website shows it within a few minutes | Nothing |
| Scan held | A check stopped it; Fares is emailed the reason | Read the log; tell Fares if it's not obvious |
| Scan review | It needs Fares's approval | Nothing |
| Scan not sent: "The key isn't right" | The saved key is wrong or was revoked | Ask Fares for the key, repeat step 4 |
| Scan not sent: "say which market…" | The realm isn't known yet | Set `$Market` to `Realm Faction` in the script |
| Scan not sent: busy or full | The inbox's hourly limit | Nothing: the next run tries again |
| Scan not sent: no answer | No internet, or the inbox is down | Nothing: the next run tries again |
| Logs published | Their branch was updated | Nothing |
| Logs not filed | `combat_logs.py` failed: the log says why | See "When you're blocked" |

## Troubleshooting

- **Look first:** `%LOCALAPPDATA%\Tazdingo\update.log`, and Task Scheduler's "Tazdingo scan" history.
- **"Auctionator.lua not readable":** Auctionator's format may have changed. Run `git -C "$env:LOCALAPPDATA\Tazdingo\repo" pull` and repeat step 3's check. If it still fails, tell Fares, with the error but not the file.
- **No notifications:** check Windows' notification settings for Windows PowerShell; the log still records everything.
- **To send the current scan again:** delete `last-scan.txt` and `last-file-time.txt`.

## Uninstall

```powershell
Unregister-ScheduledTask -TaskName 'Tazdingo scan' -Confirm:$false
Unregister-ScheduledTask -TaskName 'Tazdingo logs' -Confirm:$false
Remove-Item -Recurse "$env:LOCALAPPDATA\Tazdingo"
```

Ask Fares to revoke the key, and to remove the branch `logs-<username>` and its line in `data/game.json`.
