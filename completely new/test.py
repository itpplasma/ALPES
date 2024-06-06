import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Create a data matrix with NaN values representing empty spaces
data_matrix = np.array([[1, 2, np.nan],
                        [3, np.nan, 5],
                        [np.nan, 7, 8]])

# Plot the heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(data_matrix, annot=True, cmap='viridis', fmt='.1f', cbar=False)
plt.title('Heatmap with Empty Spaces')
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.show()