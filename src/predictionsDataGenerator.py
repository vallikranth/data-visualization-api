import os
import time
import json
import random
from timeit import default_timer as timer

success = 0
failure = 0

def mockData(finalJsonRows):
    data={}
    data['modelName']="Deep1"
    data['version']="V1"
    data['predictionDate']=time.time()
    getPredictions(data)
    generateActualValue(data)
    #print("data is:",json.dumps(data))
    finalJsonRows = finalJsonRows.append(data);
    #writeFile(data)

def getPredictions(data):
    data['predictions']=[]
    numberOfPredictions=random.randint(1,5)
    randomNumberArray = random.sample(range(1, 101), numberOfPredictions)
    arraysum = sum(randomNumberArray)
    randomNumberArray = [(i/arraysum) * 100 for i in randomNumberArray]
    
    for i in range(numberOfPredictions):
        prediction={}
        prediction['answer']=str(random.randint(1,76))
        prediction['probability']=randomNumberArray[i]
        data['predictions'].append(prediction)
        
def generateActualValue(data):
    global success
    global failure
    if(len(data['predictions']) % 2 == 0):
            success = success +1
            randomIndex=random.randint(0,len(data['predictions'])-1)
            data['actual'] = data['predictions'][randomIndex]['answer']
    else:
        failure = failure +1
        data['actual'] = str(random.randint(1,76))

def writeFile(data):
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    outputFilePath= os.path.join(currentDirectory, "../data/prediction-mock.json")
    #===========================================================================
    # if os.path.isfile(outputFilePath):
    #     fileModifiedTime=os.path.getmtime(outputFilePath)
    #     currentTime=time.time()
    #     timediff = currentTime - fileModifiedTime
    #     print("file exists and is older by {} seconds. Deleting...".format(timediff))
    #===========================================================================
        #os.remove(outputFilePath)
    outputFile = open(outputFilePath, 'w+')
    for row in data:
        outputFile.write(json.dumps(row))
        outputFile.write("\n")
    print("successfully written mock data to file:",outputFilePath)
    outputFile.close()
    
if __name__ == '__main__':
    start = timer()
    numberOfRows = 100
    finalJsonRows = []
    for i in range(numberOfRows):
        mockData(finalJsonRows)
    writeFile(finalJsonRows)    
    print("Total good predictions rows:",success)
    print("Total bad predictions rows:",failure)
    print("Total time taken is {} seconds".format(timer()-start))
    