---
layout: page
title: echen0719's General Utils
description: Hate having to find free tools to do the things I need
img: assets/img/pack.png
importance: 2
category: work
related_publications: true
pretty_table: true
---

<style>

.word-count-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

</style>

<p style="margin-top: -15px;">Self-explanatory, ehh?</p>

<script>
const text = document.getElementById("text");
const words = document.getElementById("words");
const characters = document.getElementById("characters");
const sentences = document.getElementById("sentences");
const fileInput = document.getElementById("fileInput");

text.addEventListener("input", updateCount);

function updateCount() {
    const value = text.value;
    characters.textContent = value.length;
    
    // equivalent of "\\S+"
    let wordCount = value.trim().match(/\S+/g);
    words.textContent = wordCount ? wordCount.length : 0; // one-line if else statement

    // count number of punctuation (excluding spaces)
    let sentenceCount = value.trim().match(/[.!?]+/g);
    sentences.textContent = sentenceCount ? sentenceCount.length : 0;
}

function loadFile() {
    fileInput.click()
}

fileInput.addEventListener("change", function () {
    const file = this.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = function (event) {
        text.value = event.target.result;
        updateCount();
    };

    reader.onerror = function () {
        console.log("Unable to read this file.");
    };

    reader.readAsText(file);

    this.value = "";
});

function clearText() {
    text.value = "";
    updateCount();
}
</script>

<div class="word-count-container">
    <h3 style="text-align: center;">Word Counter</h3>
    <div>
        <span id="words" style="font-weight: bold;">0</span> Words |
        <span id="characters" style="font-weight: bold;">0</span> Characters |
        <span id="sentences" style="font-weight: bold;">0</span> Sentences
    </div>

    <textarea id="text" rows="10" cols="75" placeholder="Type or paste your text here..." autocomplete="off"></textarea>
    
    <div class="buttons">
        <input id="fileInput" type="file" hidden>
        <button onclick="loadFile()">Load file</button>
        <button onclick="clearText()">Clear text</button>
    </div>
    
    <p></p>
</div>

<script>

</script>

<div class="image-color-remover-container">
    <h3 style="text-align: center;">Remove Color From Image</h3>
    <div>
        <p>INDEV</P>
    </div>
</div>