# Review and validation log

## Author review

Three passes: source and scope comparison; consistency of source summaries with the new recommendations; rendered-copy/export and macro static checks. The last pass caught and removed an accidental literal Python-style policy line in the market HTML before publication. It also corrected a healthstone modifier interaction, an unusable in-combat ring swap and superseded official mechanics.

No outside-model consultation was run. The prescribed Claude CLI is not installed in this environment; no independent review or runtime gameplay testing is claimed.

## Checks

- 38 Python tests passed, with one expected skip for original SavedVariables files unavailable here.
- 10 Node relay/news tests passed.
- Browser JavaScript syntax passed.
- Build/site check: 72 generated HTML pages, 77 source guides, two markets; source headings, internal links and public-content privacy checks passed.
- Session checks: every content page has exactly one Tazdingo recommendation; Field findings match their pre-review bytes; macro examples stay within 255 characters; market HTML has no stray source-code policy line and the plain-text export includes the same economic limitations.
- Final publication and live checks: pending.
