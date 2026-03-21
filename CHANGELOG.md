# Changelog

All notable changes to vsWaybar Studio are documented here.

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
