# Authentic Warcraft artwork — 27 October 2026

Fares explicitly requested replacing generated scenery with authentic reusable Warcraft images, including small creatures and objects. This supersedes the old generated-only/own-captures-only policy.

## Source review

- Official Forever reveal press kit: Darkspear Islands 090, Orgrimmar new-lighting 053 and Horde camping 064. Original composition retained; delivery copies resized and encoded as WebP. The official fan-site FAQ permits limited non-commercial display, with notices; no claim of public-domain or unrestricted reuse is made.
- Original Blizzard Fan Site Kit via Internet Archive: nine transparent class renders, favouring Trolls and other Horde races. Its included licence expressly permits modification as needed to create a WoW fan site. Classic edition identified in the public credits. Licence and readme preserved alongside archive/source fingerprints.
- Blizzard public icon renderer: checked all fourteen object/creature icon URLs used or considered. Creature accents include boar and crocolisk; item accents include crates, coins, sword, potion and fishing pole.

## Implementation review

- Twelve local images total approximately 400 KB; all have source, credit, edition, original filename, dimensions, delivery treatment and SHA-256 in `data/art.json`.
- Sourced images and personal screenshots use separate publication allowlists. Unlisted files never publish from either folder. Existing raw-data privacy checks remain intact.
- Replaced homepage art/social preview, world/launch scenery, class cards/sidebars, professions/price banner artwork and world-topic icons. Retained the site's independent mark, UI design and subtle paper textures.
- Every page credits Blizzard; Sources and credits lists individual assets and distinguishes Classic from Forever. No website template or layout copied.
- Local validation: 38 Python tests (one expected skip), ten Node tests, browser script syntax, and 72-page build/link/privacy checks pass.
- No outside-model consultation: this is a reversible visual update, with source verification and direct live review. No independent review is claimed.

PR #4 merged as `86d744b27e7def276a5293bea63988da15d64fb3`; validation run 40477533297 and publish run 40477656697 succeeded. Live browser: authentic Darkspear homepage and caption verified; class hub loads all nine transparent renders with no horizontal overflow. Initial grid sizing allowed tall portraits to exceed their intended box; fixed with explicit illustration bounds. Remaining scene/credits checks follow the final small CSS publication. No phone-browser verification is claimed: this browser exposes no supported viewport-resize API.
