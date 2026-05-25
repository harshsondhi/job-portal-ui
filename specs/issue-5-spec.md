# Issue #5 — Technical Specification

## Context

**Title:** Inside the footer, when hover onto the "Terms of Service" nothing being display

**State:** Closed (fix merged via commit `ca5b828` on branch `fix/term-of-service-hover-tooltip`, PR #7)

**Problem Statement:**
The footer's "Terms of Service" link had the hover background highlight div but was missing the tooltip popup that appeared on hover. The "Cookie Policy" link had already received its tooltip fix (PR #3 / commit `8fd33ef`), and the same fix needed to be applied consistently to "Terms of Service". Users hovering over the link received no contextual information about what the terms covered.

---

## Proposed Changes

### File: `src/components/Footer.jsx`

**Location:** The `<a>` element wrapping "Terms of Service" in the bottom bar (lines ~148–161 in current state).

**Change:** Added the tooltip `<div>` inside the "Terms of Service" `<a>` element, matching the identical pattern used by Privacy Policy, Cookie Policy, and (later) Contact Us.

**Before (missing tooltip — original state):**
```jsx
<a className="group relative hover:text-white transition-colors duration-300">
  <span className="relative z-10">Terms of Service</span>
  <div className="absolute inset-0 bg-gradient-to-r from-primary-600/20 to-purple-600/20 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 -inset-2"></div>
</a>
```

**After (with tooltip — fixed state):**
```jsx
<a className="group relative hover:text-white transition-colors duration-300">
  <span className="relative z-10">Terms of Service</span>
  <div className="absolute inset-0 bg-gradient-to-r from-primary-600/20 to-purple-600/20 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 -inset-2"></div>
  <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-3 w-72 bg-gray-800 border border-gray-600 text-gray-200 text-xs rounded-xl px-4 py-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none z-50 shadow-xl">
    <p className="font-semibold text-white mb-1">Terms of Service</p>
    <p>By using JobPortal, you agree to our terms governing use of the platform, including job postings, applications, and account conduct. We reserve the right to update these terms at any time.</p>
    <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-600"></div>
  </div>
</a>
```

**Tooltip content:**
- **Title:** `Terms of Service`
- **Body:** `By using JobPortal, you agree to our terms governing use of the platform, including job postings, applications, and account conduct. We reserve the right to update these terms at any time.`
- **Arrow:** CSS border-trick downward arrow pointing toward the link

**Diff summary (commit `ca5b828`):** +5 lines, 0 deletions — purely additive.

---

## Impact Assessment

- **Scope:** Single file, single component — `src/components/Footer.jsx`.
- **No breaking changes:** Purely additive — one new `<div>` inside an existing `<a>` element.
- **No new dependencies:** Uses only existing Tailwind CSS utility classes already present in sibling tooltips.
- **Consistent with existing pattern:** Tooltip markup and class names are identical to Privacy Policy and Cookie Policy tooltips; no new design tokens or variants introduced.
- **Accessibility:** `pointer-events-none` on the tooltip prevents interference with mouse events. Tooltip fades via opacity transition, same as peers.
- **Dark mode:** Uses explicit dark-bg classes (`bg-gray-800`, `text-gray-200`) — consistent with project's ThemeContext approach (no `dark:` Tailwind variant).
- **Related issues:** This is one of a series of four identical tooltip fixes across footer links — see also issue #3 (Cookie Policy), issue #6 (Privacy Policy), and issue #9 (Contact Us).

---

## Verification Plan

1. **Start dev server:** `npm run dev`
2. **Navigate to any page** that renders the `Footer` component (e.g., `/`, `/jobs`).
3. **Scroll to the bottom** to see the footer links.
4. **Hover over "Terms of Service":** Confirm the tooltip popup appears with the title "Terms of Service" and the terms summary text.
5. **Hover over the other three links** (Privacy Policy, Cookie Policy, Contact Us): Confirm their tooltips are unaffected.
6. **Check hover background highlight** on "Terms of Service": Confirm the gradient highlight appears on hover.
7. **Lint check:** `npm run lint` — should produce no new errors.
