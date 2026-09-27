# Accessibility & High-DPI (PySide6)

Two areas that separate a polished Qt app from an amateur one.

## Accessibility

### Names & roles
- Every **icon-only** button and **custom** control needs a name:
  - Widgets: `btn.setAccessibleName("Save")`, `setAccessibleDescription(...)`.
  - QML: `Accessible.role: Accessible.Button; Accessible.name: "Save"`.
- A `QToolButton`/`MouseArea` with only an icon is invisible to screen readers
  without this.

### Focus & keyboard
- Keep a **visible focus indicator** (`:focus` in QSS; don't remove it).
- Logical tab order: rely on layout order, or set `setTabOrder(a, b)`.
- Standard keys work: Enter activates default button, Esc cancels dialogs, Space
  toggles checks, arrows move within lists/menus.
- Provide mnemonics: `"&File"`, `"&Save"` → Alt+F / Alt+S.

### Labels & feedback
- Inputs get a real label via buddy: `label.setBuddy(lineEdit)` (Alt+mnemonic
  focuses the field).
- Errors announced and placed near the field; don't rely on color alone — add
  icon/text.

### Contrast
- Body text ≥ 4.5:1, large text ≥ 3:1, in **both** light and dark themes.
- Don't encode meaning in color only (gain/loss, ok/error) — add arrow/icon/text.

### High-contrast / system settings
- Honor OS high-contrast mode; test that your QSS doesn't override it into an
  unreadable state.

## High-DPI (crisp at 150% / 200% / 4K)

- **Qt 6 scales automatically** — design in logical pixels/points; don't disable
  it. (Qt 5 needed `QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)`.)
- **Icons:** ship **SVG** (`QIcon(":/icons/save.svg")`) or provide `@2x`/`@3x`
  raster via the resource system so Qt picks the right one. One 16px PNG will
  blur at scale.
- **Sizes in points, not pixels:** `font.setPointSize(11)` (scales with DPI) over
  `setPixelSize`. Prefer layout-driven sizing over fixed `setFixedSize`.
- **Test** at 100%, 150%, 200% and on a 4K monitor; check a second monitor with a
  different scale factor (per-monitor DPI).
- Bundle assets and fonts via a `.qrc` resource file so paths resolve regardless
  of working directory.

## Quick checks
```
[ ] Tab through the whole screen — focus always visible, order logical
[ ] Every icon-only/custom control has an accessibleName
[ ] Run at 200% scaling — icons crisp, nothing clipped, text not truncated
[ ] Contrast verified in light AND dark
[ ] Meaning never carried by color alone
```
