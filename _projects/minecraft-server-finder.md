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

This is the front end of a Minecraft server pinger. It requires a backend *API*  to function. Specifically, one that returns JSON in the format of:

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

To save you some time, I made my own [custom API here](https://github.com/echen0719/minecraft-server-api) that has instructions on how to setup and run as a local endpoint. While this isn't 100% required, it is heavily recommended since the backup API is [mcsrvstat](https://api.mcsrvstat.us/), which I do not want to flood their servers with thousands of requests. Use this 3rd party API service only when necessary, use a local API when possible. The default local API endpoint is set at ```127.0.0.1:6767``` but can be changed to other addresses and ports.

Note: You might need to enable your browser to access local device endpoints so you can connect to your hosted API.

### Instructions

- Check "Custom API" to be true and enter your API endpoint into the input box with the placeholder "Custom api address..."
- Enter the number of workers (threads) into the second input box with the placeholder "Specify number of workers..."
- Check any other options you want to enable such as "Show Offline", "Have Players?", or "Randomizer"
- Click the start button to start scanning. Preferrably open up your browser's network debug tool with Ctrl+Shift+I --> Network.
- Click the stop button to stop the scan at any time. Results will be shown below this menu.

<table style="width: 100%; border-collapse: collapse; text-align: center;">
    <thead>
        <tr style="background-color: #f2f2f2;">
            <th style="border: 1px solid #ddd; padding: 8px;">Show Offline</th>
            <th style="border: 1px solid #ddd; padding: 8px;">Have Players?</th>
            <th style="border: 1px solid #ddd; padding: 8px;">Randomizer</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">Servers that do not respond are shown. They could still be valid Minecraft servers but likely not.</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Filters servers that have at least one player. </td>
            <td style="border: 1px solid #ddd; padding: 8px;">Scans can be done sequentially or in random order. Random order is better.</td>
        </tr>
    </tbody>
</table>
<p></p>

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

        {% include servers-list-fetch.html %}
        {% include servers-list.html %}
    </div>
</body>

<p></p>
### How does this work?

From the surface, this seems to be an extremely complicated project. In many ways, it is. But it can definitely be summarized simply. So below, I will provide some form of a workflow on how this server scanner functions.

1. Gather valid IP addresses that respond to port 25565: Using [masscan](https://github.com/robertdavidgraham/masscan), the entire IPv4 address space was scanned on port 25565 and results were saved as a JSON file.
2. This JSON output, with around ~2.1 million addresses is formatted uniformly and cleaned with [Python scripts](https://github.com/echen0719/minecraft-server-api) and then compressed into a ZIP file, uploaded to this static website.

    Sample of the output looks like:

    ```json
    [{"ip": "135.x.34.227", "port": 25565, "timestamp": "1782503645"},
    {"ip": "43.169.x.121", "port": 25565, "timestamp": "1782503645"},
    {"ip": "8.x.201.78", "port": 25565, "timestamp": "1782503645"}]
    ```

3. Now, the fun part on the front end begins.

    The website loads a manifest file located [here](https://echen0719.github.io/assets/minecraftscans/scans.json) which has information on how many addresses were found by masscan, the estimated number of valid Minecraft servers, the date of the scan, and most importantly, which ZIP file to download.

    Obviously, with something being ~23 MB in size, it would be logical to store the giant file in the browser's cache storage. Once downloaded, this file can be reused without redownloading. Once the ZIP file is downloaded, [JSZip](http://jszip.org/) extracts the archive and then is parsed into JSON.

4. Once the scan JSON data is loaded, it is filtered through the selection of user filters which are listed in the instructions. After a list of filtered servers is made, the browser starts pinging the servers in that list. This is also where the custom API comes in.

    Browsers can't directly create raw TCP requests to ping Minecraft servers and receive their response (at least not static websites like this one). Instead, the browser sends a HTTP request to the API which handles the Minecraft server status and reply back to the browser.

    More specifically, the API primarily gets the online status, MOTD, version, player count/max, and favicon using [mcstatus](https://mcstatus.io/). The source code for the simple API is [here](https://github.com/echen0719/minecraft-server-api). 

    ```python
    from mcstatus import JavaServer, LegacyServer # actual Minecraft ping libraries

    from fastapi import FastAPI, HTTPException, Request, status # for browser to API actual processing
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware # CORS for static website purposes
    ```

    This step is also done by multiple workers since waiting for one server to finish before checking the next one would be painfully slow. Using workers solves this sequential problem. If the worker count is set to 10, the browser creates 10 asynchronous ping processes.

    In the case that the local API doesn't respond, it has a backup to use [https://api.mcsrvstat.us/3/](https://api.mcsrvstat.us/3) as an endpoint.

5. The website processes the receives JSON data from the APIs, parses it, and then calls renders the results on screen. If the server is deemed valid and online, it will populate the server list in a "bubble-up form" where it rises to the top of the list once other offline servers around it are scanned and hidden. Note that this behavior only applies when "Show Offline" is disabled. Each valid server is displayed with its IP, version, favicon, player count/max, and a "View Raw JSON" button.

    This is the main logic that does the rendering (and parsing):
    ```js
    if (status.online) {
        if (status.icon) {
            iconHtml = `<img src="${status.icon}" class="server-icon" alt="icon">`;
        }
        else {
            iconHtml = `<img src="/assets/img/pack.png" class="server-icon" alt="icon">`;
        }

        let motd = 'No MOTD provided';
        if (status.motd) {
            if (Array.isArray(status.motd.html)) {
                motd = status.motd.html.join('<br>');
            }
            else if (typeof status.motd.html === 'string') {
                motd = status.motd.html;
            }
            else if (Array.isArray(status.motd.clean)) {
                motd = status.motd.clean.join('<br>');
            }
            else if (typeof status.motd.clean === 'string') {
                motd = status.motd.clean;
            }
        }

        const currentPlayers = status.players?.online || 0;
        const maxPlayers = status.players?.max || 0;
        const gameVersion = status.version || "Unknown";

        detailsHtml = `
            <div>
                <strong style="color: #eee;">${key}</strong> <span style="color: lime;">[Online]</span><br>
                <span style="color: #eee;">Version: ${gameVersion}</span><br>
                <span style="color: #eee;">Players: ${currentPlayers}/${maxPlayers}</span><br>
                <div style="margin-top: 5px; font-family: monospace; background: #1a1a1a; padding: 4px; border-radius: 4px;">${motd}</div>
            </div>
        `;
    }
    ```

6. Finally, the browser remembers the user's preferred settings. Things like the checkboxes and input boxes values are stored to browser's ```localStorage``` which the website will restore these values next time.

### Conclusion

And that's basically the whole project. There are three main pieces working together:

- Masscan + Python: Find and prepare potential Minecraft IP Addresses
- Minecraft Server API: Takes in an IP and retrieves Minecraft Server statuses
- Frontend: Downloads scan data, sends API requests, and format the data into UI.

Yes. I am looking forward to making this tool better. I would love if you could leave feedback as Github issues here: [https://github.com/echen0719/echen0719.github.io/issues](https://github.com/echen0719/echen0719.github.io/issues). Any type of feedback will be appreciated.

Also, I am not liable for any damage or griefing that occurs on Minecraft servers with this tool. Everything you do afterwards with your results is up to you.