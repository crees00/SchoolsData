##########################################################################
setwd("C:/Users/reesc1/Docs/Code/R/Titanic")
#SET-UP
#Install the recursive partitioning and regression trees package
install.packages("rpart")
install.packages("rpart.plot")
install.packages("rattle")
require("rpart")
require("rpart.plot")
require("rattle")
# library(rpart)
# library(rpart.plot)
# library(rattle)


#Set the working directory where you will be loading and saving data from

#Load Titanic dataset that we will train the data on
Titanic.Train <- read.csv("train.csv", stringsAsFactors=FALSE)


#HAVE A LOOK AT THE DATA YOU ARE GOING TO USE
#Review structure of the data (shows field type and outputs form first few cases)
str(Titanic.Train)

#Look at a summary of the data (shows distribution of data for numeric fields)
summary(Titanic.Train)

#FIT THE MODEL
#Apply Decision Tree model to predict whether passengers survived based on the 6 variables
#Note that the control variables are option. These control the the size and structure of the
#decision tree. Type ?rpart.control help documentation for more information on how these work.
Titanic.Train.RP.model <- rpart(Survived ~ Sex + Age + SibSp + Parch + Fare + Embarked, #Equation
                                data=Titanic.Train, method="class",  #Data source. Method = class is needed for binomial model
                                control=rpart.control(minsplit=8, minbucket=4, cp=0.005, maxdepth = 10)) #control variables

#Plot the decision tree
fancyRpartPlot(Titanic.Train.RP.model)

#An alternative style of plotting the tree
prp(Titanic.Train.RP.model)

#Show the importance of each of the variables. This is a reflection of the goodness of fit 
#each variable provides. The high the number the more important the variable
Titanic.Train.RP.model$variable.importance 

#APPLY THE MODEL
#We can take the model we've fitted and apply it to our training data
#This will give us a percentage value for each record. 
#This is our prediction of how likely they were to survive
#The predict function is of the form predict([model name],[dataset name], [output required])
#In this case response gives us the % chance that they survive according to our model
Titanic.Train.RP.Preds <- predict(Titanic.Train.RP.model,type="prob")

#Look at a summary of our predictions. The % chance of survival varies from 5% to 100%
summary(Titanic.Train.RP.Preds)

#Match the predictions back onto the main dataset to create a new file
#We need to take the second column of the predictions (the survival percentage)
Titanic.Train.With.Predictions <- data.frame(Titanic.Train, Prediction = Titanic.Train.RP.Preds[,2])

#Show the average prediction chance of survival for those who did live or die (Survived = 1 or 0)
#Model gives an average prediction of 27% for those who died and 61% for those who lived
aggregate(Prediction ~ Survived, data=Titanic.Train.With.Predictions, 
          FUN=function(x) {sum(x)/length(x)})

#Look at an individual result - the fifth case in the dataset
#Mr William Henry Allen did not survive (Survived = 0)
#Our model gave him a 10% chance of survival. Not very good odds! The model is doing OK here.
Titanic.Train.With.Predictions [5,]   #Square brackets mean take 5th row (then comma) show all columns

#We can save our results to a csv file
write.csv(Titanic.Train.With.Predictions, file="Titanic.Train.With.Predictions.RP.csv")

