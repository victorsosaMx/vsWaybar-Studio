# Changelog

All notable changes to vsWaybar Studio are documented here.

---

## [1.4.0] — 2026-04-09

### New features

- **Pill style (invert colors)** — every module form (both standard Waybar modules and custom user modules) now has a "Pill style (invert colors)" toggle switch. When enabled, the module renders with its assigned color token as a solid rounded background and `@base` as the text color — matching the inverted pill aesthetic popularized by bars like Omarchy. The border-radius follows the bar's configured `zone-radius` so it integrates naturally with all bar styles (bar / islands / modules). Live preview updates instantly on toggle.
  - Bar modules: the color token (`@peach` for CPU, `@mauve` for memory, `@green` for network, etc.) becomes the background; text uses `@base`.
  - Custom user modules: the hex color from the color picker becomes the background.
  - Dock modules: full pill support with hover state (slightly dimmed background).
  - The `_inverted` flag is persisted in `config.jsonc` and restored on reopen.

- **`vsbar.py` — unified bar-visualization script** — four new `custom/bar-*` modules (`bar-cpu`, `bar-mem`, `bar-vol`, `bar-wifi`) backed by a single script `vsbar.py` installed to `~/.config/waybar/scripts/`. The script uses `--type cpu|mem|vol|wifi` dispatch and renders a configurable fill-bar (default 8 segments, `█` / `░` characters) with percentage label. Output is Waybar JSON (`text`, `tooltip`, `percentage`). Options: `--width N`, `--fill CHAR`, `--empty CHAR`, `--no-label`, `--show-total` (memory). Each module has a dedicated form in the Modules tab with an Install button and exec presets.

### Bug fixes

- **Module colors not reflected in system Waybar** — the `_MOD_CSS_TOKENS` enforcement loop was not running for all standard modules; extended the loop and added explicit color rules for the new `custom/bar-*` modules in the modpad block. All preview colors now match the system bar.
- **`.modules-right` CSS block duplicating on every Apply** — the regex replacing the modules zone block was too narrow; extended it to also consume any trailing orphaned `.modules-right { padding-right: … }` block left by previous saves, preventing accumulation across multiple Applies.
- **`[Errno 17]` crash on second Apply** — `os.makedirs(orig_dir)` in `_backup_configs()` raised `FileExistsError` when the `backups/original/` directory already existed but was empty; fixed with `exist_ok=True`.
- **Dock user module icon wrong in preview** — dock modules whose config lives in `self._cfg` (bar user modules also added to the dock layout) were not found by the `mod in dock` check; `mod_html` now falls back to `self._cfg` for both `format` (glyph) and `_color` when the dock config dict lacks the key.
- **Dock user module color not applied in system** — `_build_save_dock_css()` only looked up `_color` in `self._dock_cfg`; it now falls back to `self._cfg` for modules shared between bar user modules and dock zones. Same fallback applied to the hover color rule.
- **Pill `color: @base` overwritten by `_MOD_CSS_TOKENS`** — the `_MOD_CSS_TOKENS` regex loop was running after the modpad block was appended and patching the pill rules' `color: @base` back to the module's token color (e.g. `@green`), making text invisible on the colored background. Pill rules are now appended after the `_MOD_CSS_TOKENS` loop so they cannot be overwritten.

---

## [1.3.1] — 2026-04-06

### Improvements

- **Full English UI** — all dialogs, labels, hints, placeholders, column headers, status messages and inline code comments that were in Spanish have been translated to English. Affected areas: dock position conflict warning, group/CFFI add dialogs, custom module icon picker, mode toggle ("Popup menu"), launcher/menu form labels and hints, menu items table columns, inline edit panel, group form (orientation, drawer, group modules), Templates tab buttons ("Preview" / "Apply") and the template status message.

---

## [1.3.0] — 2026-04-04

### New features

