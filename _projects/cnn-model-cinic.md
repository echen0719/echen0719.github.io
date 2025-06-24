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
  <input type="file" name="file" accept="image/*" id="fileInput">
  <div id="fileInfo"></div>
  <script>
    document.getElementById('fileInput').addEventListener('change', function(event) {
    var file = event.target.files[0];
    if (file) {
      var fileInfo = `
        <p>File Name: ${file.name}</p>
        <p>File Size: ${file.size} bytes</p>
        <p>File Type: ${file.type}</p>
      `;
    document.getElementById('fileInfo').innerHTML = fileInfo;
    });
  </script>
</body>
</html>
