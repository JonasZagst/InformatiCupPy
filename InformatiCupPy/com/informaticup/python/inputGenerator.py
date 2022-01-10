import random

# import Main
import ioParsing
from InformatiCupPy.com.informaticup.python.algorithms.SimpleDijkstraAlgorithm import SimpleDijkstraAlgorithm
from InformatiCupPy.com.informaticup.python.algorithms.SimpleTrainParallelizationAlgorithm import SimpleTrainParallelizationAlgorithm
from InformatiCupPy.com.informaticup.python.ioParsing.InputParser import InputParser
from InformatiCupPy.com.informaticup.python.ioParsing.OutputParser import OutputParser


class inputGenerator:

    def __init__(self):
        self.numberOfStations = 0
        self.numberOfTrains = 0
        self.numberOfPassengers = 0
        self.stationMaxCap = 0
        self.lineMaxLength = 0
        self.lineMaxCap = 0
        self.trainMaxMaxSpeed = 0
        self.trainMaxCap = 0
        self.passengerMaxGroupSize = 0
        self.fileName = ''
        self.numberOfFiles = 0
        self.stationCapList = []


    def getNumberOfObjects(self):
        print('Wie viele Bahnhöfe soll die Inputdatei haben?')
        self.numberOfStations = int(input())
        print('Wie viele Strecken soll die Inputdatei haben?')
        self.numberOfLines = int(input())
        print('Wie viele Züge soll die Inputdatei haben?')
        self.numberOfTrains = int(input())
        print('Wie viele Passagiere soll die Inputdatei haben?')
        self.numberOfPassengers = int(input())

    def getSpecifications(self):
        print('Wie hoch soll die maximale Kapazität der Bahnhöfe sein?')
        self.stationMaxCap = int(input())
        print('Wie lang soll eine Strecke maximal sein?')
        self.lineMaxLength = int(input())
        print('Wie hoch soll die maximale Kapazität der Strecken sein?')
        self.lineMaxCap = int(input())
        print('Wie hoch soll die maximale Maximalgeschwindigkeit der Züge sein?')
        self.trainMaxMaxSpeed = int(input())
        print('Wie hoch soll die Maximale Kapazität der Züge sein?')
        self.trainMaxCap = int(input())
        print('Wie groß soll eine Passagiergruppe maximal sein?')
        self.passengerMaxGroupSize = int(input())
        print('Wie soll die Inputdatei heißen?')
        self.fileName = str(input())
        print('Wie viele Files sollen generiert werden?')
        self.numberOfFiles = int(input())

    def generateInputFile(self):
        self.getNumberOfObjects()
        self.getSpecifications()

        for i in range(1, self.numberOfFiles + 1):
            self.inputFile = open(self.fileName + "_" + str(i) + ".txt", "w+")
            self.generateStations()
            self.generateLines()
            self.generateTrains()
            self.generatePassengers()

            self.inputFile.close()

        # self.solveGeneratedFiles()

    # def solveGeneratedFiles(self):
    #
    #
    #     for i in range(1, self.numberOfFiles + 1):
    #         input = InputParser("../python/"+self.fileName + "_"+str(i)+".txt").parse_input()
    #         Main.main()
    #         # solvers = [SimpleTrainParallelizationAlgorithm("../python/"+self.fileName + "_"+str(i)+".txt"), EasyDijkstraAlgorithm("../python/"+self.fileName + "_"+str(i)+".txt")]
    #         # OutputParser.parse_output_files(solvers, input)

    def generateStations(self):
        self.inputFile.write("# Bahnhoefe: str(ID) int(Kapazitaet) \n")
        self.inputFile.write("[Stations]\n")
        for x in range(1, self.numberOfStations+1):
            stationString = "S"+str(x)+" "+str(random.randint(1, self.stationMaxCap))+" \n"
            self.stationCapList.append(int(stationString[3:stationString.__len__()]))
            self.inputFile.write(stationString)

    def generateLines(self):
        lineList = []

        self.inputFile.write("\n# Strecken: str(ID) str(Anfang) str(Ende) dec(Laenge) int(Kapazitaet)\n")
        self.inputFile.write("[Lines]\n")

        for x in range(self.numberOfLines):
            lineString = "L" + str(x) + " "

            lineBeginning = random.randint(1, self.numberOfStations)
            lineEnding = random.randint(1, self.numberOfStations)

            if lineBeginning != lineEnding:
                lineString = lineString+"S"+str(lineBeginning)+" "+"S"+str(lineEnding)+" "
            else:
                if lineBeginning == self.numberOfStations-1:
                    lineBeginning = lineBeginning-1
                elif lineBeginning == 0:
                    lineBeginning = lineBeginning+1
                else:
                    lineBeginning = lineBeginning+1
                lineString = lineString + "S" + str(lineBeginning) + " " + "S" + str(lineEnding) + " "

            lineString = lineString+str(random.randint(1, self.lineMaxLength))+" "+str(random.randint(1, self.lineMaxCap))+"\n"

            lineList.append(lineString)

        allLines = ""
        missingStation = []
        temporaryLineList = []

        # getting all stations now connected
        for i in lineList:
            allLines =allLines + i[4]+i[7]

        # getting all missing lines (station not connected)
        for i in range(1, self.numberOfStations+1):
            if str(i) not in allLines:
                missingStation.append(str(i))

        # appending all missing line strings (of not connected stations) to the lineList
        for i in missingStation:
            missingLineString = "L"+str(self.numberOfLines+int(i))+" "+"S"+str(i)+" "+"S"+str(random.randint(1, self.numberOfStations))+" "+str(random.randint(1, self.lineMaxLength))+" "+str(random.randint(1, self.lineMaxCap))+"\n"

            lineList.append(missingLineString)

        # deletes dublicates
        lineList = list(dict.fromkeys(lineList))

        # getting other dublicates
        for i in lineList:
            a = i.replace("S" + str(i[7]) + " " + "S" + str(i[4]), "X")
            temporaryLineList.append(a)

        # deleting other dublicates
        lineList = temporaryLineList
        temporaryLineList2 =  []
        for i in lineList:
            if not i.__contains__("X"):
                temporaryLineList2.append(i)
        lineList = temporaryLineList2

        # unify line IDs
        counter = 0
        temporaryLineList3 = []
        for i in lineList:
            counter = counter + 1
            index = i.find(" ")
            #print(index)
            CurrentLineID = i[0:index]
            #print(CurrentLineID)
            a = i.replace(CurrentLineID, "L"+str(counter))
            temporaryLineList3.append(a)
        lineList = temporaryLineList3

        # writing all lines into the input file
        for i in lineList:
            self.inputFile.write(i)

    def generateTrains(self):
        self.inputFile.write("\n# Zuege: str(ID) str(Startbahnhof)/* dec(Geschwindigkeit) int(Kapazitaet)\n")
        self.inputFile.write("[Trains]\n")

        trainList = []

        for x in range(1, self.numberOfTrains+1):
            firstStation = random.randint(1, self.numberOfStations)

            if firstStation != self.numberOfStations:
                trainString = "T" + str(x) + " " + "S"+ str(firstStation) +" "+str(random.randint(1, self.trainMaxMaxSpeed-1))+" "+str(random.randint(1, self.trainMaxCap-1)) + "\n"
            else:
                trainString = "T" + str(x) + " " + "*" +" "+str(random.randint(1, self.trainMaxMaxSpeed- 1))+" "+str(random.randint(1, self.trainMaxCap - 1)) + "\n"
            trainList.append(trainString)


        # checking capacity of first station

        for i in range(1, self.numberOfStations+1):
            for a in trainList:
                counter = 0
                if a.__contains__("S"+str(i)):
                    counter = counter +1
            if counter > self.stationCapList[i-1]:
                numberOfWrongTrains = counter - self.stationCapList[i-1]
                counter2 = 0
                for c in trainList:
                    if counter2 < numberOfWrongTrains:
                        if c.contains("S"+str(i)):
                            indexC = trainList.index(c)
                            newString = c
                            trainList.remove(c)
                            counter2 = counter2 + 1
                            newString = newString.replace("S"+str(i), "*")
                            trainList.remove(c)
                            trainList.insert(indexC, newString)




        for i in trainList:
            self.inputFile.write(i)

    def generatePassengers(self):
        self.inputFile.write("\n# Passagiere: str(ID) str(Startbahnhof) str(Zielbahnhof) int(Gruppengroeße) int(Ankunftszeit)\n")
        self.inputFile.write("[Passengers]\n")
        for x in range(1, self.numberOfLines+1):
            passengerString = "P" + str(x) + " "

            passengerStart = random.randint(1, self.numberOfStations)
            passengerArrival = random.randint(1, self.numberOfStations)

            if passengerStart != passengerArrival:
                passengerString = passengerString + "S" + str(passengerStart) + " " + "S" + str(passengerArrival) + " "
            else:
                if passengerStart == self.numberOfStations - 1:
                    passengerStart = passengerStart - 1
                elif passengerStart == 0:
                    passengerStart = passengerStart + 1
                else:
                    passengerStart = passengerStart + 1
                passengerString = passengerString + "S" + str(passengerStart) + " " + "S" + str(passengerArrival) + " "
            passengerString = passengerString + str(random.randint(1, self.passengerMaxGroupSize)) + " " + str(random.randint(1, 200)) + "\n"
            self.inputFile.write(passengerString)

    def printNumberOfObjects(self):
        print(self.numberOfStations)
        print(self.numberOfLines)
        print(self.numberOfTrains)
        print(self.numberOfPassengers)