- **Custom module — GTK popup menu mode** — user modules in User Commands now have a mode selector: **Launcher** (previous behaviour: icon + on-click) or **Menu** (new). In Menu mode the form shows a visual item editor with Label / Command columns, `+ Item`, `─ Sep`, `↑`, `↓` and `✕` buttons, and an inline edit panel with auto-generated IDs from the label. On apply, the GtkBuilder XML is generated and written automatically to the configured path (`~/.config/waybar/{name}_menu.xml`). The saved `config.jsonc` includes `menu`, `menu-file` and `menu-actions` instead of `on-click`. The mode is persisted in config so it is restored correctly when the editor is reopened.

- **Workspaces — persistent workspaces option** — the `hyprland/workspaces` module form now includes an "Enable persistent" switch and an editable JSON field to define which workspaces should always be shown (e.g. `{"*": [1, 2, 3, 4, 5]}`). When the switch is off, `persistent-workspaces` is omitted entirely from the saved JSON (dynamic behaviour). The JSON field is visually disabled when the switch is off.

- **`group/` module support** — Waybar groups are now loaded, edited and saved correctly. The Modules tab shows a "Groups" section (always visible) with a `+ Group` button; the form lets the user define orientation, drawer settings (transition-duration, children-class, direction) and the member module list via a ComboBox populated with all available modules. Groups can be added to any Layout zone (bar and dock). Member modules that only exist inside a group receive their own config block in the saved JSON. Dock groups are loaded correctly from `config.jsonc[1]`.

- **`cffi/` module support** — CFFI modules (third-party dynamic libraries `.so`) are now loaded, edited and saved correctly. The Modules tab shows a "CFFI Modules" section with a `+ CFFI` button; the form provides a `module_path` field and a free-form JSON editor for any extra keys the library requires. CFFI modules can be added to any Layout zone (bar and dock) and are cleaned from the layout when removed.

### Improvements

- **GtkBuilder XML generation** — `_build_menu_xml()` helper generates clean, indented XML compatible with Waybar; `_parse_menu_xml()` loads existing XMLs and cross-references IDs with `menu-actions` to restore commands when the editor is reopened.
- **`justify` field on all modules** — every module form now includes a "Text align" selector (`— / left / center / right`) at the bottom. When the value is empty it is not written to JSON; when set it is serialized as `"justify": "left"` etc.

### Bug fixes

- **Dock groups not loading** — `_load_config` only scanned the bar dict (`config[0]`) for `group/` keys; it now also scans the dock dict (`config[1]`) and merges found groups into the shared `self._groups` registry.
- **Groups not written to dock dict on save** — `_build_save_config` now writes the group block and its member module config blocks to the dock dict when the group is referenced in a dock zone.
- **Removing a group did not clean the Layout** — deleting a `group/` from the Modules tab now removes it from bar and dock zones in both `self._cfg`/`self._dock_cfg` and the Layout ListStores.
- **Removing a custom module did not clean all zones** — dock apps were only removed from dock zones and user commands only from bar zones; any custom module is now removed from all zones in both bars on delete.
- **False "unrecognized modules" warning** — `_validate_layout` did not include `group/` or `cffi/` in the known-modules set; groups and CFFI modules loaded from config incorrectly triggered the warning banner even though the editor handles them correctly.

---

## [1.2.2] — 2026-03-31

### Bug fixes

- **`Gtk.FontButton.get_font_name()` deprecation warning** — replaced all 4 call sites with `get_font()`, the non-deprecated equivalent; eliminates the `DeprecationWarning` printed to stderr on GTK 3.22+

---

## [1.2.1] — 2026-03-30

### Bug fixes

