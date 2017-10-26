import random

import tools

class Reger():
    def __init__(self,param=None):
        if param!=None:
            self.setParam(param)
        else:
            self.param=[0,1]

    def setParam(self,params):
        if len(params)<2:
            raise RuntimeError("too few param")
        self.param=params

    def getParam(self):
        return self.param

    def compute(self,inputXs):
        outputYs=[]
        for x in inputXs:
            y=self.param[0]
            index=1
            countX=x
            while index<len(self.param):
                y+=self.param[index]*countX
                countX*=x
                index+=1
            outputYs.append(y)
        return outputYs

    def computeGradient(self,samples):
        inputXs = samples[0]
        inputYs = samples[1]

        reger = Reger(self.getParam())
        regYs = reger.compute(inputXs)
        res = []
        for index in range(len(inputYs)):
            res.append(regYs[index] - inputYs[index])

        gradients = []
        countXs = [1 for _ in inputXs]
        for _ in range(len(self.getParam())):
            gradient = 0
            for index in range(len(countXs)):
                gradient += res[index] * countXs[index]
                countXs[index] *= inputXs[index]
            gradient/=len(countXs)
            gradients.append(gradient)
        return gradients

    def updateParam(self,gradients,learningRate):
        for index in range(len(self.param)):
            self.param[index]-=gradients[index]*learningRate

    def update(self,samples,learningRate):
        gradients=self.computeGradient(samples)
        self.updateParam(gradients,learningRate)

def randomParam(dim,max=1,min=-1):
    params=[]
    for _ in range(dim):
        params.append(random.uniform(min,max))
    return params

def show(regDim,realDim=None,realParam=None,numOfSample=100,learningRate=0.001,scale=0.1):
    if realParam==None:
        if realDim==None:
            raise RuntimeError("both realDim and realParam is None")
        realParam=randomParam(realDim)
        print("random param:"+str(realParam))
    startParam=randomParam(regDim)

    reger=Reger(realParam)
    samples=tools.getSamples(reger,numOfSample,scale=scale)

    reger.setParam(startParam)
    while True:
        reger.update(samples,learningRate)
        tools.draw(reger)

if __name__=="__main__":
    show(regDim=3,realDim=16,scale=0.05,learningRate=0.2,numOfSample=100)