import numpy as np
class Polybius:
    encodings = []
    order = []
    dims = 0
    tab = []
    orderString = ""
    def __init__(self,order="abcdefgh[ij]klmnopqrstuvwxyz", dims=5): 
        self.orderString = order
        self.order = Polybius.order_to_list(order)
        self.dims=dims
        self.tabulify()
        self.initEncodings()
    def order_to_list(order):
        order = [ [i] for i in list(order)] 
        i=0 
        while True:
            if i>=len(order): 
                break
            if order[i][0]=="[":
                order.pop(i)
                array = []
                while order[i][0]!="]":
                    array.append(order[i][0])
                    order.pop(i) 
                order[i] = array
            i+=1
        return order
        
    def tabulify(self):
        order = list(self.order)
        for i in range(self.dims,len(self.order)):
            if(i%int(len(self.order)/self.dims))==0:
                order[i] = "\n"+str(order[i])
        self.tab ="".join([str(i) for i in order])
    def getIndex(self,char):
        for i in range(len(self.order)):
            if char in self.order[i]:
                return i
    def getTupIndex(self,tup):
            return int((tup[0]-1)*self.dims+tup[1]-1)
    def initEncodings(self):
        for i in range(1,len(self.order)+1):
            self.encodings.append(self.encode(i))
    def modulo2(num,basis):
        modulo = num%basis
        if modulo==0: 
            return basis 
        else:
            return modulo
    def encode_char(self,char):
        return self.encodings[self.getIndex(char)]
    def encode(self,index):
       # index = self.getIndex(char)
        return np.array([int(np.ceil(index/self.dims)),Polybius.modulo2(index,self.dims)])
    def encode_int(self,char):
        encoded = self.encode_char(char)
        return int(encoded[0]*10+encoded[1])
    def decode(self,tup):
        tup = ((Polybius.modulo2(tup[0],self.dims),Polybius.modulo2(tup[1],self.dims)))
        return self.order[self.getTupIndex(tup)]
    def decode_int(self,integer):
        one = (integer%10)
        dec = (integer-integer%10)/10
        return self.decode((dec,one))
    def __repr__(self):
        return self.tab
    def genAlphabet(header,alphabet):
        header = genOrderCommand(header)
        alphabet = genOrderCommand(alphabet)
    def legalchars(self,inputchars):
        if inputchars in self.orderString:
            return True
        else:
            return False
    def encodeString_int(self,sentence):
        sentence = [i for i in filter(self.legalchars,sentence)]
        print(sentence)
        newsentence = []
        for i in sentence:
            newsentence.append(self.encode_int(i))
        return newsentence 
    def encodeString(self,sentence):
        sentence = [i for i in filter(self.legalchars,sentence)]
        print(sentence)
        newsentence = []
        for i in sentence:
            newsentence.append(self.encode_char(i))
        return newsentence
    def decodeString_int(self,sentence):
        newsentence = []
        for i in sentence:
            m = self.decode_int(i)
            if len(m)>1:
                newsentence.append("[")
            for j in m:
                newsentence.append(j)
            if len(m)>1: 
                newsentence.append("]")
        return "".join(newsentence)

    def decodeString(self,sentence):
         newsentence = []
         for i in sentence:
             m = self.decode(i)
             if len(m)>1:
                 newsentence.append("[")
             for j in m:
                 newsentence.append(j)
             if len(m)>1: 
                 newsentence.append("]")
         return "".join(newsentence)      

class contentUnit:
    content = ""
    intcontent = []
    tuplecontent = []
    def __init__(self,content,intcontent,tuplecontent):
        self.content = content
        self.intcontent = intcontent
        self.tuplecontent = tuplecontent

def repeatFuncAdd(seta,setb,offset=0):
    setc = seta.copy()
    for i in range(len(seta)):
        setc[i]+=setb[(i+offset)%len(setb)]
    return setc

def getClosestRect(area,xlen):
     if(area%xlen==0):
             return area
     else:
             return area-(area%xlen)+xlen

def reshapeRect(data,lenx):
     newArea = getClosestRect(len(data),lenx)
     leny = int(newArea/lenx)
     data = list(data)
     for i in range(len(data),newArea):
         data.append(0)
     return np.reshape(data,(leny,lenx))

