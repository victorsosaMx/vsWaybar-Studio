#!/usr/bin/env python3

import json
import os
import urllib.request
import urllib.error

CONF_PATH = os.path.expanduser("~/.config/waybar/weather.conf")

def load_conf():
    conf = {"API_KEY": "", "CITY": "Monterrey", "UNITS": "metric"}
    try:
        with open(CONF_PATH) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    conf[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return conf

def main():
    conf     = load_conf()
    api_key  = conf.get("API_KEY", "")
    city     = conf.get("CITY", "Monterrey")
    units    = conf.get("UNITS", "metric")
    deg_sym  = "°F" if units == "imperial" else "°C"

    if not api_key:
        print(json.dumps({"text": "󰖐 no key", "tooltip": "Set API_KEY in ~/.config/waybar/weather.conf"}))
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}&lang=es"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())

        temp        = round(data["main"]["temp"])
        description = data["weather"][0]["description"]
        icon_code   = data["weather"][0]["icon"]

        icons = {
            "01d": "󰖙", "01n": "󰖔",
            "02d": "󰖕", "02n": "󰼱",
            "03d": "󰖐", "03n": "󰖐",
            "04d": "󰖐", "04n": "󰖐",
            "09d": "󰖗", "09n": "󰖗",
            "10d": "󰖖", "10n": "󰖖",
            "11d": "󰙾", "11n": "󰙾",
            "13d": "󰖘", "13n": "󰖘",
            "50d": "󰖑", "50n": "󰖑",
        }
        icon = icons.get(icon_code, "󰖐")

        feels_like = round(data["main"]["feels_like"])
        temp_min   = round(data["main"]["temp_min"])
        temp_max   = round(data["main"]["temp_max"])
        humidity   = data["main"]["humidity"]
        wind_speed = round(data["wind"]["speed"] * 3.6)
        pressure   = data["main"]["pressure"]
        city_name  = data["name"]
        country    = data["sys"]["country"]

        sep = "<span size='4096'> </span>"
        tooltip = (
            f"<span size='xx-large' weight='bold'>{icon}  {temp}{deg_sym}</span>\n"
            f"<span size='large' color='#aaaaaa'>{description.capitalize()}</span>\n"
            f"<span size='small' color='#666666'>📍 {city_name}, {country}</span>\n"
            f"{sep}\n"
            f"<span color='#ffcc66'>🤔  Feels like</span>   <span weight='bold'>{feels_like}{deg_sym}</span>\n"
            f"<span color='#88ccff'>⬇️  Min</span>           <span weight='bold'>{temp_min}{deg_sym}</span>\n"
            f"<span color='#ff8888'>⬆️  Max</span>           <span weight='bold'>{temp_max}{deg_sym}</span>\n"
            f"{sep}\n"
            f"<span color='#88ddff'>💧  Humidity</span>     <span weight='bold'>{humidity}%</span>\n"
            f"<span color='#aaffaa'>💨  Wind</span>          <span weight='bold'>{wind_speed} km/h</span>\n"
            f"<span color='#ccaaff'>🔵  Pressure</span>     <span weight='bold'>{pressure} hPa</span>"
        )

        print(json.dumps({"text": f"{icon} {temp}{deg_sym}", "tooltip": tooltip}))

    except Exception as e:
        print(json.dumps({"text": "󰖐 N/A", "tooltip": str(e)}))

if __name__ == "__main__":
    main()
