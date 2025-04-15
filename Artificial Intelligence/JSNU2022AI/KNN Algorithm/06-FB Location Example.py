# 06 - FB Location Example
# row_id: record unique ID
# x, y: spatial coordinates
# accuracy: positioning accuracy
# time: timestamp
# place_id: predicted location label

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# 1. Load the dataset
data = pd.read_csv("./data/train.csv")

# Optional: Check basic info
# print(data.describe())
# print(data.shape)

# 2. Data preprocessing
# 2.1 Filter spatial coordinates
facebook_data = data.query("x > 2.0 & x < 2.5 & y > 2.0 & y < 2.5")
# print(facebook_data.shape)

# 2.2 Convert timestamp
# print(facebook_data['time'].head())
time = pd.to_datetime(facebook_data['time'], unit='s')
# print(time.head())

# Convert to DateTimeIndex
time = pd.DatetimeIndex(time)

# Extract hour
facebook_data['hour'] = time.hour

# Extract day
facebook_data['day'] = time.day

# Extract weekday
facebook_data['weekday'] = time.weekday

# 2.3 Filter locations with few records
place_count = facebook_data.groupby('place_id').count()

# Filter place_id with at least 4 records
place_count = place_count[place_count['row_id'] > 3]
# print(place_count.shape)

# 2.4 Keep records of valid place_id
facebook_data = facebook_data[facebook_data['place_id'].isin(place_count.index)]
print(facebook_data.shape)

# 2.5 Feature and label separation
x = facebook_data[['x', 'y', 'accuracy', 'day', 'hour', 'weekday']]
y = facebook_data['place_id']

# 2.6 Train-test split
x_train, x_test, y_train, y_test = train_test_split(
    x, y, random_state=22, test_size=0.2
)

# 3. Feature scaling
# 3.1 Instantiate scaler
transfer = StandardScaler()

# 3.2 Apply fit_transform
x_train = transfer.fit_transform(x_train)
x_test = transfer.fit_transform(x_test)

# 4. Model training with KNN + GridSearchCV
# 4.1 Instantiate estimator
estimator = KNeighborsClassifier()

# 4.2 Define hyperparameter grid
param_grid = {'n_neighbors': [1, 3, 5, 7, 9]}

estimator = GridSearchCV(
    estimator=estimator,
    param_grid=param_grid,
    cv=10,
    n_jobs=1
)

# 4.3 Train
estimator.fit(x_train, y_train)

# 5. Model evaluation
# 5.1 Predict and compare
y_pre = estimator.predict(x_test)
print("Prediction:\n", y_pre)

# 5.2 Score
score = estimator.score(x_test, y_test)
print("Accuracy score:\n", score)

# 5.3 Additional evaluation metrics
print("Best estimator:\n", estimator.best_estimator_)
print("Best score:\n", estimator.best_score_)
print("CV Results:\n", estimator.cv_results_)
