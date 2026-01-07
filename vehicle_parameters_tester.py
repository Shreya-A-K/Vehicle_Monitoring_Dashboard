from vehicle_telemetry_generator import generate_telemetry, initial_telemetry
import time

alert_history = []  # global list to store all alerts
last_alert = {"speed": "", "engine_temp": "", "oil_quality": ""}  # track last message

def alert(level, message):
    print(f"[{level}] {message}")

def analyse(telemetry):
    issue_flag = 0
    print(f"\nTimestamp: {telemetry['timestamp']}")
    print(f"Speed: {telemetry['speed']:.1f} km/h | "
          f"Engine Temp: {telemetry['engine_temperature']:.1f} °C | "
          f"Oil Quality: {telemetry['oil_quality_index']:.1f}")

    # Speed
    if telemetry["speed"] > 110:
        msg = "SPEED IS VERY HIGH! Risk of accident or engine damage!"
        if last_alert["speed"] != msg:
            alert("CRITICAL", msg)
            last_alert["speed"] = msg
            alert_history.append((telemetry["timestamp"], "CRITICAL", msg))
        issue_flag = 1
    elif telemetry["speed"] > 90:
        msg = "Reduce speed for vehicle longevity"
        if last_alert["speed"] != msg:
            alert("WARNING", msg)
            last_alert["speed"] = msg
            alert_history.append((telemetry["timestamp"], "WARNING", msg))
        issue_flag = 1
    else:
        last_alert["speed"] = ""
        alert("INFO", "Speed is normal")

    # Engine Temperature
    if telemetry["engine_temperature"] > 115:
        msg = "ENGINE OVERHEATED! TURN OFF IMMEDIATELY!"
        if last_alert["engine_temp"] != msg:
            alert("CRITICAL", msg)
            last_alert["engine_temp"] = msg
            alert_history.append((telemetry["timestamp"], "CRITICAL", msg))
        issue_flag = 1
    elif telemetry["engine_temperature"] > 105:
        msg = "Overheating — give vehicle some rest"
        if last_alert["engine_temp"] != msg:
            alert("WARNING", msg)
            last_alert["engine_temp"] = msg
            alert_history.append((telemetry["timestamp"], "WARNING", msg))
        issue_flag = 1
    elif 95 < telemetry["engine_temperature"] <= 105:
        msg = "Engine temperature rising — slow down"
        if last_alert["engine_temp"] != msg:
            alert("INFO", msg)
            last_alert["engine_temp"] = msg
            alert_history.append((telemetry["timestamp"], "INFO", msg))
    else:
        last_alert["engine_temp"] = ""
        alert("INFO", "Engine temperature normal")

    # Oil Quality
    if telemetry["oil_quality_index"] < 50:
        msg = "Immediate service required! Oil critically degraded"
        if last_alert["oil_quality"] != msg:
            alert("CRITICAL", msg)
            last_alert["oil_quality"] = msg
            alert_history.append((telemetry["timestamp"], "CRITICAL", msg))
        issue_flag = 1
    elif telemetry["oil_quality_index"] < 70:
        msg = "Possible alcohol contamination detected"
        if last_alert["oil_quality"] != msg:
            alert("WARNING", msg)
            last_alert["oil_quality"] = msg
            alert_history.append((telemetry["timestamp"], "WARNING", msg))
        issue_flag = 1
    elif 70 <= telemetry["oil_quality_index"] < 85:
        msg = "Oil quality degrading — monitor"
        if last_alert["oil_quality"] != msg:
            alert("INFO", msg)
            last_alert["oil_quality"] = msg
            alert_history.append((telemetry["timestamp"], "INFO", msg))
    else:
        last_alert["oil_quality"] = ""
        alert("INFO", "Oil quality normal")

    if issue_flag == 0:
        print("Status: No critical alerts")

def telemetry_analyser():
    choice=input("Enter initial state or skip (A/B):")
    if choice.strip().upper()=="A":
        vehicle_id=int(input("Enter vehicle ID:"))
        speed=float(input("Enter intial speed:"))
        engine_temp=float(input("Enter the inital engine temperature:"))
        oil_quality_index=int(input("Enter the inital oil quality index:"))
        state={
            "vehicle_id":vehicle_id,
            "speed":speed,
            "engine_temperature":engine_temp,
            "oil_quality_index":oil_quality_index
        }


    else:
        state = {
            "vehicle_id": initial_telemetry["vehicle_id"],
            "speed": initial_telemetry["speed"],
            "engine_temperature": initial_telemetry["engine_temperature"],
            "oil_quality_index": initial_telemetry["oil_quality_index"]
        }
    while True:
        tel=generate_telemetry(state)
        analyse(tel)
        state=tel
        time.sleep(2)
    

