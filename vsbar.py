#!/usr/bin/env python3
"""
vsbar.py — Unified bar-stats module for Waybar (vsWaybar Studio)
Outputs a visual progress bar in Waybar JSON format.

Usage:
  vsbar.py --type cpu|mem|vol|wifi [options]

Options:
  --type TYPE      Stat to display: cpu, mem, vol, wifi
  --width N        Bar segments (default: 8)
  --fill CHAR      Filled char (default: █)
  --empty CHAR     Empty char  (default: ░)
  --no-label       Omit numeric label
  --show-total     Memory: show "used/total" instead of just "used"
"""
import json, argparse, subprocess, re, time

# ── bar builder ───────────────────────────────────────────────────────────────

def make_bar(pct: int, width: int, fill: str, empty: str) -> str:
    n = round(max(0, min(100, pct)) * width / 100)
    return fill * n + empty * (width - n)

# ── data sources ──────────────────────────────────────────────────────────────

def _cpu() -> int:
    def _stat():
        with open("/proc/stat") as f:
            v = list(map(int, f.readline().split()[1:]))
        return v[3] + v[4], sum(v)
    i1, t1 = _stat()
    time.sleep(0.4)
    i2, t2 = _stat()
    dt = t2 - t1
    return int(100 - (i2 - i1) * 100 / dt) if dt else 0

def _mem():
    d = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":")
            d[k.strip()] = int(v.split()[0])
    total = d["MemTotal"]
    avail = d.get("MemAvailable",
                  d["MemFree"] + d.get("Buffers", 0) + d.get("Cached", 0))
    used  = total - avail
    pct   = int(used * 100 / total) if total else 0
    gb    = lambda kb: kb / 1024 / 1024
    return gb(used), gb(total), pct

def _vol():
    try:
        vo = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], text=True)
        mu = subprocess.check_output(["pactl", "get-sink-mute",   "@DEFAULT_SINK@"], text=True)
        m  = re.search(r"(\d+)%", vo)
        return int(m.group(1)) if m else 0, "yes" in mu
    except Exception:
        return 0, False

def _wifi():
    try:
        out = subprocess.check_output(
            ["nmcli", "-t", "-f", "ACTIVE,SIGNAL,SSID", "dev", "wifi"],
            text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            p = line.split(":")
            if p[0] == "yes" and len(p) >= 3:
                return int(p[1]) if p[1].isdigit() else 0, ":".join(p[2:]) or "WiFi"
    except Exception:
        pass
    try:
        out = subprocess.check_output(["iwconfig"], text=True, stderr=subprocess.DEVNULL)
        m = re.search(r"Link Quality=(\d+)/(\d+)", out)
        if m:
            e = re.search(r'ESSID:"([^"]+)"', out)
            return int(m.group(1)) * 100 // int(m.group(2)), e.group(1) if e else "WiFi"
    except Exception:
        pass
    return 0, ""

# ── main ─────────────────────────────────────────────────────────────────────

ap = argparse.ArgumentParser()
ap.add_argument("--type",       required=True, choices=["cpu", "mem", "vol", "wifi"])
ap.add_argument("--width",      type=int, default=8)
ap.add_argument("--fill",       default="█")
ap.add_argument("--empty",      default="░")
ap.add_argument("--no-label",   action="store_true")
ap.add_argument("--show-total", action="store_true")
args = ap.parse_args()

W, F, E = args.width, args.fill, args.empty

if args.type == "cpu":
    pct  = _cpu()
    bar  = make_bar(pct, W, F, E)
    lbl  = "" if args.no_label else f" {pct}%"
    print(json.dumps({"text": f"󰍛 {bar}{lbl}", "tooltip": f"CPU: {pct}%", "percentage": pct}))

elif args.type == "mem":
    used, total, pct = _mem()
    bar  = make_bar(pct, W, F, E)
    if args.no_label:    lbl = ""
    elif args.show_total: lbl = f" {used:.1f}G/{total:.1f}G"
    else:                lbl = f" {used:.1f}G"
    print(json.dumps({"text": f"󰾆 {bar}{lbl}",
                      "tooltip": f"RAM: {used:.1f}G / {total:.1f}G  ({pct}%)",
                      "percentage": pct}))

elif args.type == "vol":
    vol, muted = _vol()
    if muted:
        print(json.dumps({"text": "󰝟 mute", "tooltip": "Muted", "percentage": 0}))
    else:
        icon = "󰕿" if vol < 34 else "󰖀" if vol < 67 else "󰕾"
        bar  = make_bar(vol, W, F, E)
        lbl  = "" if args.no_label else f" {vol}%"
        print(json.dumps({"text": f"{icon} {bar}{lbl}", "tooltip": f"Volume: {vol}%", "percentage": vol}))

elif args.type == "wifi":
    sig, ssid = _wifi()
    if not ssid:
        print(json.dumps({"text": "󰖪 Sin red", "tooltip": "Disconnected", "percentage": 0}))
    else:
        icon = "󰖩" if sig >= 70 else "󰖧" if sig >= 40 else "󰖩"
        bar  = make_bar(sig, W, F, E)
        lbl  = "" if args.no_label else f" {sig}%"
        print(json.dumps({"text": f"{icon} {bar}{lbl}", "tooltip": f"{ssid}: {sig}%", "percentage": sig}))
