import pickle

with open('my_dumped_classifier.pkl', 'rb') as fid:
    model_loaded = pickle.load(fid)

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


    #if n_features == 5:
    X = [iyear, country, attacktype1, targtype1, weaptype1],
    #else:
        #X = [iyear, country, crit1, crit2, crit3, attacktype1, targtype1, targsubtype1, weaptype1, weapsubtype1, ransom], #TODO: reshape to 1D array

    print(model_loaded.predict(X))