def reshapeRect_tup(data,lenx):
     newArea = getClosestRect(len(data),lenx)
     leny = int(newArea/lenx)
     data = list(data)
     for i in range(len(data),newArea):
         data.append(np.array([0,0]))
     return np.reshape(data,(leny,lenx,-1))




def getPossibilities(offset,length,wordlength,encrypt_int,repertoire):
    aggreg_data = reshapeRect(encrypt_int,wordlength)
    new_data = []
    for i in range(offset,length+offset):
        experiment_data = [] 
        for k in range(repertoire):
            integer = int(np.ceil((k+1)/int(np.sqrt(repertoire))))*10+(k%int(np.sqrt(repertoire))+1)
            aux_data = aggreg_data.copy()[:,i]
            print(len(aux_data))
            for j in range(len(aux_data)):
                aux_data[j] -= integer
            experiment_data.append(aux_data)
            #np.reshape(experiment_data,(-1,length))
        new_data.append(experiment_data)
    return new_data

def getPossibilities_multi(offset,length,wordlength,encrypt_int,repertoire):
    aggreg_data = reshapeRect(encrypt_int,wordlength)
    new_data = []
    for i in range(offset,length+offset):
        experiment_data = [] 
        for k in range(repertoire[i-offset][0],repertoire[i-offset][1]):
            integer = int(np.ceil((k+1)/int(np.sqrt(repertoire))))*10+(k%int(np.sqrt(repertoire))+1)
            aux_data = aggreg_data.copy()[:,i]
            print(len(aux_data))
            for j in range(len(aux_data)):
                aux_data[j] -= integer
            experiment_data.append(aux_data)
            #np.reshape(experiment_data,(-1,length))
        new_data.append(experiment_data)
    return new_data

def getPermutationTree(new_data):
    levels_a = [ HungDaddy(i) for i in new_data[0]]
    middle_levels = [levels_a]
    for i in range(1,len(new_data)-1):
        currentLayer = []
        for j in range(len(new_data[i])):
            
            for k in range(len(middle_levels[i-1])):
                cock = MiddleFaggot(new_data[i][j],middle_levels[i-1][k])
                currentLayer.append(cock)
        middle_levels.append(currentLayer)
    currentLayer = []
    for m in range(len(new_data[len(new_data)-1])):
        for n in range(len(middle_levels[len(middle_levels)-1])):
            cock = TopBull(new_data[len(new_data)-1][m],middle_levels[len(new_data)-2][n])
            currentLayer.append(cock)
    middle_levels.append(currentLayer)
    return middle_levels

def extractPermutations(middle_levels):
    t = TreeGraph(middle_levels)
    return t.getLastLevelBranches()
 
def reshapePermutation(permutations):
    permutations = np.array(permutations)
    newperms = []
    for i in range(len(permutations)):
        newperms.append([ permutations[i,:,j] for j in range(len(permutations[i][0])) ])
    return np.array(newperms)[:,:,::-1]

def refillPermutations(permutations,originalString, wordLength):
    perms = []
    size = len(permutations[0][0])
    for i in range(len(permutations)):
        perms.append(refillPermutation(permutations[i],originalString,size,wordLength))
    return perms

def refillPermutation(permutation,originalString,origSize, wordLength):
    perm = []
    counter = 0
    #leny = (int(len(originalString)/wordLength))
    for i in range(len(originalString)):
        if i % wordLength < origSize:
            current = permutation[int(counter/origSize)][counter%origSize]
            perm.append(current)
            counter+=1
        else:
            perm.append(originalString[i])
    
    return perm
def getStringRepresentation(polybius,permutations):
    str_a = []
    for i in permutations:
        str_b = []
        for j in i:
            str_b.append(polybius.decodeString_int(j))
        str_b = "\n".join(str_b)
        str_a.append(str_b)
    return str_a

class HungDaddy:
    def __init__(self,content):
        self.content = content
    def getParents(self,content):
        content.append(self.content)
        return content

class MiddleFaggot:
    def __init__(self,content,parent):
        self.parent = parent
        self.content = content
    def getParents(self,content):
        content.append(self.content)
        return self.parent.getParents(content)

class TopBull:
    def __init__(self,content,parent):
        self.parent = parent
        self.content = content
    def getParents(self):
        return self.parent.getParents([self.content])


