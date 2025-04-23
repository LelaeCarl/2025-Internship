# 01 - Clustering Algorithm

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score

# 1. Generate dataset
# n_samples = 1000 → 1000 data points
# n_features = 2 → 2 features
# centers → 4 cluster centers
# cluster_std → spread of each cluster = 0.4
# random_state → ensures reproducibility
X, y = datasets.make_blobs(
    n_samples=1000,
    n_features=2,
    centers=[[-1, -1], [0, 0], [1, 1], [2, 2]],
    cluster_std=[0.4, 0.1, 0.1, 0.1],
    random_state=1
)

# Optional: Visualize raw data
# plt.scatter(X[:, 0], X[:, 1])
# plt.show()

# 2. Clustering with n_clusters = 4
estimator = KMeans(n_clusters=4, random_state=2)
y_pred = estimator.fit_predict(X)

# Visualize clustering result
plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.title("KMeans Clustering with 4 Clusters")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()

# Evaluate clustering quality with Calinski-Harabasz Index
print("Calinski-Harabasz Score:", calinski_harabasz_score(X, y_pred))
