import os
import requests
import plotly.graph_objects
from plotly.graph_objects import Scatter, Layout, Figure

def getStatistics():
    curseforge = requests.get("https://raw.githubusercontent.com/echen0719/block-finder/refs/heads/26.2/curseforge-statistics.json", timeout=10)
    modrinth = requests.get("https://raw.githubusercontent.com/echen0719/block-finder/refs/heads/26.2/modrinth-statistics.json", timeout=10)

    curseforge.raise_for_status()
    modrinth.raise_for_status()

    return {
        "curseforge": curseforge.json(),
        "modrinth": modrinth.json()
    }

def main():
    json = getStatistics()

    if not json:
        print("No JSON information")
        return

    curseforgeData = [
        {"x": item["day"], "y": item["total"]}
        for item in json["curseforge"]["queryResult"]["data"]
    ]

    modrinthData = [
        {"x": item["day"], "y": item["total"]}
        for item in json["modrinth"]["queryResult"]["data"]
    ]

    curseforgeTrace = Scatter(
        x=[item["x"] for item in curseforgeData],
        y=[item["y"] for item in curseforgeData],
        mode="lines+markers+text",
        name="CurseForge Downloads",
        line={"color": "#f16436", "width": 4},
        text=[item["y"] for item in curseforgeData],
        textposition="top center"
    )

    modrinthTrace = Scatter(
        x=[item["x"] for item in modrinthData],
        y=[item["y"] for item in modrinthData],
        mode="lines+markers+text",
        name="Modrinth Downloads",
        line={"color": "#00af5c", "width": 4},
        text=[item["y"] for item in modrinthData],
        textposition="top center"
    )

    layout = Layout(
        xaxis={
            "title": "Date",
            "type": "date",
        },
        yaxis={
            "title": "Downloads",
            "rangemode": "tozero",
            "dtick": 10
        },
        hovermode="x unified"
    )

    curseforgeFig = Figure(data=[curseforgeTrace], layout=layout)
    modrinthFig = Figure(data=[modrinthTrace], layout=layout)

    curseforgeOutput = "assets/img/block-finder-statistics/block-finder-curseforge-downloads.png"
    os.makedirs(os.path.dirname(curseforgeOutput), exist_ok=True)

    modrinthOutput = "assets/img/block-finder-statistics/block-finder-modrinth-downloads.png"
    os.makedirs(os.path.dirname(modrinthOutput), exist_ok=True)

    curseforgeFig.write_image(curseforgeOutput, width=1600, height=900, scale=2)
    modrinthFig.write_image(modrinthOutput, width=1600, height=900, scale=2)

if __name__ == "__main__":
    main()