class TreeGraph:
    levels = []
    def __init__(self,levels):
        self.levels = levels
    def addlevel(self,level):
        levels.append(level)
    def getLastLevelBranches(self):
        lastlevels = []
        for i in self.levels[len(self.levels)-1]: 
            lastlevels.append(i.getParents())
        return lastlevels

def getRange(arr):              
  tuples = []
  for i in range(len(arr[0])):
          scope = arr[:,i]
          max = np.max(scope%10)
          min = np.min(scope%10)
          tuples.append(max-min)
  return tuples 

def getAvgProbability(rect):                                    
     p = [ getProbability(rect[:,i]) for i in range(len(rect[0]))] 
     return np.mean(p)

def getAvgProbability_closest(rect):
    p = []
    for i in range(len(rect)):
        for j in rect[i]:
            p.append(j)
    return np.mean(getProbability(p))

def getProbability(text):                                     
     unique, counts = np.unique(list(text), return_counts=True)
     c = np.sum(counts*(counts-1))                               
     l = len(text)*(len(text)-1)                                 
     return c/l

def reshapeRect_noPadding(cipher,lenx):
    buckets = []
    for i in range(lenx):
        buckets.append([])
        for j in range(len(cipher)):
            if j%lenx == i:
                buckets[i].append(cipher[j])
    return np.array(buckets)

def getProbabilityHistogram(cipher):
    probabilities = []
    for i in range(2,len(cipher)-1):
        probabilities.append(getAvgProbability(reshapeRect(cipher,i)))
    return probabilities

def getIndexDict(arr):
    return [(i+2,arr[i]) for i in range(len(arr))]

def getCoords(i,base,treeSpan):
    starter = i
    coords = []
    counter = treeSpan
    while starter != 0:
        carry = starter%base
        starter-=carry
        starter = int(starter/base)
        coords.append(carry+1)
        counter-=1
    for i in range(0,counter):
        coords.append(1)
    return coords

def getPolybiusCoords(polybius,coords):
    newcoords = []
    for i in coords:
        var = polybius.encode(i)
        num = var[0]*10+var[1]
        newcoords.append(num)
    return newcoords

def appendRow(cipher,matrix,wordlength):
    newperm = []
    for i in range(len(cipher)):
        if i % wordlength == len(matrix[0]):
            newperm.append(np.append(matrix[int(i/wordlength)],cipher[i]))
    return np.array(newperm)

def zipChildren(array):
    zipped = []
    for i in range(len(array)*len(array[0])):
        zipped.append(array[int(i/len(array[0]))][i%len(array[0])])
    return zipped
   

def findNihil(rect,repertoire,desiredprob,bounds):
    perms = [np.array(rect)[:,i] for i in range(len(rect[0]))]
    for i in range(1,len(perms)):
        print("\n\n")
        maxcoord = int(np.sqrt(repertoire))
        coords = (maxcoord+1)*10+(maxcoord%10+1)
        for k in range(coords+1):
                        #print(coords)
            permcopy = perms.copy()[0:i+1]
            #print(permcopy)
            permcopy[i]-=k
            #print(permcopy[i][i])
            probability = getProbability(zipChildren(permcopy))
            print(probability)
            if probability < desiredprob+bounds and probability > desiredprob-bounds:
                print("hello")
                for m in range(len(permcopy)):
                    for n in range(len(permcopy[m])):
                        perms[m][n] = permcopy[m][n]
                break
            permcopy[i]+=k
    return perms

def findNihil_biased(rect,repertoire,desiredprob,bounds,bias):
    perms = [np.array(rect)[:,i] for i in range(len(rect[0]))]
    perms[0]-=bias
    for i in range(1,len(perms)):
        print("\n\n")
        for k in range(repertoire):
            maxcoord = int(np.sqrt(repertoire))
            coords = (int(k/maxcoord)+1)*10+((k%maxcoord)+1)
                        #print(coords)
            permcopy = perms.copy()[0:i+1]
            #print(permcopy)
            permcopy[i]-=coords
            #print(permcopy[i][i])
            probability = getProbability(zipChildren(permcopy))
            print(probability)
            
            if probability < desiredprob+bounds and probability > desiredprob-bounds:
                print("hello")
                for m in range(len(permcopy)):
                    for n in range(len(permcopy[m])):
                        perms[m][n] = permcopy[m][n]
                        break
            permcopy[i]+=coords
    return perms

