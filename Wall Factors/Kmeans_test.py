from sklearn.cluster import KMeans
import numpy as np

## Data Set
X = np.array([[1, 2], [1, 4], [1, 0],[10, 2], [10, 4], [10, 0]])

## Perform KMeans with 2 clusters and random initial position
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)

## Index of cluster each data point belongs to
kmeans.labels_
# Output: array([1, 1, 1, 0, 0, 0], dtype=int32)

## Predict the closest cluster each input belongs to.
kmeans.predict([[0, 0], [12, 3]])
#Output: array([1, 0], dtype=int32)


## Cluster centers (coordinates to pass to path finding algorithm)
kmeans.cluster_centers_
#Output: array([[10.,  2.],[ 1.,  2.]])

test = np.int_(kmeans.cluster_centers_)
print(test, type(test))