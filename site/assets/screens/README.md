# Your own screenshots

Drop in-game screenshots here as `.webp` or `.jpg` (lowercase names with dashes, e.g. `zephras-isle-dawn.webp`).
Nothing here is published until it's listed in `data/game.json` under `"screenshots"`, with a caption:

    "screenshots": [{"file": "zephras-isle-dawn.webp", "caption": "Dawn over Zephras Isle", "page": "world/zones"}]

Before listing one, check it shows no character names, guild names or chat (hide the UI with Alt+Z before taking it).
Converting with `cwebp -q 80 in.png -o out.webp` also strips the file's metadata.
