import configparser
import os

_ini_path = os.path.join(os.path.dirname(__file__), "config.ini")

if not os.path.exists(_ini_path):
    raise FileNotFoundError(
        f"config.ini not found at {_ini_path}. "
        "Create it with [weather] latitude, longitude, units, and refresh_minutes."
    )

_cfg = configparser.ConfigParser()
_cfg.read(_ini_path)

LATITUDE: float = _cfg.getfloat("weather", "latitude")
LONGITUDE: float = _cfg.getfloat("weather", "longitude")
UNITS: str = _cfg.get("weather", "units", fallback="celsius")
WEATHER_REFRESH_MS: int = _cfg.getint("weather", "refresh_minutes", fallback=15) * 60 * 1000
