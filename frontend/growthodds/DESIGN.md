# Design System Strategy: Calculated Precision

## 1. Overview
This design system avoids noisy dashboard conventions and uses a restrained editorial style instead. The core principles are intentional asymmetry, strong typography contrast, and generous whitespace.

Pair a geometric display font with a highly legible body font. Use large margins and open layouts so key metrics and odds stand out without relying on dense grids or dividers.

---

## 2. Colors & Surfaces
The palette uses deep greens for emphasis, a muted red for alerts, and soft neutral surfaces for the main canvas.

*   **Primary (`#003528`) & Primary Container (`#0A4D3C`):** Use for high-impact moments and primary navigation.
*   **Secondary (`#B6171E`):** Use sparingly for alerts, negative trends, or urgent actions.
*   **Neutral Surfaces (`#F9F9F8` to `#E1E3E2`):** Use for backgrounds, sections, and tonal layering.

### No-Line Rule
Do not use 1px solid borders to define sections. Separate areas through background color shifts only.

### Surface Hierarchy
Treat the UI as layered surfaces:
*   **Level 0:** `surface` (`#f9f9f8`)
*   **Level 1:** `surface-container-low` (`#f3f4f3`)
*   **Level 2:** `surface-container-lowest` (`#ffffff`)

Use lighter inner surfaces against slightly darker parent surfaces to create depth.

### Glass & Gradient
For floating elements, use `surface-container-lowest` at 80% opacity with a `20px` backdrop blur.

Primary CTAs should use a subtle linear gradient from `primary` (`#003528`) to `primary-container` (`#0A4D3C`) at `135deg`.

---

## 3. Typography
Use a dual-font system to balance character with readability.

*   **Display & Headlines:** Use for hero metrics and section titles.
*   **Body & Labels:** Use for data points, tooltips, and supporting text.
*   **Labels:** Use tracked labels with `letter-spacing: 0.05rem` where compact UI tags need more structure.

---

## 4. Elevation & Depth
Shadows should be minimal. Depth should come primarily from tonal layering.

*   **Layering Principle:** Inner containers should be lighter than their parent.
*   **Ambient Shadows:** For floating elements, use `32px` to `48px` blur at `4%` to `6%` opacity of `on-surface` (`#191c1c`).
*   **Ghost Border:** If a visible boundary is required for accessibility, use `outline-variant` at `15%` opacity.

Avoid heavy drop shadows and fully opaque borders.

---

## 5. Components

### Buttons
*   **Primary:** Gradient fill (`primary` to `primary-container`), `12px` rounded corners, white text.
*   **Secondary:** `surface-container-high` background with `on-surface` text. No border.
*   **Tertiary:** Text-only style with `surface-container-low` on hover.

### Cards & Lists
*   Do not use horizontal divider lines.
*   Separate list items with spacing instead of borders.
*   Use a `1rem` gap between stacked items on `surface-container-lowest`.
*   For data tables, alternate tonal rows (`surface` vs `surface-container-low`) instead of using lines.

### UI Elements
*   **Badges:** Use pill shapes with `secondary-container` for low probability and `primary-fixed` for high probability.
*   **Floating overlays:** Use the glassmorphism treatment for detail views and floating actions.
*   **Chips:** Use `4px` or `8px` corners so they feel distinct from more rounded action buttons.

---

## 6. Do’s and Don’ts

### Do
*   Use `16 (5.5rem)` or `20 (7rem)` spacing for top-level margins.
*   Use asymmetric layouts to create editorial flow.
*   Keep iconography thin, around `1px` to `1.5px` stroke weight.

### Don’t
*   Do not use pure black (`#000000`); use `on-surface` (`#191c1c`) instead.
*   Do not use standard heavy shadows.
*   Do not use fully saturated reds; use `secondary` (`#B6171E`) instead.
