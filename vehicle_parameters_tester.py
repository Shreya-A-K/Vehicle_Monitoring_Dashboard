from vehicle_telemetry_generator import generate_telemetry, initial_telemetry
from flask import Flask, render_template, request

app = Flask(__name__)

alert_history = []
telemetry_history = []
last_alert = {"speed": "", "engine_temp": "", "oil_quality": ""}
current_state = None

@app.route("/parameter_entry",methods=["GET","POST"])
def set_custom_parameters():
    global current_state, telemetry_history, alert_history 
    if request.method == "POST":
            current_state = {
                "vehicle_id": int(request.form["vehicle_id"]),
                "speed": float(request.form["speed"]),
                "engine_temperature": float(request.form["engine_temperature"]),
                "oil_quality_index": int(request.form["oil_quality_index"])
            }
            return render_template("dashboard.html")



@app.route("/",methods=["GET","POST"])
def init_mode_selection():
    global current_state, telemetry_history, alert_history
    if request.method=="POST":
        mode = request.form.get("mode")
        telemetry_history.clear()
        alert_history.clear()
        if mode == "custom":
            return render_template("model_parameters.html")
        else:
            current_state = initial_telemetry.copy()
            return render_template("dashboard.html")

    return render_template("index.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    global current_state
    issue_flag=0
    # Generate ONE telemetry sample per request
    if current_state:
        tel = generate_telemetry(current_state)
        issue_flag = analyse(tel)
        current_state = tel

    return render_template(
        "dashboard.html",
        telemetry_list=telemetry_history,
        alert_history=alert_history,
        issue_flag=issue_flag
    )


def analyse(telemetry):
    global telemetry_history, last_alert
    issue_flag = 0
    telemetry_history.append(telemetry)
    telemetry_history[:] = telemetry_history[-100:]

    # SPEED
    if telemetry["speed"] > 110:
        msg = "SPEED IS VERY HIGH! Risk of accident or engine damage!"
        if last_alert["speed"] != msg:
            alert_history.append((telemetry["timestamp"], "CRITICAL", msg))
            last_alert["speed"] = msg
        issue_flag = 1

    elif telemetry["speed"] > 90:
        msg = "Reduce speed for vehicle longevity"
        if last_alert["speed"] != msg:
            alert_history.append((telemetry["timestamp"], "WARNING", msg))
            last_alert["speed"] = msg
        issue_flag = 1
    else:
        last_alert["speed"] = ""

    # ENGINE TEMPERATURE
    if telemetry["engine_temperature"] > 115:
        msg = "ENGINE OVERHEATED! TURN OFF IMMEDIATELY!"
        if last_alert["engine_temp"] != msg:
            alert_history.append((telemetry["timestamp"], "CRITICAL", msg))
            last_alert["engine_temp"] = msg
        issue_flag = 1

    elif telemetry["engine_temperature"] > 105:
        msg = "Overheating — give vehicle some rest"
        if last_alert["engine_temp"] != msg:
            alert_history.append((telemetry["timestamp"], "WARNING", msg))
            last_alert["engine_temp"] = msg
        issue_flag = 1
    else:
        last_alert["engine_temp"] = ""

    # OIL QUALITY
    if telemetry["oil_quality_index"] < 50:
        msg = "Immediate service required! Oil critically degraded"
        if last_alert["oil_quality"] != msg:
            alert_history.append((telemetry["timestamp"], "CRITICAL", msg))
            last_alert["oil_quality"] = msg
        issue_flag = 1

    elif telemetry["oil_quality_index"] < 70:
        msg = "Possible alcohol contamination detected"
        if last_alert["oil_quality"] != msg:
            alert_history.append((telemetry["timestamp"], "WARNING", msg))
            last_alert["oil_quality"] = msg
        issue_flag = 1
    else:
        last_alert["oil_quality"] = ""
    return issue_flag
