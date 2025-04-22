# 03 - Feature Reduction - Feature Selection - Filter Method - Correlation Coefficients

from scipy.stats import pearsonr, spearmanr

# Pearson correlation demonstration
x1 = [12.5, 15.3, 23.2, 26.4, 33.5, 34.4, 39.4, 45.2, 55.4, 60.9]
x2 = [21.2, 23.9, 32.9, 34.1, 42.5, 43.2, 49.0, 52.8, 59.4, 63.5]

# Pearson correlation
ret = pearsonr(x1, x2)
print("Pearson correlation coefficient:\n", ret)

# Spearman correlation
ret = spearmanr(x1, x2)
print("Spearman correlation coefficient:\n", ret)
