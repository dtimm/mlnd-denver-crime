import pandas as pd
import numpy as np
import sklearn.metrics as sk

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeRegressor

# perform some sort of analysis on the crime_weather.csv data

crime_weather = pd.read_csv('data/crime_weather.csv')

crimes = crime_weather.columns.tolist()[12:]
target = crime_weather[crimes]
crime_weather.drop(crimes, axis=1, inplace=True)
crime_weather.drop('Date', axis=1, inplace=True)
crime_weather.fillna(0.0, inplace=True)

today = []
for i in xrange(16):
    today.append([i, 15, 88, 8, 29.72, 74, 10, 24, 62, 6, 4])

today = pd.DataFrame(today)

X_tr, X_ts, y_tr, y_ts = train_test_split(crime_weather, target, test_size=0.33, random_state=42)

scale = StandardScaler()
scale.fit(X_tr)

X_tr = scale.transform(X_tr)
X_ts = scale.transform(X_ts)
today = scale.transform(today)

# perform grid search to optimize parameters
reg = DecisionTreeRegressor(random_state=42, max_depth=7, min_samples_split=50)
params = {}
'''params = { 
            'max_depth':[2, 5, 7, 10],
            'min_samples_split':[20,30,50],
            'max_features':[None]
         }'''
gscv = GridSearchCV(reg, params, cv=5)

gscv.fit(X_tr, y_tr)

print gscv.best_estimator_

print 'TR Score: {0}'.format(gscv.score(X_tr, y_tr))
print 'TS Score: {0}'.format(gscv.score(X_ts, y_ts))
#print 'Today: {0}'.format(pd.DataFrame(gscv.predict(today), columns=crimes))
#print pd.DataFrame(gscv.predict(X_ts)).describe()
#print pd.DataFrame(y_ts).describe()