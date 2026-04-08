import gc
import secrets
import sys
import time

from machine import Pin, I2C

from lib.ahtx0 import AHT20
from lib.connect import Connect
from lib.lighting import Lighting
from lib.requester import Requester
from lib.stemma_soil_sensor import StemmaSoilSensor
from lib.germination import phases, color

wifi = Connect(
    ssid=secrets.SSID,
    password=secrets.PASSWORD,
    hostname=secrets.HOSTNAME,
)
wifi.connect()

lights = Lighting(count=secrets.PIXEL_COUNT, pin=secrets.LIGHT_PIN)
air_i2c = I2C(secrets.I2C_ID, sda=Pin(secrets.SDA_PIN), scl=Pin(secrets.SCL_PIN), freq=20000)
soil_i2c = I2C(secrets.I2C_ID, sda=Pin(secrets.SDA_PIN), scl=Pin(secrets.SCL_PIN), freq=20000)
phase_key: str = "germination"
tzo = 4
ROW_COUNT = 8
ROW_SIZE = 32
requester = Requester()

gc.enable()


def c_to_f(c_temp: float) -> float:
    return (c_temp * 9 / 5) + 32


def air() -> dict:
    temp_target = phases.get(phase_key, {}).get("temperature")
    try:
        air_sensor = AHT20(air_i2c)
        air_sensor_data = {
            "temperature": {
                "actual": c_to_f(air_sensor.temperature),
                "target": (c_to_f(temp_target[0]), c_to_f(temp_target[1])),
            },
            "humidity": {
                "actual": air_sensor.relative_humidity,
                "target": phases.get(phase_key, {}).get("humidity")
            },
        }
    except ValueError as er:
        air_sensor_data = {"error": str(er)}
    finally:
        pass

    return air_sensor_data


def soil() -> dict:
    try:
        soil_sensor = StemmaSoilSensor(soil_i2c)
        soil_sensor_data = {
            "moisture": soil_sensor.get_moisture(),
            "soil_temp": c_to_f(soil_sensor.get_temp()),
        }
    except ValueError as er:
        soil_sensor_data = {"error": str(er)}
    finally:
        pass

    return soil_sensor_data


def run_lights():
    phase_data = phases.get(phase_key)
    hours = phase_data.get("duration")
    start_hour = hours[0]
    end_hour = hours[1]

    t = time.localtime()
    adjusted_hour = (t[3] - tzo) % 24
    current_decimal = adjusted_hour + t[4] / 60.0

    noon = (start_hour + end_hour) / 2.0

    if start_hour <= current_decimal <= end_hour:
        if current_decimal <= noon:
            progress = (current_decimal - start_hour) / (noon - start_hour)
        else:
            progress = (end_hour - current_decimal) / (end_hour - noon)
        rows_lit = max(1, min(ROW_COUNT, round(progress * ROW_COUNT)))
        lights.sun_position(rows_lit, ROW_SIZE, profile=color)
    else:
        lights.turn_off()


while True:
    try:
        air_data = air()
        soil_data = soil()
        run_lights()
        data: dict = {
            "air": air_data,
            "soil": soil_data,
            "lights": lights.status,
        }

        post_path = "data/"
        _ = requester.post(path=post_path, data=data)

        get_path = f"devices/{secrets.DEVICE_ID}"
        response = requester.get(path=get_path)
        response_data = response.get("data", {})
        notes = response_data.get("notes", {})
        current_phase = notes.get("phase", "germination")

        phase_key = current_phase if current_phase != phase_key else phase_key
        phase_key = current_phase if current_phase != phase_key else phase_key
    except KeyboardInterrupt:
        print('Interrupted')
        lights.turn_off()
        try:
            sys.exit(0)
        except Exception as exc:
            raise f"System exit exception: {exc}"
    gc.collect()
    time.sleep(3600)
