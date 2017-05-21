import argparse
import random
from timeit import default_timer as timer

import numpy as np
from block_cluster_tree import BlockClusterTree
from cluster import Cluster
from cluster_tree import ClusterTree
from profilehooks import profile

from HierMat.grid import Grid
from HierMat.splitable import RegularCuboid


@profile
def main(args):
    lim1 = 0
    lim2 = 0
    lim3 = 0
    if args.dimension >= 1:
        lim1 = args.limit
    if args.dimension >= 2:
        lim2 = args.limit
    if args.dimension == 3:
        lim3 = args.limit if args.dimension > 2 else 0
    link_num = 2
    if args.dimension == 1:
        points = [np.array([float(i) / lim1]) for i in range(lim1)]
        links = [[points[l] for l in [random.randint(0, lim1 - 1) for x in range(link_num)]] for i in range(lim1)]
    elif args.dimension == 2:
        points = [np.array([float(i) / lim1, float(j) / lim2]) for i in range(lim1) for j in range(lim2)]
        links = [[points[l] for l in [random.randint(0, lim1 * lim2 - 2) for x in range(link_num)]]
                 for i in range(lim1) for j in range(lim2)]
    else:
        points = [np.array([float(i) / lim1, float(j) / lim2, float(k) / lim3]) for i in range(lim1) for j in
                  range(lim2) for k in range(lim3)]
        links = [[points[l] for l in [random.randint(0, lim1 * lim2 * lim3 - 1) for x in range(link_num)]]
                 for k in range(lim3) for j in range(lim2) for i in range(lim1)]
    grid = Grid(points, links)
    cluster = Cluster(grid)
    rc = RegularCuboid(cluster)
    start = timer()
    ct = ClusterTree(rc, 1)
    end = timer()
    print("ClusterTree build-up took " + str(end - start))
    start = timer()
    bct = BlockClusterTree(ct, ct)
    end = timer()
    print("BlockClusterTree buil-up took " + str(end - start))

if __name__ == '__main__':
    parser = argparse.ArgumentParser("HMatrix Profiler")
    parser.add_argument("dimension", type=int, choices=[1, 2, 3])
    parser.add_argument("limit", type=int)
    args = parser.parse_args()
    main(args)