- **Buttons invisible / indistinguishable** — GTK3 gradients were overriding background colors on all buttons; added `background-image: none; box-shadow: none` globally and introduced a `btn_bg` token in both THEME_DARK and THEME_LIGHT so header, open, and theme-toggle buttons have consistent, readable contrast in both editor modes
- **Page backgrounds dark in light mode** — `_scrolled()` was using `sw.add(child)` which creates an implicit `GtkViewport` with no CSS class; the implicit viewport inherited the system GTK dark theme background instead of the editor theme; fixed by creating an explicit `Gtk.Viewport` with the `page-scroll` class so all tab pages correctly follow the active editor theme
- **Alert bar text unreadable** — alert bar used hardcoded colors for the message text; changed to `{t['txt']}` so it follows the active theme
- **Template card buttons wrong colors** — template cards now attach a per-card `CssProvider` using the template's own palette colors (background, text, accent) so card buttons preview the actual template colors regardless of the active editor theme
- **Layout zone icons not showing** — zone list labels fell back to the raw module key when the module was not in `MODULE_LABELS`; added `_zone_label()` helper that looks up the `format` field from the module config chain (`cfg → _dock_cfg → _cfg`) and falls back to `󰘳` for unrecognized custom modules
- **Preview icon "vshy" for new dock modules** — the preview HTML fallback for custom modules without a `format` was slicing the module key (`mod.split("/")[-1][:4]`); changed to the generic `󰘳` glyph so new dock apps show a recognizable placeholder instead of a text fragment
- **Cannot remove custom modules or dock apps** — `_on_user_mod_remove()` rewritten: Waybar built-ins and reserved custom modules now show a dismissible warning alert instead of silently failing; user-created custom modules are removed from `_user_modules`, `self._cfg`, and all bar zone stores; dock apps are removed from `_dock_cfg` and all dock zone stores
- **Layout preview not updating after add / remove** — `_on_zone_add()` and `_on_zone_remove()` now call `_refresh_preview()` so the live preview bar reflects zone changes immediately
- **Tab build errors silent** — `_build_tab()` now wraps the builder call in a try/except and renders an inline error label if a tab fails to build, preventing the rest of the UI from being affected

---

## [1.2.0] — 2026-03-29

### Improvements

- **Lazy tab loading** — only the Bar tab is built at startup; the remaining 8 tabs are built the first time they are visited; startup time is significantly reduced on lower-end hardware
- **Sticky header** — the app header (title, Apply, Open, Export, Save as) and the live bar preview strip are now always visible regardless of scroll position; the Apply button can no longer scroll out of view

### Bug fixes

- **Labels invisible in light theme** — the system GTK theme was bleeding its own text color into the editor; added a global `label { color }` rule and `button label { color: inherit }` to guarantee correct colors in both dark and light editor modes
- **Tab content not scrollable** — placeholder boxes used for lazy loading defaulted to horizontal orientation, so inner ScrolledWindows received width but not height and could not activate vertical scrolling; fixed to vertical orientation
- **Layout tab — dock section and footer buttons not reachable** — the two expand zones (bar + dock) could exceed the available notebook height on a default-size window; the Layout tab is now wrapped in a ScrolledWindow
- **Scripts tab — Save and Load buttons not reachable** — the script editor had a fixed 340 px minimum height that pushed the button row below the window boundary; removed the minimum so the editor flexes to available space and buttons are always visible
- **Minimum window size enforced** — `set_size_request(900, 600)` prevents the window from being resized to a state where controls are inaccessible
- **Deprecated `Gdk.Screen.get_default()`** — replaced with `Gdk.Display.get_default().get_default_screen()` with a safe fallback; suppresses deprecation warnings on GTK 3.22+

---

## [1.1.0] — 2026-03-29

### New features

