---
layout: page
title: Minecraft Server Finder v2
description: Scanner for the internet for Minecraft Servers (scanner tool below)
img: assets/img/serverfinder.png
importance: 1
category: work
related_publications: true
---

Ain't this really cool? Sometimes, you just want to meet new friends all across the world through Minecraft. Well, I gotchu since I scanned the whole internet for servers that you can join. Don't trust me? Give my implmentation a try and see who you meet (or who you grief).

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
    @import url('https://fonts.cdnfonts.com/css/minecraft-4');

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

    .scan-notes {
        font-size: 16px;
        font-weight: 400;
        color: #888;
        margin-bottom: 20px;
    }

    .stats {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
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
        <h1 style="font-family: 'Minecraft'">echen0719's Minecraft Server Finder</h1>
        <p class="scan-notes" style="text-align: center;">Scan for online servers with options <a href="#instructions-link">(click here for setup instruction)</a></p>

        <div class="stats">
            <div class="stats-box">
                <div class="stat-value" id="server-count" style="font-family: 'Minecraft'">-</div>
                <div class="stat-label">Total Minecraft Servers*</div>
            </div>

            <div class="stats-box">
                <div><a href="https://github.com/kgurchiek/Minecraft-Server-Scanner" class="stat-value" id="scan-time" style="text-decoration: none; font-family: 'Minecraft'">-</a></div>
                <div class="stat-label">Last Scan</div>
            </div>
        </div>

        <p class="scan-notes" style="margin-top: -20px; text-align: right;">*as of last scan time</p>

        {% include servers-list-fetch.html %}
        {% include servers-list.html %}
    </div>
</body>

<div id="instructions-link" style="scroll-margin-top: 60px;"><p></p></div>
### **Important Setup, Read Below:**

This is the front end of a Minecraft server pinger. It requires a backend *API*  to function. Specifically, one that returns JSON in the format of:

#### Recommended Setup

I made my own **[custom API here](https://github.com/echen0719/minecraft-server-api)** that has instructions in the README file for setting it up locally. While this isn't 100% required, it is heavily recommended since the backup API is [mcsrvstat](https://api.mcsrvstat.us/), which I do not want to flood their servers with thousands of requests. Use this 3rd party API service only when necessary, use a local API when possible. 

<p style="text-align: center; text-decoration: underline;">A quick and basic API guide: </p>

- Visit [https://github.com/echen0719/minecraft-server-api/blob/main/mcstatusPing.py](https://github.com/echen0719/minecraft-server-api/blob/main/mcstatusPing.py) and download the file.
- Install necessary Python packages by ```pip install fastapi mcstatus slowapi uvicorn```
- Run the script by ```python mcstatusPing.py --host 127.0.0.1 --port 6767 --semaphore 500 --cors --url /scan```

The default local API endpoint is set at ```127.0.0.1:6767``` but can be changed to other addresses and ports.

*Note: You might need to enable your browser to access local device endpoints so you can connect to the API.

##### API Response

My API returns a JSON in this format. If you have a custom API, make sure it also responds with a similar format:

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

In the future, I am thinking of making a more modular scanner, but that's future goals...

<p></p>
### How does this work?

From the surface, this seems to be an extremely complicated project. In many ways, it is. But it can definitely be summarized simply. So below, I will provide some form of a workflow on how this server scanner functions.

1. Normally I would have to use a port scanning tool like [masscan](https://github.com/robertdavidgraham/masscan) to scan entire IPv4 address space on different ports to find valid Minecraft servers. However, I don't have good networking avaliable so I used the IPs found by [kgurchiek's tool](https://github.com/kgurchiek/Minecraft-Server-Scanner).
2. But in order to reliably fetch the latest file off of Github, I would need to use Github's API to find the hash of the latest uploaded **[ips](https://github.com/kgurchiek/Minecraft-Server-Scanner/blob/main/ips)** file and download it. Which is exactly what I did:

    Sample of the fetching code looks like:

    ```js
    const contentFetch = await fetch(`https://api.github.com/repos/${conf.repo}/contents/${conf.path}?ref=${conf.branch}`);
    // ...

    const contentData = await contentFetch.json();
    const remoteSHA = contentData.sha
    const downloadURL = contentData.download_url
    // ...

    let commitDate = null;
    const commitsFetch = await fetch(`https://api.github.com/repos/${conf.repo}/commits?path=${conf.path}&sha=${conf.branch}&per_page=1`);
    // ...

    const commitsData = await commitsFetch.json();
    for (const commit of commitsData) {
        const commitDetails = await fetch(`https://api.github.com/repos/${conf.repo}/commits/${commit.sha}`);
        if (!commitDetails.ok) continue;

        const commitData = await commitDetails.json();
        const fileRecord = commitData.files?.find(file => file.filename === conf.path && file.sha === remoteSHA);

        if (fileRecord) {
            commitDate = commitData.commit.committer.date;
            break;
        }
    }
    // ...

    const downloadFetch = await fetch(downloadURL);
    // ...
    ```
    The website will then cache the file to the browser's indexedDB so it doesn't always have to download (unless file changes). I also made a Python equivalent using requests which can be found [here](https://github.com/echen0719/minecraft-server-api/blob/main/test/createIPJson.py).

3. The **ips** file is in a format where every 6 bytes represents a host. Each 6 bytes can be broken down into two sections: one 4 bytes and another 2 bytes. The first 4 bytes (each 8-bit) stores the IP address. The final 2 bytes (16-bit) store the port in big-endian format. So

    11000000 10101000 00000001 00000001 : 00011010 01101111 = 192 168 1 1 : 0x1A6F = 192.168.1.1:6767

    This is a really great method for storing these IPs in a compact manner.

4. Once the bytes are all read, it populates an array with elements of {ip, port}. This array is then filtered through the selection of user filters which are listed in the instructions. After a list of filtered servers is made, the browser starts pinging the servers in that list. This is also where the custom API comes in.

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

6. Finally, the browser remembers the user's preferred settings. Things like the checkboxes and input boxes values are stored to browser's ```localStorage``` which the website will restore these values next time. The **ips** file is also saved for future use in ```indexedDB```.

### Conclusion

And that's basically the whole project. There are three main pieces working together:

- Masscan + Python: Find and prepare potential Minecraft IP Addresses
- Minecraft Server API: Takes in an IP and retrieves Minecraft Server statuses
- Frontend: Downloads scan data, sends API requests, and format the data into UI.

Yes. I am looking forward to making this tool better. I would love if you could leave feedback as Github issues here: [https://github.com/echen0719/echen0719.github.io/issues](https://github.com/echen0719/echen0719.github.io/issues). Any type of feedback will be appreciated. I am thinking of hosting the API myself with more lenient limits, but I don't know yet.

Also, I am not liable for any damage or griefing that occurs on Minecraft servers with this tool. Everything you do afterwards with your results is up to you.