---
layout: page
title: Minecraft Server Finder
description: Scanner for the whole internet to find online Minecraft servers each week
img: assets/img/serverfinder.png
importance: 2
category: work
related_publications: true
---

Ain't this really cool? Sometimes, you just want to meet new friends all across the world through Minecraft. Well, I gotchu since I scanned the whole internet for servers that you can join. Don't trust me? Give my implmentation a try and see who you meet (or who you grief).

### **Important Information, Read Below:**

This is the front end of a Minecraft server pinger. It requires a backend to function. Specifically, an *API* that returns JSON in the format of:

```json
{
    "online": "true/false",
    "motd": {
        "html": "HTML format of MOTD",
        "clean": "Plain format of MOTD"
    },
    "version": "Version info",
    "protocol": "Version protocol",
    "players": {
        "online": "Players currently online",
        "max": "Maximum player count"
    },
    "icon": "Server Favicon",
}
```

To save you some time, I made my own [custom api here](https://github.com/echen0719/minecraft-server-api) that has instructions on how to setup and run as a local endpoint. While this isn't 100% required, it is heavily recommended since the backup API is [mcsrvstat](https://api.mcsrvstat.us/), which I do not want to flood their servers with thousands of requests. Use this 3rd party API service only when necessary, use a local API when possible. The default local api endpoint is set at ```127.0.0.1:6767``` but can be changed.

<style>
    .mc-finder {
        font-family: "Roboto", sans-serif;
        background: #181818;
        padding: 40px 20px;
        border-radius: 10px;
        color: #eee;
        max-width: 1000px;
        margin: 0 auto;
    }

    .mc-finder h1 {
        text-align: center;
        font-size: 32px;
        font-weight: 600;
        color: limegreen;
        margin-bottom: 10px;
    }

    .mc-finder p {
        font-size: 16px;
        font-weight: 400;
        color: #888;
        margin-bottom: 20px;
    }

    .scan-footnote {
        text-align: right;
        font-size: 12px;
        font-weight: 400;
        color: #eee;
        margin-top: -20px;
    }

    .stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        justify-items: center;
        align-items: center;
        margin-bottom: 40px;
    }

    .stats-box {
        background: darkslategray;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid steelblue;
        width: 100%;
        min-width: 200px;
    }

    .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: limegreen;
        margin-bottom: 8px;
    }

    .stat-label {
        font-size: 12px;
        font-weight: 400;
        color: lightgray;
        letter-spacing: 1px;
    }
</style>
<body>
    <div class="mc-finder">
        <h1>Minecraft Server Finder</h1>
        <p style="text-align: center;">Scan for online servers on port 25565</p>

        <div class="stats">
            <div class="stats-box">
                <div class="stat-value" id="server-count">-</div>
                <div class="stat-label">Total Scanned Servers*</div>
            </div>

            <div class="stats-box">
                <div class="stat-value" id="player-count">-</div>
                <div class="stat-label">Estimated Online Servers*</div>
            </div>

            <div class="stats-box">
                <div class="stat-value" id="scan-time">-</div>
                <div class="stat-label">Last Scan</div>
            </div>
        </div>

        <p class="scan-footnote">*as of last scan time</p>

        {% include servers-list.html %}
    </div>
</body>

<p></p>
### **How does this work?**