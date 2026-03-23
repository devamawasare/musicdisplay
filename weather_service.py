import json
import urllib.request

from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSignal, pyqtSlot

# WMO Weather Interpretation Codes → short description
_WMO_CODES: dict[int, str] = {
    0: "Clear",
    1: "Mostly Clear", 2: "Partly Cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy Fog",
    51: "Light Drizzle", 53: "Drizzle", 55: "Heavy Drizzle",
    61: "Light Rain", 63: "Rain", 65: "Heavy Rain",
    71: "Light Snow", 73: "Snow", 75: "Heavy Snow",
    77: "Snow Grains",
    80: "Light Showers", 81: "Showers", 82: "Heavy Showers",
    85: "Snow Showers", 86: "Heavy Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm w/ Hail", 99: "Thunderstorm w/ Heavy Hail",
}

_UNIT_SYMBOL = {"celsius": "°C", "fahrenheit": "°F"}


class WeatherWorker(QObject):
    weatherFetched = pyqtSignal(str, str)
    fetchFailed = pyqtSignal()

    def __init__(self, lat: float, lon: float, units: str):
        super().__init__()
        self._lat = lat
        self._lon = lon
        self._units = units
        self._symbol = _UNIT_SYMBOL.get(units, "°C")

    @pyqtSlot()
    def fetch(self) -> None:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={self._lat}&longitude={self._lon}"
            f"&current=temperature_2m,weathercode"
            f"&temperature_unit={self._units}"
            f"&forecast_days=1"
        )
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read())
            current = data["current"]
            temp = f"{current['temperature_2m']:.0f}{self._symbol}"
            desc = _WMO_CODES.get(int(current["weathercode"]), "Unknown")
            self.weatherFetched.emit(temp, desc)
        except Exception:
            self.fetchFailed.emit()


class WeatherService(QObject):
    weatherReady = pyqtSignal(str, str)

    def __init__(self, lat: float, lon: float, units: str, refresh_ms: int):
        super().__init__()
        self._refresh_ms = refresh_ms

        self._thread = QThread()
        self._worker = WeatherWorker(lat, lon, units)
        self._worker.moveToThread(self._thread)
        self._worker.weatherFetched.connect(self.weatherReady)

        self._timer = QTimer(self)
        self._timer.setInterval(refresh_ms)
        self._timer.timeout.connect(self._trigger)

    def start(self) -> None:
        self._thread.start()
        self._timer.start()
        self._trigger()

    def stop(self) -> None:
        self._timer.stop()
        self._thread.quit()
        self._thread.wait()

    def _trigger(self) -> None:
        QTimer.singleShot(0, self._worker.fetch)
