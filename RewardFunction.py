# -*- coding: utf-8 -*-
"""
Created on Fri Feb 09 13:49:03 2018

@author: Ahmed Raafat
"""
import numpy
import re


def ComputeReward(speed,trackpos,angle,dist):
    stuck=0
    SOOT=0
    OOT=0
    

    if numpy.abs(trackpos)>=0.9:
        OOT=1   
    elif numpy.abs(trackpos)>=0.70:
        SOOT=1    
        
    if (numpy.abs(angle) >= 45 and speed<10) or (speed<5 and dist>20):
        x=count()
       # print("Restart in" +str(25-x))
        if x==25:
            stuck=1
            count.counter=0
    
    Rspeed=numpy.power((speed/float(130)),4)*0.05
    Rtrackpos=numpy.power(1/(float(numpy.abs(trackpos))+1),4)*0.8
    Rangle=numpy.power((1/((float(numpy.abs(angle))/40)+1)),4)*0.15
    

    
    if stuck==1:
        Reward=-2
    elif SOOT==1:
        Reward=(Rspeed+Rtrackpos+Rangle)*0.5
    elif OOT==1:
        if numpy.abs(trackpos) >=1.5:
            Reward=-1.5
        else:
            Reward=numpy.abs(trackpos)*(-1)
    else:
        Reward=Rspeed+Rtrackpos+Rangle
    #print("Reward = "+str(Reward))
    return Reward
'''
#maximum action index depending on Qmax value
def FindQmaxIndex(state,table):
    State=Stateindex(convert2string(state))
    x=table.loc[State][1:]
    ActionIndex=numpy.argmax(x)
    return int(ActionIndex)
'''

#Do After first iteration
def FindQmaxIndex(state,table):
    State=Stateindex(convert2string(state))
    maximum=table.iloc[State][1]
    ActionIndex=0
    for i in range (15):
        if table.iloc[State][i+1]>maximum: 
            maximum=table.iloc[State][i+1]
            ActionIndex=i
    return ActionIndex



def Stateindex(state):
    getnumbers=re.findall('\d+', state)
    values=[]
    
    for i in range (11):
        values.append(int(getnumbers[i]))
    
    output = "".join(map(str, values))
    del values
    return int(output, 2)


def convert2string(state):     #Converting state into partioned state (0000)(000)(0000)
    b=tuple(state)
    x=str(b[0:4])+str(b[4:7])+str(b[7:11])
    return x


def count():
    count.counter += 1 
    return(count.counter)
count.counter = 0
