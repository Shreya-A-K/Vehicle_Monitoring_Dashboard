import random
from datetime import datetime


def generate_speed(prev_speed):
    change = random.uniform(-5, 8)
    speed = prev_speed + change
    return max(0, min(speed, 130))

def generate_oil_quality_index(prev_quality):
    degradation = random.uniform(0.01, 0.05)
    quality = prev_quality - degradation

    # Rare contamination event
    if random.random() < 0.002:
        quality -= random.uniform(10, 20)

    return max(0, quality)


def generate_timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d-%H:%M:%S")

def generate_engine_temp(speed, prev_temp):
    if speed > 80:
        temp_change = random.uniform(0.5, 1.5)
    else:
        temp_change = random.uniform(-0.3, 0.6)

    temp = prev_temp + temp_change
    return max(60, min(temp, 125))

def generate_telemetry(tel):
    new_speed=generate_speed(tel["speed"])
    telemetry={"vehicle_id":tel["vehicle_id"],
               "timestamp": generate_timestamp(),
               "speed":new_speed,
               "engine_temperature":generate_engine_temp(new_speed,tel["engine_temperature"]),
               "oil_quality_index":generate_oil_quality_index(tel["oil_quality_index"])
               }
    return telemetry

initial_telemetry = {
    "vehicle_id": 1,
    "speed": 40,
    "engine_temperature": 75,
    "oil_quality_index": 100
}


