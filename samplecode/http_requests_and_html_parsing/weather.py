"Print Chicago forecast"
import json
from urllib.request import urlopen
import time

# This URL contains grid data specifying the Chicago area
# the "LOT/76/73" part was looked up using a previous API call
# but will not change, so is hard-coded here.
url = "https://api.weather.gov/gridpoints/LOT/76,73/forecast"

time.sleep(0.5)
with urlopen(url) as fp:
    chicago_forecast_data = json.load(fp)

forecast = chicago_forecast_data["properties"]["periods"][0]

print("Current Chicago forecast: {}".format(forecast["shortForecast"]))
print()
print(forecast["detailedForecast"])
