# 03 - Feature Preprocessing

# MinMaxScaler - Normalization
# StandardScaler - Standardization

from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd

# 1. Read file
data = pd.read_csv("./data/dating.txt")
print(data)

'''
1. Normalization
fit_transform: Apply a uniform transformation to the data
(e.g. scale data to ~N(0,1) or project it into a fixed interval)

fit: Calculate metrics like mean, std, max, min from training data
transform: Perform normalization, scaling, dimensionality reduction, etc., based on fit
'''

# 1.1 Instantiate a scaler
# transfer = MinMaxScaler(feature_range=(0, 10))

# 1.2 Call fit_transform method
# minmax_data = transfer.fit_transform(
#     data[['milage', 'Liters', 'Consumtime']]
# )

# 1.3 Result after normalization
# print("Normalized data:\n", minmax_data)

'''
2. Standardization
'''

# 2.1 Instantiate a scaler
transfer = StandardScaler()

# 2.2 Call fit_transform method
minmax_data = transfer.fit_transform(
    data[['milage', 'Liters', 'Consumtime']]
)

# 2.3 Output results
print("Data after standardization:\n", minmax_data)
print("Mean of each feature:\n", minmax_data.mean())
print("Variance of each feature:\n", minmax_data.var())
