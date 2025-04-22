# 04 - Feature Reduction - Principal Component Analysis (PCA)

from sklearn.decomposition import PCA

data = [[2, 8, 4, 5],
        [5, 3, 0.8, 1],
        [5, 4, 9, 1]]

# 1. Retain a certain number of components
# transfer = PCA(n_components=2)
# trans_data = transfer.fit_transform(data)
# print(trans_data)

# 2. Retain 95% of information
transfer = PCA(n_components=0.95)
trans_data = transfer.fit_transform(data)
print(trans_data)
