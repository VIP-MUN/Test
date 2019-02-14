# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
import numpy as np
import math
import sys

def Normalization(Data):
    for column in Data:
        minvalue=Data[column].min()
        maxvalue=Data[column].max()
        Data[column]=Data[column].apply(lambda x: (x - minvalue)/(maxvalue-minvalue))
    return Data
  
#===========================
def ValidationSetApproach(trainingdata, K,DistanceType):
    randomTrainingData=trainingdata.sample(frac=1)
    print ( "randomTrainingData")
    print (randomTrainingData)
    tdRows=int( randomTrainingData.shape[0])
    print("Number of rows in TD: "+str(tdRows))
    tdsize = int(math.floor(tdRows/5))
    print ("first part\n")
    TrainPart =  randomTrainingData.head(tdsize*3)
    print("##############################################################")
    print(TrainPart)
    ValidationPart =  randomTrainingData[(tdsize*3):(tdsize*4)]
    print("##############################################################")
    print(ValidationPart)
    TestPart =  randomTrainingData[tdsize*4:]
    print("##############################################################")
    print(TestPart)
    
    ClassicalKNN(TrainPart,ValidationPart,K,DistanceType)  # output in csv
    output = pd.read_csv( "output.csv", sep='\t') 
    print (output)
    df1=output['Class']
    #df2=trainingdata.DataFrame(columns=['Class'])
    df2=ValidationPart['Class']
    #df1 = output['Class']

    df1Size=int(df1.shape[0])
    df2=ValidationPart['Class']
    df2Size=int(df2.shape[0])
    print ("df1 size = \n")
    print (df1Size)
    print ("df2 size = \n")
    print (df2Size)
    print ("df1 \n")
    print (df1)
    print ("df2 \n")
    print (df2)
    print (list (df2))
    if (df1.equals(df2)):
        print( "Algorithm is matching the test results by 100%")
    else:
        dfsim = df2.where(df2 == df1)
        print("Number of Errors:"+str(dfsim.isna().sum()))
        
    return 23
 #===========Cross validation=============  
def CrossValidation(trainingdata, K,DistanceType):
    #X_train, X_test, y_train, y_test = train_test_split(trainingdata.loc[:, trainingdata.columns != 'Class'], trainingdata['Class'], test_size=0.4, random_state=0)
    X_train, X_test, y_train, y_test = train_test_split(trainingdata, trainingdata['Class'], test_size=0.4, random_state=0)   
    print ( "x_train")
    print ( X_train)
             
    print ( "x_test")
    print ( X_test)
             
    print ( "y_train")
    print ( y_train)
             
    print("y_test")
    print(y_test)
    choice = input()
    ClassicalKNN(X_train,X_test,K,1)
    output = pd.read_csv( "output.csv", sep='\t') 
    print (output)
    PredictedOutput=output['Class']  # this should be compared with y_test
    
    #print (str(PredictedOutput[i])+ " vs " +str(y_test[i]))  does not work
    i = 0
    TP=0
    FP=0
    print ("PredictedOutput")
    print (PredictedOutput)
    print ("y_test")
    print (y_test)
    print ( len(PredictedOutput) )
    print ( len(y_test))
    while  i <len(PredictedOutput):
        
        if PredictedOutput[i] == y_test[i]:
            TP +=1
        else:
            FP+=1
    
        i+=1
    
    Percision = TP/(TP+FP)
    print ( "Percision = %f /n",Percision)
    return 2
 #===========Distance Funcs============= 
def EculideanDistance(inputInstance,testInstance):
    Summation =0
    #for column in testInstance:
    for i in range(8):
        
        #print ("inputInstance[column]") 
        #print ((inputInstance[1][i]))
        #print("\n")
        d=inputInstance[1][i] - testInstance[1][i]
        Summation= Summation+ math.pow(d ,2)
        #print ("inputInstance=" +str(inputInstance)+"\n")
        #print ("testInstance =" + str (testInstance)+"\n")
    print ("Summation =" +str(Summation)+"\n")
    print ( "class number is =  ")  
    print (inputInstance[1][9])
    Distance = [math.sqrt(Summation),inputInstance[1][9]]
    
    #print ( "class number is =  ") 
    #print ( inputInstance.iloc[:,-1])
    return Distance
 
 #======================== 
