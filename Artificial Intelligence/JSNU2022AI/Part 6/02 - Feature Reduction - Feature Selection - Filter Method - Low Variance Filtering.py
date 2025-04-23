# 02 - Feature Reduction - Feature Selection - Filter Method - Low Variance Filtering

import pandas as pd
from sklearn.feature_selection import VarianceThreshold

# Feature Selection: Low Variance Filter
def var_thr():
    # 1. Load the dataset
    data = pd.read_csv("./data/factor_returns.csv")
    print(data)

    # 2. Initialize low variance filter object
    transfer = VarianceThreshold(threshold=10)

    # 3. Apply feature selection
    trans_data = transfer.fit_transform(data.iloc[:, 1:10])

    print("Shape of the data before filtering:\n", data.iloc[:, 1:10].shape)
    print("Shape of the data after filtering:\n", trans_data.shape)
    print(trans_data)

if __name__ == '__main__':
    var_thr()
