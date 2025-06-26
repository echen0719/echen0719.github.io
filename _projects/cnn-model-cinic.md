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
  <label for="fileInput"><strong>Upload Image:</strong></label>
  <input type="file" name="file" accept="image/*" id="fileInput">

  <label for="imageUrl"><strong>Or Enter Image URL:</strong></label>
  <input type="text" id="imageUrl" placeholder="https://somewebsite.com/somepicture.png" style="width: 25%;">
  <button id="uploadBtn">Upload</button>

  <div id="output" style="padding: 1em 0;"></div>
  <div id="barChart"></div>
  {% include torch-model.html %}
</body>
</html>