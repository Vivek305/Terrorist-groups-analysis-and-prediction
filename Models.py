
# coding: utf-8

# ## Predicting Group Responsible

# ## Preparation

# In[1]:


#get_ipython().run_line_magic('matplotlib', 'inline')

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

import pandas as pd
import numpy as np
import time
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV


# In[2]:


#from IPython.display import display

if config.getboolean('Booleans', 'UseLessFeatures') == True:
    n_features = 5
else:
    n_features = 11

gtd = pd.read_csv('gtd_processed_%dfeatures.csv' % n_features, encoding='latin1', low_memory=False)

#display(gtd.tail(5))
gtd.shape


# Split-out validation dataset

# ## Data Partitioning

# In[3]:


array = gtd.values
seed = 188
X = array[:,1:]
Y = array[:,0]
validation_size = 0.10
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)


# ## Model Building

# In[4]:


models = []

models.append(('CART', DecisionTreeClassifier()))
#specified from "Tuning Hyperparameters with Randomized Search" below
models.append(('KNN', KNeighborsClassifier(n_neighbors=5, metric='cityblock')))

if config.getboolean('Booleans', 'RunPoorPerformingClassifiers') == True:
    models.append(('GNB', GaussianNB())) # GNB: 0.353792% (0.002758) - 9.339 seconds
    models.append(('LDA', LinearDiscriminantAnalysis())) #LDA: 0.285051% (0.004282) - 5.299 seconds

if config.getboolean('Booleans', 'RunRandomForest') == True:
    models.append(('RF', RandomForestClassifier()))

if config.getboolean('Booleans', 'RunSVM') == True:
    models.append(('SVM', SVC(probability=True))) #Too slow for this many samples - O(N^3)

results = []
names = []
scoring = 'accuracy'

for name, model in models:
    start_time = time.time()
    kfold = model_selection.KFold(n_splits=20, random_state=seed) #ensure same seed so models are directly comparable
    cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f%% (%f) - %s seconds" % (name, cv_results.mean(), cv_results.std(), round((time.time() - start_time),3))
    print(msg)


# ## Compare Algorithms

# In[5]:


fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()


# In[6]:


knn = KNeighborsClassifier()


# tune the hyperparameters via a randomized search:

# In[7]:


knnParams = {"n_neighbors": np.arange(1, 31, 2), #k-NN = odd integers in the range [0, 29]
          "metric": ["euclidean", "cityblock"]} #both the Euclidean distance and Manhattan/City block distance


# In[8]:


grid = RandomizedSearchCV(knn, knnParams)
start = time.time()
grid.fit(X_train, Y_train)


# evaluate the best randomized searched model on the testing data:

# In[9]:


print("[INFO] randomized search took {:.2f} seconds".format(
    time.time() - start))
acc = grid.score(X_validation, Y_validation)
print("[INFO] grid search accuracy: {:.2f}%".format(acc * 100))
print("[INFO] randomized search best parameters: {}".format(
    grid.best_params_))


# ## Make predictions on validation dataset

# In[10]:


cart = DecisionTreeClassifier()
cart.fit(X_train, Y_train)
predictions = cart.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))


# In[14]:


iyear = 2018
country = 140
crit1 = 1
crit2 = 1
crit3 = 1
attacktype1 = 12
targtype1 = 7
targsubtype1 = 45
weaptype1 = 13
weapsubtype1 = 0
ransom = 1


if n_features == 5:
    X = [iyear, country, attacktype1, targtype1, weaptype1],
else:
    X = [iyear, country, crit1, crit2, crit3, attacktype1, targtype1, targsubtype1, weaptype1, weapsubtype1, ransom], #TODO: reshape to 1D array

print(cart.predict(X))
# print cart.predict_proba(X)
