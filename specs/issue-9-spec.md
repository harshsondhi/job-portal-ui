# Issue #9 — Technical Specification

## Context

**Title:** Inside the footer, when user hovers on "Contact Us" no text is being displayed

**State:** Closed (fix merged via PR from branch `claude/issue-9-20260524-1412`)

**Problem Statement:**
The footer contained four bottom links: Privacy Policy, Terms of Service, Cookie Policy, and Contact Us. The first three each displayed a tooltip popup on hover, explaining their purpose. The "Contact Us" link was missing this tooltip entirely. Users hovering over "Contact Us" received no contextual help text explaining where the link leads or what they can do there.

The "Contact Us" link also differed structurally — it used a `<Link>` (router navigation) rather than a plain `<a>`, because it navigates to `/contact` where users can send messages to the admin team.

---

## Proposed Changes

### File: `src/components/Footer.jsx`

**Location:** Lines 171–182 (post-fix state)

**Change:** Added a hover tooltip `<div>` to the "Contact Us" `<Link>` element, matching the identical pattern used by Privacy Policy, Terms of Service, and Cookie Policy.

The tooltip structure pattern used across all four links:

```jsx
<div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-3 w-72 bg-gray-800 border border-gray-600 text-gray-200 text-xs rounded-xl px-4 py-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none z-50 shadow-xl">
  <p className="font-semibold text-white mb-1">{Title}</p>
  <p>{Description}</p>
  <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-600"></div>
</div>
```

**Tooltip content added to "Contact Us":**
- **Title:** `Contact Us`
- **Body:** `Have a question or facing an issue? Send a message to our admin team and we'll get back to you as soon as possible.`
- **Arrow:** CSS border-trick arrow pointing downward toward the link

**Before (missing tooltip):**
```jsx
<Link
  to="/contact"
  className="group relative hover:text-white transition-colors duration-300"
>
  <span className="relative z-10">Contact Us</span>
  <div className="absolute inset-0 bg-gradient-to-r from-primary-600/20 to-purple-600/20 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 -inset-2"></div>
</Link>
```

**After (with tooltip):**
```jsx
<Link
  to="/contact"
  className="group relative hover:text-white transition-colors duration-300"
>
  <span className="relative z-10">Contact Us</span>
  <div className="absolute inset-0 bg-gradient-to-r from-primary-600/20 to-purple-600/20 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 -inset-2"></div>
  <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-3 w-72 bg-gray-800 border border-gray-600 text-gray-200 text-xs rounded-xl px-4 py-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none z-50 shadow-xl">
    <p className="font-semibold text-white mb-1">Contact Us</p>
    <p>Have a question or facing an issue? Send a message to our admin team and we&apos;ll get back to you as soon as possible.</p>
    <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-600"></div>
  </div>
</Link>
```

---

## Impact Assessment

- **Scope:** Single file, single component — `src/components/Footer.jsx`.
- **No breaking changes:** Purely additive — a `<div>` inside an existing element.
- **No new dependencies:** Uses only existing Tailwind CSS utility classes.
- **Consistent with existing pattern:** The tooltip markup and class names are identical to the three other footer links, so no new design tokens or variants were introduced.
- **Accessibility:** `pointer-events-none` on the tooltip prevents it from interfering with mouse events. The tooltip fades in/out via opacity transition, same as peers.
- **Dark mode:** The component uses explicit dark-bg classes (`bg-gray-800`, `text-gray-200`, etc.), consistent with project dark-mode approach (ThemeContext toggling, no `dark:` Tailwind variant).

---

## Verification Plan

1. **Start dev server:** `npm run dev`
2. **Navigate to any page** that renders the `Footer` component (e.g., `/`, `/jobs`).
3. **Scroll to the bottom** to see the footer links.
4. **Hover over "Contact Us":** Confirm the tooltip popup appears with the title "Contact Us" and the help message.
5. **Hover over the other three links** (Privacy Policy, Terms of Service, Cookie Policy): Confirm their tooltips are unaffected.
6. **Click "Contact Us":** Confirm it navigates to `/contact`.
7. **Check hover background highlight** on "Contact Us": Confirm the gradient highlight appears on hover (same as peers).
8. **Lint check:** `npm run lint` — should produce no new errors.
