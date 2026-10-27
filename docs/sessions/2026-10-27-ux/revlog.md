# Focused UX pass — 27 October 2026

Requested: remove Latest in Tazdingo from the homepage and tighten useful UI details across the site.

## Findings and changes

- Homepage repository commit messages are developer-facing and occupy a useful column. Removed that card and its rendering; class picker spans the row. Individual page histories remain. News gets a wider desktop column; temporary Beta content remains in place.
- Search suggestions lacked arrow-key traversal, Escape/outside/focus dismissal, an empty state and stale-request handling. Added those. Exact submissions still navigate; partial submissions expose/focus suggestions rather than unexpectedly sending guide queries into the market. An unavailable search index retains native item-price fallback.
- Market dropdowns used long options and inconsistent sizing. Shortened labels, aligned controls, added Reset, and preserved query/scope/order in shareable URLs. Narrow screens stack controls; input text remains at least 16px to avoid forced phone zoom.
- More pages never marked their top-level section active because its landing URL differs from the section key. Fixed it, and reserve aria-current=page for the actual landing page. Breadcrumbs now use a labelled navigation landmark. Keyboard menus dismiss on leaving the group.
- Phone article sidebars placed a long tools list before the content and hid the contents links. The same content now sits in one native disclosure above the article on narrow screens; open by default on desktop, still available without scripts. Desktop sidebars scroll within the viewport rather than hiding their lower links.
- News refresh now visibly says Checking… while busy, rather than only fading the button. A global hidden rule prevents component display styles from overriding the hidden attribute.

## Review and verification

Source review of templates, CSS and browser behaviour. No outside-model consultation: changes are bounded and reversible, and direct interaction checks are more useful for these issues. No independent review is claimed. Existing privacy, provenance, market arithmetic and news classifier boundaries are unchanged.

Local validation and GitHub/live interaction results recorded at completion.
