# 01 - Linear Regression

# Steps:
# 1. Load dataset
# 2. Basic preprocessing (omitted)
# 3. Feature engineering (omitted)
# 4. Model training
# 5. Model evaluation

from sklearn.linear_model import LinearRegression

# -----------------------------
# 1. Load the dataset
# -----------------------------
# x contains midterm (weight 0.3) and final exam scores (weight 0.7)
# y contains the final grade: e.g., 80*0.3 + 86*0.7 = 84.2

x = [[80, 86],
     [82, 80],
     [85, 78],
     [90, 90],
     [86, 82],
     [82, 90],
     [78, 80],
     [92, 94]]

y = [84.2, 80.6, 80.1, 90, 83.2, 87.6, 79.4, 93.4]

# -----------------------------
# 2. Model Training
# -----------------------------
# Step 1: Instantiate estimator
estimator = LinearRegression()

# Step 2: Train the model
estimator.fit(x, y)

# -----------------------------
# 3. View coefficient
# -----------------------------
coef = estimator.coef_
print("Coefficients:\n", coef)

# -----------------------------
# 4. Prediction
# -----------------------------
# Predict final grade given [80 midterm, 100 final]
print("Prediction:\n", estimator.predict([[80, 100]]))
