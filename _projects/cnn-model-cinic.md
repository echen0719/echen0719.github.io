---
layout: page
title: PyTorch CINIC-10 Model
description: description
img: assets/img/quartz.png
importance: 1
category: work
related_publications: true
---

<html>
<body>
  <div style="border-style: solid; border-width: 3px; border-radius: 5px; padding: 8px 3px 3px 5px">
    <label for="fileInput"><strong>Upload Image:</strong></label>
    <input id="fileInput" type="file" name="file" accept="image/*" id="fileInput">
    <br>
    <label for="imageUrl"><strong>Or Enter Image URL:</strong></label>
    <input type="text" id="imageUrl" placeholder="https://somewebsite.com/somepicture.png" style="width: 25%;">
    <button id="uploadBtn">Upload</button>
    <img id="preview" style="float: right; transform: scale(2.5); padding-right: 2%">
    <br>
    <label for="randImg"><strong>Or Pick Random:</strong></label>
    <button id="randImg">Random Image</button>
  </div>

  <div id="output" style="padding: 1em 0;"></div>
  <div id="barChart"></div>
  {% include torch-model.html %}
</body>
</html>