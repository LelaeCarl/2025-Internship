# 05 - Exploring User Preferences for Products with Fine-Grained Clustering

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# 1. Load datasets
order_product = pd.read_csv("./data/order_products__prior.csv")
products = pd.read_csv("./data/products.csv")
orders = pd.read_csv("./data/orders.csv")
aisles = pd.read_csv("./data/aisles.csv")

# 2. Data preprocessing
# 2.1 Merge tables
table1 = pd.merge(order_product, products, on=['product_id', 'product_id'])
table2 = pd.merge(table1, orders, on=['order_id', 'order_id'])
table = pd.merge(table2, aisles, on=['aisle_id', 'aisle_id'])

# 2.2 Generate crosstab (user vs. aisle interaction frequency)
data = pd.crosstab(table['user_id'], table['aisle'])
print("Crosstab shape: ", data.shape)

# 2.3 Subsample the data (first 1000 users)
new_data = data[:1000]

# 3. Feature engineering: dimensionality reduction via PCA
transfer = PCA(n_components=0.9)  # Preserve 90% of the variance
trans_data = transfer.fit_transform(new_data)

# 4. Machine Learning - KMeans Clustering
estimator = KMeans(n_clusters=5)  # Set number of clusters to 5
y_pre = estimator.fit_predict(trans_data)

# 5. Model Evaluation
print("Silhouette Score: ", silhouette_score(trans_data, y_pre))