- **Dock support** — full second bar configuration: position, height, spacing, layer, margins, font, bar-style, opacity, zone-radius, border-width, module layout and custom dock modules; config and CSS are saved as a unified array `[bar, dock]` with proper `window#waybar` / `window#waybar.dock` CSS namespacing so both bars coexist without conflicts
- **WebKit2 live preview** — replaced the custom Cairo drawing engine with an embedded WebKit2 WebView; the preview now renders real CSS (flexbox, border-radius, rgba, keyframe animations) and accurately reflects bar-style, heights, zone padding and workspace animations
- **Bar + Dock preview** — the WebView strip shows both bars simultaneously with their real module icons
- **True center alignment in preview** — center zone is always perfectly centered regardless of left/right content width (flex:1 wrapper technique)
- **Config auto-detection at startup** — tries `config.jsonc` → `config.json` → `config` in order; uses the first one found instead of always assuming `config.jsonc`
- **Open dialog asks for both files** — the Open button now shows a single dialog with two file pickers (JSON config + CSS stylesheet), both pre-filled with current paths and browseable; supports `.json`, `.jsonc` and extensionless config files
- **`backups/original/` — first-contact backup** — the first time a save triggers a backup and `backups/original/` does not exist (or is empty), a permanent copy of the user's original `config`, `style.css` and `scripts/` is saved there; never overwritten on subsequent saves
- **Tab icons** — all notebook tabs now have Nerd Font icons
- **vsHub tab** — discover and launch the full vs ecosystem from inside the app; fetches a live tool manifest from GitHub in the background, falls back to a built-in list when offline; installed tools get a Launch button, missing ones get GitHub + AUR install buttons
- **JSONC support** — configs with `//` line comments, `/* */` block comments and trailing commas now load correctly; covers the default Waybar example config and most community-shared configs
- **Named module instances** — `battery#bat2`, `pulseaudio#microphone`, `clock#UTC` and similar are now detected, shown in the Modules tab under "Named instances", editable via the base module form, and written back to the config on save
- **Unknown module preservation** — config blocks for modules the app doesn't recognize (e.g. `mpd`, `sway/mode`, `keyboard-state`) are now preserved verbatim on save instead of being silently dropped
- **Layout validation alert** — a dismissible warning banner appears below the preview when unrecognized modules are found in the layout zones or config; lists the affected modules by name
- **Docs links** — each module form now has a "Docs ↗" button that opens the Waybar wiki page for that module

### Bug fixes

- **Double scroll at low resolutions** — removed the outer `ScrolledWindow` that wrapped the entire window; header and preview are now always visible and each tab manages its own scroll independently
- **DnD between Layout columns not working** — `set_reorderable(True)` registers `GTK_TREE_MODEL_ROW` as the preferred DnD target; when dragging between TreeViews GTK negotiated that format and `data.get_text()` always returned None; replaced with `enable_model_drag_source` + `enable_model_drag_dest` using only `text/plain`, with a unified handler for both within-zone reorder and cross-zone moves
- **vsHub "you are here" showing wrong app** — detection now compares `tool["exe"]` against `"vswaybar-studio"` locally instead of trusting the `"self"` flag from the remote JSON
- **vshypr-theme-manager themes not applying (bar going black)** — `apply_waybar()` rewritten to update `@define-color` tokens in-place via regex; vsWaybar CSS now uses `alpha(@base, X)` so a single token change propagates to all backgrounds automatically
- **Dock font-size not applying in system** — dock CSS now writes `window#waybar.dock * { font-size: Npx }` at the top of the dock block
- **`window#dock` residual selectors** — three regex patterns in `_load_dock_config()` used the old selector; fixed to `window#waybar.dock`
- **Bar height not reflected in islands/modules preview** — zone containers now get explicit `height: {bar_h - 4}px` (islands) and module pills get `height: {bar_h - 8}px` (modules)
- **`@pink` / `@cyan` undefined in hover CSS** — changed to `@mauve` / `@blue` with correct Catppuccin RGB values

---

## [1.0.2] — 2026-03-22

### Bug fixes

- **Buttons unresponsive when window is small** — all content now lives inside a root `ScrolledWindow`; Hyprland can resize the window to any size without misaligning event areas

---

## [1.0.1] — 2026-03-21

### New features

- **User Commands** — add unlimited custom launcher modules from the Modules tab: pick an icon from a curated Nerd Font glyph library (~96 glyphs), set a color, an on-click command and an optional tooltip; each module appears in the bar as a clickable icon and can be added to any zone in the Layout tab
- **`custom/settings` module** — new built-in module: gear icon that opens vsWaybar Studio on click
- **Automatic backups** — every save operation (Apply, Save as…, Save script, Save script as…) creates a timestamped backup of `config`, `style.css` and all scripts to `~/.config/waybar/backups/` using the format `YYYYMMDD_HHMMSS_filename`
- **Bar-style detection** — reopening the editor now correctly reads `bar` / `islands` / `modules` style from the existing CSS instead of defaulting to `bar`; also restores `zone-radius`, `border-width` and module colors
- **Script execute permissions** — saving a script now sets `chmod 755` automatically; previously scripts were saved without execute permission and Waybar could not run them
- **`weather.sh` bundled default** — the fallback weather script now ships as a bundled default and is shown in the Scripts tab instead of "File not found"
- **Waybar process tracking** — the editor tracks the Waybar process it started and kills only that one on restart, avoiding conflicts with other Waybar instances

