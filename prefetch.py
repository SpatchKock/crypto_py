import numpy as np
import matplotlib.pyplot as plt
from order import *
from libs import *

def fetchContent(file):
    file = open(file,"r")
    content = file.read()
    charcontent = content.split(" ")
    intcontent = np.array([ int(i) for i in charcontent])
    firstdigits = intcontent%10
    seconddigits = np.array([int((intcontent[i]-firstdigits[i])/10) for i in range(len(intcontent))])
    tuplecontent = np.array([ (seconddigits[i],firstdigits[i]) for i in range(len(firstdigits))])
    return contentUnit(content,intcontent,tuplecontent)

ty = fetchContent("46ty.txt")
nihilist = fetchContent("Nihilist.txt")

