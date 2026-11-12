# Tazdingo's automatic updates on a co-player's Windows PC: instructions for Codex

**Reader:** Codex (CLI or desktop app) on a co-player's Windows 11 Home PC, working with that co-player. They have no GitHub account. Read this whole file before doing anything, then do the install steps with them, one at a time, and stop to ask whenever a step needs their answer or their hands.

**Address of this file:** https://raw.githubusercontent.com/faresbn/Tazdingo/main/docs/chatgpt/MIKE_CODEX_WOW_SCRIPTS.md (the repository is public: reading it needs no account).

## What this gives the co-player

After every Auction House scan in World of Warcraft: Forever, when they `/reload` or log out, their PC sends the scan to Tazdingo by itself. A few minutes later it shows a Windows notification saying the prices are published, or why not. Their scans then sit in the same price history as Fares's (one market per realm and faction) on https://faresbn.github.io/Tazdingo/ and in the feed ChatGPT reads.

## What runs on Fares's Mac (so you know the whole system)

A watcher script in the game's SavedVariables folder, run by macOS (launchd), with Claude Code doing the repository work:

| When | What it does |
|---|---|
| Every save of `Auctionator.lua` | Imports the scan (`scripts/ingest.py --push`: a scan record, tests, build, commit, push) and confirms the website published it |
| 06:00, 14:00, 22:00 | Refreshes ForeverDB's public data; reads the account's own characters from `ForeverDB.lua` (`scripts/characters.py`, labels such as "Orc Warlock", never names); files finished combat logs on the repository's `logs` branch (`scripts/combat_logs.py`) |
| Before every job | Clears iCloud's duplicate "name 2.ext" files (`scripts/icloud_janitor.py`) |

It sends macOS notifications when a job finishes or fails. Fares's Mac writes to GitHub with his own account.

**Why this PC needs much less:** the co-player has no GitHub account, so their PC can't write to the repository. Tazdingo has a route for exactly that: the **inbox**, which takes an addon's file with a **personal inbox key** and does the import on GitHub's side (`.github/workflows/inbox.yml` runs the same `ingest.py`). So this PC only has to notice a new scan and send the file. That's a small PowerShell script; **no AI runs on each update**, and Codex is only needed to install and troubleshoot it.

## What this PC can and can't do yet

| Capability | On this PC | Why |
|---|---|---|
| Auction House scans, automatically | **Yes** (this file) | The inbox takes `Auctionator.lua` with a personal key, no account needed |
| Characters' progression (`ForeverDB.lua`) | **Not yet** | The inbox publishes what it receives exactly as sent, and `ForeverDB.lua` holds other players' names. It must be reduced to our own characters first (as `characters.py` does on the Mac), and the repository's character file is written for one account only. |
| Combat logs | **Not yet** | They're too big for the inbox (25 MB per file, `.lua` only), and the logs branch is rebuilt by one machine at a time. |

Fares decides how to add the last two. Don't improvise a route for them, and don't send either file through the inbox.

## Ground rules for Codex

1. **Never see, type or store the inbox key yourself.** The co-player types it into the prompt in step 4. Don't echo it, log it, paste it into a file, a command line you show, or this conversation.
2. **Send only `Auctionator.lua` through the inbox.** Everything sent there is **published** in the public repository, held submissions included. Never send `ForeverDB.lua`, `OneForAll.lua`, combat logs, screenshots or anything with a key or password in it.
3. **The copy of the repository on this PC is read-only.** Don't commit or push from it, and don't edit its files: the script runs `git pull` on it before each check, and any local change would stop that.
4. Keep everything in `%LOCALAPPDATA%\Tazdingo`. That folder isn't synced by OneDrive, which, like iCloud on the Mac, can make conflicting "file 2" copies.
5. Ask before anything outside these steps.

## Before you start: what the co-player needs

- **A personal inbox key from Fares**, sent privately (not in a shared chat or project). Without it the inbox refuses the file.
- **Their realm and faction.** If they play on **CAMWOW EU5 Realm 2 PvP, Horde**, the inbox already knows that market and needs nothing more. Otherwise note it as `Realm Faction` (for example `Realm Alliance`) for step 5.
- **Their WoW account folder.** It's under `C:\Program Files (x86)\World of Warcraft\_forever_\WTF\Account\`, unless the game is installed elsewhere. If there's more than one account folder, ask which one they play on.

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

## Troubleshooting

- **Look first:** `%LOCALAPPDATA%\Tazdingo\update.log`, and Task Scheduler's "Tazdingo scan" history.
- **"Auctionator.lua not readable":** Auctionator's format may have changed. Run `git -C "$env:LOCALAPPDATA\Tazdingo\repo" pull` and repeat step 3's check. If it still fails, tell Fares, with the error but not the file.
- **No notifications:** check Windows' notification settings for Windows PowerShell; the log still records everything.
- **To send the current scan again:** delete `last-scan.txt` and `last-file-time.txt`.

## Uninstall

```powershell
Unregister-ScheduledTask -TaskName 'Tazdingo scan' -Confirm:$false
Remove-Item -Recurse "$env:LOCALAPPDATA\Tazdingo"
```

Ask Fares to revoke the key too.
