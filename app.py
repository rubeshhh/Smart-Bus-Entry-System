from flask import Flask, render_template, request, send_file
import csv
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "bus_entries.csv")

# 🚍 Bus Route Mapping
bus_routes = {
    "TN45AB1234": "Sivakasi Bus Stand → College",
    "TN10CD5678": "Satchyapuram → College",
    "TN22EF9999": "Virudhunagar → College",
    "TN33GH0000": "Sithrajapuram → College",
    "TN55IJ1111": "ByPass → College",
    "TN66KL2222": "Thiruthangal → College",
    "TN77MN3333": "Madurai → College"
}


def read_entries():
    entries = []
    try:
        with open(csv_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                bus_no = row[0]
                route = bus_routes.get(bus_no, "Unknown Route")
                entries.append([bus_no, route, row[1], row[2]])
    except:
        pass
    return entries


@app.route("/")
def index():
    month_filter = request.args.get("month")
    entries = read_entries()

    if month_filter:
        entries = [
            e for e in entries
            if datetime.strptime(e[2], "%Y-%m-%d").strftime("%Y-%m") == month_filter
        ]

    total_buses = len(entries)

    return render_template("index.html",
                           entries=entries,
                           total_buses=total_buses,
                           selected_month=month_filter)


@app.route("/download")
def download():
    return send_file(csv_path,
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="bus_report.csv")


if __name__ == "__main__":
    app.run()