def Calculate_Nearest_neighbour(topMatched,K):
    print("topMatcheddddddddd")
    print (topMatched)
    MaxConditionalProbability=-1
    OutputClass=-1
    for j in range(K):  #loop on classes
        sum =0
        
        for i in range(K):
            if ((topMatched.iloc[j, 1] ==topMatched.iloc[i, 1]) ):# i!=j
                sum = sum+1
        print ( "sum")
        Probability=sum/K
        print(Probability)  
        if (Probability > MaxConditionalProbability):
            MaxConditionalProbability=Probability
            OutputClass=topMatched.iloc[j, 1];
    FinalOutput=[OutputClass,round(MaxConditionalProbability,2)]
    print (FinalOutput)
    return FinalOutput
      

def ClassicalKNN(trainingdata,testingdata,K,typeofDistance):
    FinalOutput=pd.DataFrame(columns=['Class','conditional_prob']);
    for row_inTest in testingdata.iterrows():
        AllDistancePerTest=pd.DataFrame(columns=['Distance','Class'])
       
        for row_inTrain in trainingdata.iterrows():
            # print ( "inside loop\n")
            # print ( row_inTrain ) 
            # print ( "row_inTest\n")
            # print (  row_inTest)
            resultlist=EculideanDistance(row_inTrain, row_inTest)
            # print ( "resultlist\n")
            # print ( resultlist)
            AllDistancePerTest.loc[len(AllDistancePerTest), :]=resultlist
     
        # d sort And get top k 5
        print ( "AllDistancePerTest\n")
        print ( AllDistancePerTest) 
        TopKPerTest=AllDistancePerTest.sort_values(by=['Distance'],ascending=False).head(3)
        print ("after sort and get top k \n" )
        #print ( AllDistancePerTest)
        print (TopKPerTest)
        
        #majority vot  or weight 
        tempOutput = Calculate_Nearest_neighbour(TopKPerTest,K)
        
        FinalOutput.loc[len(FinalOutput), :]=tempOutput
        print('FinalOutput')
        print(FinalOutput)
        #break

        #conditional probability
        #output
    FinalOutput.to_csv('output.csv',sep='\t')
        
    return 23
 
 #================main=================
print (sys.argv)
trainingdata = pd.read_csv( "TrainingData_A1.tsv", sep='\t', header=0) 

testingdata=  pd.read_csv( "TestData_A1.tsv", sep='\t', header=0) 
#K=int(sys.argv[3])
K=3
print (testingdata.head(1) )
#print ( sys.argv[3])

#type of Distane( majority vote or weights)  = 1, 2

choice = input("*Run KNN press 1 \n*Run Improve KNN  by normalization press 2 \n*Run Improve KNN  by weighted distance press 3 \n*test KNN press 4 \n*Cross Validation KNN press 5")
print (choice)
if int(choice) == 1:
    ClassicalKNN(trainingdata,testingdata,K,1)
    print ("call knn\n")
elif int(choice) == 2:
    #normalization then knn
    print (trainingdata.drop('Class', axis=1))
    NormalizedTrainingData=Normalization(trainingdata.drop('Class', axis=1))
    NormalizedTrainingData = pd.concat([NormalizedTrainingData, trainingdata['Class']], axis=1)
    NormalizedTestData=Normalization(testingdata); 
    print ( NormalizedTrainingData)
    print ( NormalizedTestData)
    #call knn
elif int(choice) == 3:
    #call knn && weight knn66
   # ClassicalKNN(trainingdata,testingdata,K,1)
    CrossValidation(trainingdata, K,1)
    print ("call knn\n")
elif int(choice) == 4:
    #test code
    ValidationSetApproach(trainingdata, K,1)
elif int(choice) == 5:
    #test CrossValidation
       #normalization then knn
    print (trainingdata.drop('Class', axis=1))
    NormalizedTrainingData=Normalization(trainingdata.drop('Class', axis=1))
    NormalizedTrainingData = pd.concat([NormalizedTrainingData, trainingdata['Class']], axis=1)
    NormalizedTestData=Normalization(testingdata); 
    
    
    CrossValidation(NormalizedTrainingData, K,1)
else:
    print ("Wrong choice!!")

