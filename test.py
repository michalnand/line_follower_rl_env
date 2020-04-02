import numpy

def make_clusters():
    result = []

    result.append(0)
    result.append(90)
    result.append(180)
    result.append(270)

    return result


def find_clusters_ids(clusters, data):

    data_length     = len(data)
    clusters_count  = len(clusters)

    distances = numpy.zeros((clusters_count, data_length))

    for cluster_id in range(clusters_count):
        x_ref = numpy.cos(angle_ref)
        y_ref = numpy.sin(angle_ref)

        x = numpy.cos(angle)
        y = numpy.sin(angle)


        dist = (x_ref - x)**2 + (y_ref - y)**2


        distances[cluster_id] = numpy.abs(data - clusters[cluster_id])

    distances = numpy.transpose(distances)

    distances_ids = numpy.argmin(distances, axis = 1)
    print(distances_ids)


clusters    = make_clusters()
data        = numpy.random.rand(10)*360


find_clusters_ids(clusters, data)