### Bug fixes

- **First install** — config and CSS directories are now created automatically if they don't exist
- **Empty or missing CSS** — when `style.css` is absent or incomplete, the editor generates a full stylesheet from a built-in base template driven by the 14 color tokens
- **CSS color tokens** — missing `@define-color` tokens are injected automatically instead of being silently skipped
- **Double Waybar** — applying changes could leave two Waybar instances running simultaneously
- **Weather and clock same color** — `#custom-weather` now uses `@peach`, `#clock` uses `@blue`; enforced on every CSS write
- **Border-width always 0 on reopen** — now correctly detected from `window#waybar` (bar style) and `.modules-left` (islands/modules)
- **Default font** — changed from `Product Sans` to `JetBrainsMono Nerd Font`
- **Default palette** — out-of-the-box palette is now Catppuccin Mocha instead of Forest Night
- **User Command color persistence** — the chosen color is saved to `style.css` and restored correctly on reopen
- **User Command padding** — each user module receives the global `mod-padding` in the CSS so icons are correctly spaced
- **Deleted User Command staying in preview** — removing a User Command now also clears it from the Layout tab zone stores immediately
- **Right-side modules too close to border** — `.modules-right` now gets extra right padding so the last icon is not flush against the bar edge

---

## [1.0.0] — 2026-03-21

### Initial release

**Core editor**
- Single-file Python 3 + GTK3 application
- Reads and writes `~/.config/waybar/config` (JSON) and `~/.config/waybar/style.css`
- Live bar preview strip at the top of the window — updates on every field change
- Dark / Light editor theme toggle
- Open and Save As support for alternative config files

**Bar tab**
- Position, output/monitor, height, spacing, layer, margins
- Visual style selector: Bar / Islands / Modules
- Opacity, zone radius, border width, separators toggle
- Font family and font size

**Layout tab**
- Interactive editor for Left / Center / Right module zones
- Add, remove and reorder modules per zone
- Load defaults button

**Modules tab**
- Full module list with per-module configuration forms
- Supported modules: `hyprland/workspaces`, `hyprland/window`, `clock`, `cpu`, `memory`, `network`, `pulseaudio`, `battery`, `tray`, `custom/arch`, `custom/weather`, `custom/updates`, `custom/swaync`, `custom/power`, and more
- Clock: format combos with presets, timezone, locale, interval, on-click actions
- Workspaces: workspace animation colors, duration, button radius/padding/min-width, persistent workspaces
- custom/arch: glyph picker, icon size, color, padding

**Styling tab**
- 14 CSS color tokens with color button + hex entry per token
- Load palette from wallpaper image via matugen
- Random palette generator (dark and light modes)
- Named palette presets (Catppuccin Mocha default)

**Templates tab**
- 54 ready-made templates across 36 color palettes
- Three visual styles per palette: Bar, Islands, Modules
- Vista previa — applies template in-place without leaving the tab or scrolling
- Aplicar — writes config + CSS to disk and restarts Waybar
- Card UI showing palette background color, text colors and color swatches

**Scripts tab**
- In-place editor for `weather.py` and other custom scripts
- OpenWeatherMap integration: API key, city and units configuration

**Palettes included**
- Catppuccin Mocha, Latte, Macchiato, Frappe
- Forest Night, Forest, Forest Daylight
- Dracula, Nord, Nord Light, Gruvbox Dark, Gruvbox Light
- Tokyo Night, One Dark, Rosé Pine, Everforest, Kanagawa
- Solarized Dark, Solarized Light, Monokai, GitHub Dark
- Mario, Mario Dark, Luigi Dark, Vader
- Cyberpunk Neon, Cyberpunk Yellow, Aurora Borealis
- Carnage, Anime, Hello Kitty, Tux, Sand, Ubuntu Dark, Ice Mint, Retro Paper
