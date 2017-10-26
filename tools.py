import cv2.cv2
import random
import numpy as np

SIZE_X=600
SIZE_Y=400
SCAL_RATIO=int(SIZE_Y//2)
background=None

def getPt(x,y):
    imageX=x*SCAL_RATIO+SIZE_Y/2
    imageY=SIZE_X/2-y*SCAL_RATIO

    return (int(imageX),int(imageY))

def drawDots(dots,image,type="dot",color="blue"):
    if color=="blue":
        color=(0,0,255)
    else:
        color=(255,0,0)

    inputXs=dots[0]
    inputYs=dots[1]
    if len(inputXs)!=len(inputYs):
        raise RuntimeError("input dot error")

    if type=="dot":
        for index in range(len(inputXs)):
            cv2.circle(image,
                       getPt(inputXs[index],inputYs[index]),
                       1,
                       color)
    else:
        index=1
        while index<len(inputXs):
            cv2.line(image,
                     getPt(inputXs[index],inputYs[index]),
                     getPt(inputXs[index-1],inputYs[index-1]),
                     color)
            index+=1

curvX=inputXs=[(i/SIZE_X-1) for i in range(SIZE_X*2)]
def drawCurvs(reger,image,color="blue"):
    inputXs=curvX
    inputYs=reger.compute(inputXs)

    return drawDots([inputXs,inputYs],image,"line",color)

def getSamples(reger,num,scale=0.1):
    noise=np.random.normal(scale=scale,size=num)

    inputXs=[random.uniform(-1,1) for _ in range(num)]
    inputYs=reger.compute(inputXs)

    for index in range(num):
        inputYs[index]+=noise[index]

    backgroundImage=np.zeros((SIZE_X,SIZE_Y,3),dtype=np.uint8)
    backgroundImage+=255

    drawDots([inputXs,inputYs],backgroundImage)
    drawCurvs(reger,backgroundImage)
    global background
    background=backgroundImage

    return inputXs,inputYs

def draw(reger):
    if background is None:
        raise RuntimeError("tools is not inited")

    image=np.copy(background)
    drawCurvs(reger,image,"red")

    cv2.imshow("reg",image)
    cv2.waitKey(1)