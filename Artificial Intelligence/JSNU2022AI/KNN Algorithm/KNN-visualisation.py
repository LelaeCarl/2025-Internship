import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# 1. Create synthetic 4D dataset
X, y = make_classification(
    n_samples=500,
    n_features=4,
    n_informative=4,
    n_redundant=0,
    n_clusters_per_class=1,
    n_classes=2,
    random_state=42
)

# 2. Split for training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# 4. Plot in 3D - color shows 4th dimension
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# 3D: Plot first 3 features
scatter = ax.scatter(
    X_train[:, 0], X_train[:, 1], X_train[:, 2],
    c=X_train[:, 3], cmap='coolwarm',
    s=40, edgecolor='k', alpha=0.8
)

# Axis labels
ax.set_xlabel('Feature 1')
ax.set_ylabel('Feature 2')
ax.set_zlabel('Feature 3')
cbar = fig.colorbar(scatter, ax=ax)
cbar.set_label('Feature 4 (Color mapped)')

plt.title("4D Data Visualization (3D space + color for 4th dimension)")
plt.show()
