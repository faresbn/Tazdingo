# UI polish review — 27 October 2026

Scope: requested cosmetic changes and small usability fixes, preserving the current site structure.

Observed live: every navigation dropdown occupied the masthead width, generated class/profession emblems were difficult to recognise as game icons, and a pointer click could immediately close a hover-opened menu.

Changes: compact widths by menu, desktop viewport scroll limits, mobile nested menus preserved, constrained selects, classic game icons including distinct specs, teal/blue palette and lighter texture, listing-margin wording. Larger illustrations remain pending own screenshots; no copied screenshots or key art were introduced.

Validation: local unittest suite (34, one expected skip), static build/check (72 pages), Node syntax check, 48 Blizzard icon URLs returned image responses. PR check 40461894054 passed. Merged as 306ff2bf8d9a0c3b7fa29a1bb47d8139fba7d26e; deployment 40461966416 passed. Live desktop browser verified class/spec icons, click-open menus, 336px More panel, no failed game icons and no horizontal overflow on the inspected page.

Feedback: useful dashboard and consistent guide sections; longer class/guide pages need stronger summaries and visible routes to practical sections. Mobile currently hides the contents navigation. Public update history currently exposes development commit language rather than reader-facing changes. These larger changes were not folded into this cosmetic pass.

Correction from user: Beta market signals are temporary placeholders for launch. Their prominence is not treated as a hierarchy defect.
