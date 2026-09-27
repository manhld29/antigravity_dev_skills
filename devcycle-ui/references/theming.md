# Theming & dark mode (PySide6)

One source of truth for colors; apply it consistently; support light + dark.

## Principle
Define **semantic tokens** (accent, surface, text, border, danger…) once, then
derive both the QSS/QPalette (Widgets) or the QML singleton (QML). Never scatter
raw hex across widgets/screens.

## Widgets (QSS + QPalette)
- Set **QPalette and QSS together, before `show()`** — otherwise a light palette
  flashes before the stylesheet loads, and some native sub-bits stay light.
- Use the `Fusion` base style; it honors `QPalette` cleanly across platforms.
- See [qss-reference.md](qss-reference.md) for a `dark_palette()` + token QSS.

Switching theme at runtime:
```python
def apply_theme(app, tokens, palette):
    app.setPalette(palette)
    app.setStyleSheet(build_qss(tokens))   # re-format the QSS template
# call on a Light/Dark toggle; widgets restyle live
```

## QML (Material/Universal + singleton)
- `Material.theme: Material.Dark` (or `Material.System` to follow the OS).
- Put tokens in `Theme.qml` (singleton); bind `color: Theme.surface` everywhere.
- Runtime switch = change the singleton's property values (or a `dark` bool that
  selects token sets); bindings update automatically.

## Follow the OS theme (optional)
- Qt 6.5+: `QStyleHints.colorScheme()` and the `colorSchemeChanged` signal tell
  you Light/Dark; map it to your token set.
- QML Material: `Material.theme: Material.System` does this for you.

## Dark-mode rules (from the UX guidelines)
- Don't invert colors — use desaturated/lighter tonal variants for dark.
- Verify contrast **separately** for dark (text ≥4.5:1, secondary ≥3:1).
- Keep borders/dividers and interaction states visible in **both** themes.
- Test both themes before delivery; never infer one from the other.

## Anti-patterns
- Hardcoded hex in individual widgets/dialogs → breaks theming. Tokenize.
- QSS-only dark mode (palette left light) → white flashes + light native bits.
- Light-only design shipped with a half-working dark mode.