def findNihil_inSecure(rect,repertoire,desiredprob,bounds):
    perms = [np.array(rect)[:,i] for i in range(len(rect[0]))]
    for i in range(1,len(perms)):
        print("\n\n")
        maxcoord = int(np.sqrt(repertoire))
        coords = (maxcoord+1)*10+(maxcoord%10+1)
        for k in range(coords+1):
            #print(coords)
            permcopy = perms.copy()[0:i+1]
            #print(permcopy)
            permcopy[i]-=k
            #print(permcopy[i][i])
            probability = getProbability(zipChildren(permcopy))
            print(probability)
            permcopy[i]+=k
            if probability < desiredprob+bounds and probability > desiredprob-bounds:
                perms[i] = permcopies[np.argmax(probs)][i]
                permcopy[i]+=k
                break

    return perms

def findNihil_unSure(rect,repertoire):
    perms = [np.array(rect)[:,i] for i in range(len(rect[0]))]
    for i in range(1,len(perms)):
        print("\n\n")
        maxcoord = int(np.sqrt(repertoire))
        coords = (maxcoord+1)*10+(maxcoord%10+1)
        probs = []
        permcopies = []
        for k in range(coords+1):
            #print(coords)
            permcopy = perms.copy()[i-1:i+1]
            #print(permcopy)
            permcopy[1]-=k
            #print(permcopy[i][i])
            probability = getProbability(zipChildren(permcopy))
            probs.append(probability)
            permcopies.append(permcopy.copy()[1])
            permcopy[1]+=k
           # print(probability)
        print(np.max(probs))
    perms[i] = permcopies[np.argmax(probs)][i]
    return perms

def findNihil_highestBidder(rect,repertoire):
    perms = [np.array(rect)[:,i] for i in range(len(rect[0]))]
    for i in range(1,len(perms)):
        print("\n\n")
        maxcoord = int(np.sqrt(repertoire))
        coords = (maxcoord+1)*10+(maxcoord%10+1)
        probs = []
        permcopies = []
        for k in range(coords+1):
                        #print(coords)
            permcopy = perms.copy()[0:i+1]
            #print(permcopy)
            permcopy[i]-=k
            #print(permcopy[i][i])
            probability = getProbability(zipChildren(permcopy))
            probs.append(probability)
            permcopies.append(permcopy.copy())
            permcopy[i]+=k
           # print(probability)
        print(np.max(probs))
        for m in range(len(permcopies[0])):
            for n in range(len(permcopies[0][0])):
                perms[m][n] = permcopies[np.argmax(probs)][m][n]
    return perms
            
def findNihil_highestBidder_biased(rect,repertoire,bias):
    perms = [np.array(rect)[:,i] for i in range(len(rect[0]))]
    perms[0]-=bias
    for i in range(1,len(perms)):
        print("\n\n")
        probs = []
        permcopies = []
        for k in range(repertoire):
            maxcoord = int(np.sqrt(repertoire))
            coords = (int(k/maxcoord)+1)*10+((k%maxcoord)+1)
                        #print(coords)
            permcopy = perms.copy()[0:i+1]
            #print(permcopy)
            permcopy[i]-=coords
            #print(permcopy[i][i])
            probability = getProbability(zipChildren(permcopy))
            probs.append(probability)
            permcopies.append(permcopy.copy())
            permcopy[i]+=coords
           # print(probability)
        print(np.max(probs))
        for m in range(len(permcopies[0])):
            for n in range(len(permcopies[0][0])):
                perms[m][n] = permcopies[np.argmax(probs)][m][n]
    return perms

 

def getPossibilityListing(offset,length,wordLength,polybius,cipher):
    pos = getPossibilities(offset,length,wordLength,cipher,len(polybius.order))
    tree = getPermutationTree(pos)
    perms = extractPermutations(tree)
    perms_rshaped = reshapePermutation(perms)
    perms_str = getStringRepresentation(polybius,perms_rshaped)
    file_a = open("nihilist_table.txt","w")
    for i in perms_str:
        file_a.write(i)
        file_a.write("\n\n\n\n\n\n\n")
    file_a.close()
    perms_fill = [(polybius.decodeString_int(j)) for j in refillPermutations(perms_rshaped,cipher,wordLength)]
    #print(str(perms_fill).replace(",","\n"))
    file_b = open("nihilist_string.txt","w")
    file_b.write(str(perms_fill))
    file_b.close()


