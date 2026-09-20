---
layout: page
title: Block Finder Statistics
permalink: /block-finder-statistics/
description: Statistics for my mod downloads
nav: false
nav_order: 11
chart:
  plotly: true
---

<div id="curseforgeDownloadsChart"></div>
<div id="modrinthDownloadsChart"></div>

<script>
    async function getStatistics() {
        try {
            const [curseforge, modrinth] = await Promise.all([
                fetch("https://raw.githubusercontent.com/echen0719/block-finder/refs/heads/26.2/curseforge-statistics.json"),
                fetch("https://raw.githubusercontent.com/echen0719/block-finder/refs/heads/26.2/modrinth-statistics.json")
            ]);

            if (!curseforge.ok || !modrinth.ok) {
                console.log("Could not fetch JSON data");
                return null;
            }

            return await {
                curseforge: await curseforge.json(),
                modrinth: await modrinth.json()
            };
        }
        catch {
            // something happened
            return null;
        }
    }

    async function main() {
        const json = await getStatistics();
        if (!json) {
            console.log("No JSON for some reason");
            return;
        }

        const curseforgeData = json.curseforge.queryResult.data.filter(item => item.day !== null).map(item => ({
            x: item.day,
            y: item.total
        }));
        
        const modrinthData = json.modrinth.queryResult.data.filter(item => item.day !== null).map(item => ({
            x: item.day,
            y: item.total
        }));

        console.log(curseforgeData);
        console.log(modrinthData);

        const curseforgeTrace = {
            x: curseforgeData.map(item => item.x),
            y: curseforgeData.map(item => item.y),
            type: "scatter",
            name: "CurseForge Downloads",
            line: {color: "#f16436"}
        };
        
        const modrinthTrace = {
            x: modrinthData.map(item => item.x),
            y: modrinthData.map(item => item.y),
            type: "scatter",
            name: "Modrinth Downloads",
            line: {color: "#00af5c"}
        };
        
        const layout = {
            title: "Block Finder Downloads",
            xaxis: {
                title: "Date",
                type: "date"
            },
            yaxis: {
                title: "Downloads",
                rangemode: "tozero"
            },
            hovermode: "x unified"
            };
        
        Plotly.newPlot("curseforgeDownloadsChart", [curseforgeTrace], layout, {responsive: true});
        Plotly.newPlot("modrinthDownloadsChart", [modrinthTrace], layout, {responsive: true});
    }

  main();
</script>
