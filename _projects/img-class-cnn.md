---
layout: page
title: Image Classification with Pretrained CNN Model
description: A model built off the MobileNet V3 model on the CIFAR-10/CINIC-10 datasets.
img: assets/img/funny-cnn.png
importance: 1
category: work
related_publications: true
pretty_table: true
---

Well...what do we see here! Below what you are currently reading is a box containing a few buttons. In case you missed the title, here’s a quick overview. Here, I am hosting a pretrained MobileNet V3 model on CIFAR-10 and CINIC-10 datasets so it can predict an image as either an airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck.

### Instructions:
- Upload image from your own computer using the button labeled as "Browse..."
- Enter a URL linking to an image on the internet and click the button labeled as "Upload"
- Click the button labeled as "Random Image" to pass an image from a preset folder.
- Please wait a few seconds for the model to initialize (especially on mobile devices).

<html>
<body>
  <div style="border-style: solid; border-width: 3px; border-radius: 5px; padding: 8px 3px 3px 5px">
    <label for="fileInput"><strong>Upload Image:</strong></label>
    <input id="fileInput" type="file" name="file" accept="image/*" id="fileInput" hidden>
    <button type="button" onclick="document.getElementById('fileInput').click()">Browse...</button>
    <br>
    <label for="imageUrl"><strong>Or Enter Image URL:</strong></label>
    <input type="text" id="imageUrl" placeholder="https://somewebsite.com/somepicture.png" style="width: 25%;">
    <button id="uploadBtn">Upload</button>
    <br>
    <label for="randImg"><strong>Or Pick Random:</strong></label>
    <button id="randImg">Random Image</button>
    <br><br>
    <div style="display: flex; align-items: center;">
      <label for="preview" style="margin: 0; padding-right: 1%;"><strong>Preview:</strong></label>
      <img id="preview">
    </div>
  </div>

  <div id="output" style="padding: 1em 0;"></div>
  <div id="barChart"></div>
  {% include torch-model.html %}
</body>
</html>

Obviously, if you're here, you're not just a robot trying to tell the difference between an airplane and a ship. I hope not... Anyways, I know you want to see some actual code. I will try to explain each portion of my code that has resulted in the model, that you should have tried, above.

{% raw %}
```python
import torch
import torchvision
from torch import nn
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torchvision import datasets, models
from torchvision import transforms
from nnFunctions import *
```
{% endraw %}

- **torchvision.datasets.ImageFolder**: Converts a folder of images (CINIC-10) to a dataset.
- **torch.utils.data.DataLoader**: Converts a dataset to a dataloader for future usage.
- **torchvision.datasets**: Library which provides the CIFAR-10 dataset so I don't have to create more folders.
- **torchvision.models**: Library which provides the MobileNet-V3L model which is used.
- **torchvision.transforms**: Library providing image alterations to improve training.
- **nnFunctions.py**: Python file with both a training and testing loop function.

**Note**: As of writing this, I have a moderate understanding of PyTorch but still need to learn to implement machine learning without the help of libraries.

{% raw %}
```python
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

trTransforms = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(60),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.47889522, 0.47227842, 0.43047404], std=[0.24205776, 0.23828046, 0.25874835])
])

teTransforms = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.47889522, 0.47227842, 0.43047404], std=[0.24205776, 0.23828046, 0.25874835])
])
```
{% endraw %}

These few lines of code are just to set up torch and image alterations for the datasets. The first line will detect if there is an accelerator and will use it. Below that is a training transforms and a testing transforms.

Training transform is made up of:
- 50% chance for a horizontal flip
- 50% chance for a vertical flip
- ±60 degrees rotation

