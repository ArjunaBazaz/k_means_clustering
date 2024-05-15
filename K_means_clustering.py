import random
import sys
import urllib.request  
import io  
from PIL import Image
URL = str(sys.argv[1])
k = int(sys.argv[2])
f = io.BytesIO(urllib.request.urlopen(URL).read()) # Download the picture at the url as a file object  

img = Image.open(f)
pix = img.load()
pixelD = {}
colorAppear = {}
for y in range(0, img.height):
    for x in range(0, img.width):
        l = pix[x,y]
        if(l not in colorAppear.keys()):
            colorAppear[l] = []
        colorAppear[l].append((x,y))
while(len(pixelD.keys()) < k):
    randomX = random.randint(0, img.width-1)
    randomY = random.randint(0, img.height-1)
    if((randomX, randomY) not in pixelD.keys()):
        pixelD[pix[randomX, randomY]] = []
while(1 == 1):
    for x in colorAppear.keys():
        bestColor = 0
        lowestError = 1000000
        for colors in pixelD.keys():
            error = (x[0] - colors[0])**2 + (x[1] - colors[1])**2 + (x[2] - colors[2])**2
            if(bestColor == 0):
                lowestError = error
                bestColor = colors
            else:
                if(error < lowestError):
                    lowestError = error
                    bestColor = colors
        for y in colorAppear[x]:
            pixelD[bestColor].append(y)
    colorList = {}
    for x in pixelD.keys():
        averageR = 0
        averageG = 0
        averageB = 0
        for y in pixelD[x]:
            l = pix[y[0], y[1]]
            averageR = averageR + l[0]
            averageG = averageG + l[1]
            averageB = averageB + l[2]
        colorList[(int(averageR/len(pixelD[x])), int(averageG/len(pixelD[x])), int(averageB/len(pixelD[x])))] = []
    if(pixelD.keys() == colorList.keys()):
        break
    pixelD = colorList
for x in pixelD.keys():
    for z in pixelD[x]:
        pix[z[0], z[1]] = x
img = img.save("kmeansout.png")