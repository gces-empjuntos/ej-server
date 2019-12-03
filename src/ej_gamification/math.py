from sidekick import import_later
from sklearn.preprocessing import Imputer

from ej_clusters.math.kmeans import euclidean_distance as distance

np = import_later("numpy")

def calculate_centroids(data, labels):
   
    centroid_array = np.array()
   
    for label in label_set:
        centroid_array.append(np.mean(data[labels == label], 0))
   
   return centroid_array


def calculate_distances(distances, labels_list, centroid_index, data_index):
    label_set = labels_list[0]
    labels = labels_list[1]
    if label_set[centroid_index] == labels[data_index]:
        distances[data_index, centroid_index] = float("inf")
    else:
        distances[data_index, centroid_index] = distance(sample, centroid)


def compute_opinion_bridge_index(df, labels):
    
    labels = np.asarray(labels)
    label_set = sorted(np.unique(labels))
    k = len(label_set)
    n_samples, _ = df.shape

    data = Imputer().fit_transform(df)

    centroids = calculate_centroids(data,labels)

    distances = np.empty([n_samples, k])

    labels_list = [label_set,labels]

    for i, sample in enumerate(data):
        for j, centroid in enumerate(centroids):
            calculate_distances(distances, labels_list, j, i)
    return distances.min(axis=1)


def compute_max_opinion_bridge(size, k):
    return int(min(max(1, 0.05 * size)), k)