In both the training and testing transforms, the images are eventually converted into tensors and normalized with values I found [here](https://github.com/BayesWatch/cinic-10).

{% raw %}
```python
trainData = ImageFolder(root="train", transform=trTransforms, target_transform=None)
trainDataLoader = DataLoader(dataset=trainData, batch_size=128, shuffle=True)

exTrainData = datasets.CIFAR10(root="data", train=True, download=True, transform=trTransforms, target_transform=None)
exTrainDataLoader = DataLoader(dataset=exTrainData, batch_size=128, shuffle=True)

testData = ImageFolder(root="test", transform=teTransforms)
testDataLoader = DataLoader(dataset=testData, batch_size=128)

exTestData = ImageFolder(root="valid", transform=teTransforms)
exTestDataLoader = DataLoader(dataset=exTestData, batch_size=128)

classesLength = len(trainData.classes)
```
{% endraw %}

Now, this is actually where I load in the data. Note that CINIC-10 has already been downloaded and un-tarred.

- torchvision's ImageFolder will be used to create a dataset from the CINIC-10's **train** folder with the training transforms and then turned into a training DataLoader.
- Extra training data will downloaded from torchvision.datasets in the form of CIFAR-10 and will also have the training transforms applied before becoming a DataLoader object.
- Testing data will be taken from CINIC-10's **test** and **valid** folder with the testing transforms and then turned into a testing DataLoader.
- Finally, a variable "classesLength" will be set to the amount of classes (10) for future use

Overall, you might have one question: *Why are you training and testing on both datasets?*
I am not very knowledgeable but I do know that more data equals higher accuracy, so...yeah.

{% raw %}
```python
model = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.DEFAULT).to(device)
model.classifier[3] = torch.nn.Sequential(
    torch.nn.Dropout(p=0.5),
    torch.nn.Linear(model.classifier[3].in_features, 10)
)
model.load_state_dict(torch.load(f='model.pth'))
```
{% endraw %}

This is where everything actually gets fun. I know that it is possible to create a model like this myself but a pretrained model is avaliable and could be used for my purpose.

This is MobileNet V3 Large, which should offer good performance while still being lightweight. It does live up to its promises since it only takes a fractions of a second to process an image on a crappy phone. I also decided to add a dropout layer to prevent overfitting and made sure it outputted 10 values at the end.

**Note**: I am loading "model.pth" since I was manually changing the learning rate.

{% raw %}
```python
for param in model.parameters():
    param.requires_grad = True

lossFx = nn.CrossEntropyLoss()
optim = torch.optim.AdamW(params=model.parameters(), lr=0.00003, weight_decay=0.0001)
```
{% endraw %}

- **model.parameters loop**: Make sure all parameters are allowed to pass through backpropagation.
- **nn.CrossEntropyLoss**: Loss function that seems to be really effective for multi-classification problems.
- **torch.optim.AdamW**: Optimizer set with a manual learning rate and a weight_decay.

Since the learning rate is changed every so often when progress slow, here is an example of what I have done to this model.

<table style="width: 100%; border-collapse: collapse; text-align: center;">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #ddd; padding: 8px;">Trial</th>
      <th style="border: 1px solid #ddd; padding: 8px;">Learning Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">1 - 8</td>
      <td style="border: 1px solid #ddd; padding: 8px;">0.001</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">8 - 15</td>
      <td style="border: 1px solid #ddd; padding: 8px;">0.0007</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">15 - 20</td>
      <td style="border: 1px solid #ddd; padding: 8px;">0.0003</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">20 - 25</td>
      <td style="border: 1px solid #ddd; padding: 8px;">0.00009</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">25 - 32</td>
      <td style="border: 1px solid #ddd; padding: 8px;">0.00003</td>
    </tr>
  </tbody>
</table>

<p></p>

{% raw %}
```python
for trial in range(7):
    print("Trial {}: ".format(trial + 1), end='')
    trainStep(model, trainDataLoader, lossFx, optim, accuracy, device)
    testStep(model, testDataLoader, lossFx, optim, accuracy, device)
    trainStep(model, exTrainDataLoader, lossFx, optim, accuracy, device)
    testStep(model, exTestDataLoader, lossFx, optim, accuracy, device)
```
{% endraw %}

It is pointless to show a loop with functions in them without the code inside the functions. The current trial is printed and each of these functions trains or tests the model.

Since the file is somewhat long, I am going to link the file with the *trainStep* and *testStep* loops [here](https://github.com/echen0719/code-suite/blob/main/Machine%20Learning/nnFunctions.py).

{% raw %}
```python
torch.save(obj=model.state_dict(), f='model.pth')
torch.onnx.export(model, torch.randn(1, 3, 32, 32).to(device), 'model.onnx')
```
{% endraw %}

This is prety straightforward. Save the model so I can manually change the learning rate for another training cycle. At the end, I output the model as a '.onnx' file which is what is actually running in the browser.

#### Conclusion

Running on validation data from CINIC-10 shows a **75.02%** accuracy and tends to confuse trucks, ships, and automobiles with each other. That is solid, given that it was only trained for 32 epochs. The model might be slightly complex for 32x32 images. In the future, I will try experimenting with different models such as *EfficientNet* or *VGG*, or custom models. Overall, a great experience for me to learn more about image classification.