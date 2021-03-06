from unittest import TestCase

import numpy
import random

from HierMat.cluster import Cluster
from HierMat.cuboid import Cuboid
from HierMat.grid import Grid
from HierMat.splitable import Splitable, RegularCuboid, MinimalCuboid, Balanced


class TestSplitable(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dummy = Splitable()
        cls.lim1 = 16
        cls.lim2 = 8
        cls.lim3 = 4
        cls.link_num = 4
        cls.points1 = [(float(i) / cls.lim1,) for i in range(cls.lim1)]
        cls.links1 = {p: [cls.points1[l] for l in [random.randint(0, cls.lim1 - 1) for x in range(cls.link_num)]]
                      for p in cls.points1}
        cls.points2 = [(float(i) / cls.lim2, float(j) / cls.lim2)
                       for i in range(cls.lim2) for j in range(cls.lim2)]
        cls.links2 = {p: [cls.points2[l] for l in [random.randint(0, cls.lim2 ** 2 - 1) for x in range(cls.link_num)]]
                      for p in cls.points2}
        cls.points3 = [(float(i) / cls.lim3, float(j) / cls.lim3, float(k) / cls.lim3)
                       for i in range(cls.lim3) for j in range(cls.lim3) for k in range(cls.lim3)]
        cls.links3 = {p: [cls.points3[l] for l in [random.randint(0, cls.lim3 ** 3 - 1) for x in range(cls.link_num)]]
                      for p in cls.points3}
        cls.grid1 = Grid(cls.points1, cls.links1)
        cls.grid2 = Grid(cls.points2, cls.links2)
        cls.grid3 = Grid(cls.points3, cls.links3)
        cls.cluster1 = Cluster(cls.grid1)
        cls.cluster2 = Cluster(cls.grid2)
        cls.cluster3 = Cluster(cls.grid3)
        cls.rc1 = RegularCuboid(cls.cluster1)
        cls.rc2 = RegularCuboid(cls.cluster2)
        cls.rc3 = RegularCuboid(cls.cluster3)
        cls.mc1 = MinimalCuboid(cls.cluster1)
        cls.mc2 = MinimalCuboid(cls.cluster2)
        cls.mc3 = MinimalCuboid(cls.cluster3)
        cls.ba1 = Balanced(cls.cluster1)
        cls.ba2 = Balanced(cls.cluster2)
        cls.ba3 = Balanced(cls.cluster3)

    def test_init(self):
        self.assertIsInstance(self.rc1, RegularCuboid)
        self.assertIsInstance(self.rc2, RegularCuboid)
        self.assertIsInstance(self.rc3, RegularCuboid)
        self.assertIsInstance(self.mc1, MinimalCuboid)
        self.assertIsInstance(self.mc2, MinimalCuboid)
        self.assertIsInstance(self.mc3, MinimalCuboid)
        self.assertIsInstance(self.rc1, Splitable)
        self.assertIsInstance(self.mc1, Splitable)
        self.assertIsInstance(self.mc1, RegularCuboid)
        self.assertIsInstance(self.ba1, Balanced)
        self.assertIsInstance(self.ba2, Balanced)
        self.assertIsInstance(self.ba3, Balanced)
        self.assertIsInstance(self.ba1, Splitable)

    def test_len(self):
        self.assertEqual(len(self.rc1), self.lim1)
        self.assertEqual(len(self.rc2), self.lim2 ** 2)
        self.assertEqual(len(self.rc3), self.lim3 ** 3)
        self.assertEqual(len(self.mc1), self.lim1)
        self.assertEqual(len(self.mc2), self.lim2 ** 2)
        self.assertEqual(len(self.mc3), self.lim3 ** 3)
        self.assertEqual(len(self.ba1), self.lim1)
        self.assertEqual(len(self.ba2), self.lim2 ** 2)
        self.assertEqual(len(self.ba3), self.lim3 ** 3)

    def test_repr(self):
        check = "<Splitable with cluster None>"
        self.assertEqual(check, self.dummy.__repr__())
        check = "<RegularCuboid with cluster {0} and cuboid {1}>".format(self.cluster1, self.rc1.cuboid)
        self.assertEqual(check, self.rc1.__repr__())
        check = "<RegularCuboid with cluster {0} and cuboid {1}>".format(self.cluster2, self.rc2.cuboid)
        self.assertEqual(check, self.rc2.__repr__())
        check = "<RegularCuboid with cluster {0} and cuboid {1}>".format(self.cluster3, self.rc3.cuboid)
        self.assertEqual(check, self.rc3.__repr__())
        check = "<MinimalCuboid with cluster {0} and cuboid {1}>".format(self.cluster1, self.mc1.cuboid)
        self.assertEqual(check, self.mc1.__repr__())
        check = "<MinimalCuboid with cluster {0} and cuboid {1}>".format(self.cluster2, self.mc2.cuboid)
        self.assertEqual(check, self.mc2.__repr__())
        check = "<MinimalCuboid with cluster {0} and cuboid {1}>".format(self.cluster3, self.mc3.cuboid)
        self.assertEqual(check, self.mc3.__repr__())
        check = "<Balanced with cluster {0}>".format(self.cluster1)
        self.assertEqual(check, self.ba1.__repr__())
        check = "<Balanced with cluster {0}>".format(self.cluster2)
        self.assertEqual(check, self.ba2.__repr__())
        check = "<Balanced with cluster {0}>".format(self.cluster3)
        self.assertEqual(check, self.ba3.__repr__())

    def test_iter(self):
        check = [p for p in self.rc1]
        self.assertEqual(check, self.points1)
        iterator = self.rc1.__iter__()
        iteriter = iterator.__iter__()
        self.assertEqual(iterator, iteriter)
        check = [p for p in self.rc2]
        self.assertEqual(check, self.points2)
        iterator = self.rc2.__iter__()
        iteriter = iterator.__iter__()
        self.assertEqual(iterator, iteriter)
        check = [p for p in self.rc3]
        self.assertEqual(check, self.points3)
        iterator = self.rc3.__iter__()
        iteriter = iterator.__iter__()
        self.assertEqual(iterator, iteriter)

    def test_getitem(self):
        i = random.randint(0, self.lim1 - 1)
        self.assertEqual(self.rc1[i], self.points1[i])
        i = random.randint(0, self.lim2 ** 2 - 1)
        self.assertTrue(numpy.array_equal(self.rc2[i], self.points2[i]))
        i = random.randint(0, self.lim3 ** 3 - 1)
        self.assertTrue(numpy.array_equal(self.rc3[i], self.points3[i]))
        i = random.randint(0, self.lim1 - 1)
        self.assertEqual(self.mc1[i], self.points1[i])
        i = random.randint(0, self.lim2 ** 2 - 1)
        self.assertTrue(numpy.array_equal(self.mc2[i], self.points2[i]))
        i = random.randint(0, self.lim3 ** 3 - 1)
        self.assertTrue(numpy.array_equal(self.mc3[i], self.points3[i]))
        i = random.randint(0, self.lim1 - 1)
        self.assertEqual(self.ba1[i], self.points1[i])
        i = random.randint(0, self.lim2 ** 2 - 1)
        self.assertTrue(numpy.array_equal(self.ba2[i], self.points2[i]))
        i = random.randint(0, self.lim3 ** 3 - 1)
        self.assertTrue(numpy.array_equal(self.ba3[i], self.points3[i]))

    def test_get_index(self):
        self.assertEqual(self.rc1.get_index(0), self.cluster1.get_index(0))
        self.assertEqual(self.rc1.get_index(-1), self.cluster1.get_index(-1))
        self.assertEqual(self.rc2.get_index(0), self.cluster2.get_index(0))
        self.assertEqual(self.rc2.get_index(-1), self.cluster2.get_index(-1))
        self.assertEqual(self.rc3.get_index(0), self.cluster3.get_index(0))
        self.assertEqual(self.rc3.get_index(-1), self.cluster3.get_index(-1))
        self.assertEqual(self.mc1.get_index(0), self.cluster1.get_index(0))
        self.assertEqual(self.mc1.get_index(-1), self.cluster1.get_index(-1))
        self.assertEqual(self.mc2.get_index(0), self.cluster2.get_index(0))
        self.assertEqual(self.mc2.get_index(-1), self.cluster2.get_index(-1))
        self.assertEqual(self.mc3.get_index(0), self.cluster3.get_index(0))
        self.assertEqual(self.mc3.get_index(-1), self.cluster3.get_index(-1))
        self.assertEqual(self.ba1.get_index(0), self.cluster1.get_index(0))
        self.assertEqual(self.ba1.get_index(-1), self.cluster1.get_index(-1))
        self.assertEqual(self.ba2.get_index(0), self.cluster2.get_index(0))
        self.assertEqual(self.ba2.get_index(-1), self.cluster2.get_index(-1))
        self.assertEqual(self.ba3.get_index(0), self.cluster3.get_index(0))
        self.assertEqual(self.ba3.get_index(-1), self.cluster3.get_index(-1))

    def test_get_grid_item(self):
        self.assertEqual(self.rc1.get_grid_item(0), self.grid1[0])
        self.assertEqual(self.rc1.get_grid_item(-1), self.grid1[-1])
        self.assertTrue(numpy.array_equal(self.rc2.get_grid_item(0), self.grid2[0]))
        self.assertTrue(numpy.array_equal(self.rc2.get_grid_item(-1), self.grid2[-1]))
        self.assertTrue(numpy.array_equal(self.rc3.get_grid_item(0), self.grid3[0]))
        self.assertTrue(numpy.array_equal(self.rc3.get_grid_item(-1), self.grid3[-1]))
        self.assertEqual(self.mc1.get_grid_item(0), self.grid1[0])
        self.assertEqual(self.mc1.get_grid_item(-1), self.grid1[-1])
        self.assertTrue(numpy.array_equal(self.mc2.get_grid_item(0), self.grid2[0]))
        self.assertTrue(numpy.array_equal(self.mc2.get_grid_item(-1), self.grid2[-1]))
        self.assertTrue(numpy.array_equal(self.mc3.get_grid_item(0), self.grid3[0]))
        self.assertTrue(numpy.array_equal(self.mc3.get_grid_item(-1), self.grid3[-1]))
        self.assertEqual(self.ba1.get_grid_item(0), self.grid1[0])
        self.assertEqual(self.ba1.get_grid_item(-1), self.grid1[-1])
        self.assertTrue(numpy.array_equal(self.ba2.get_grid_item(0), self.grid2[0]))
        self.assertTrue(numpy.array_equal(self.ba2.get_grid_item(-1), self.grid2[-1]))
        self.assertTrue(numpy.array_equal(self.ba3.get_grid_item(0), self.grid3[0]))
        self.assertTrue(numpy.array_equal(self.ba3.get_grid_item(-1), self.grid3[-1]))

    def test_get_patch_coordinates(self):
        coordinates = self.rc1.get_patch_coordinates()
        self.assertEqual(coordinates[0], 0)
        self.assertEqual(coordinates[1], self.lim1 - 1)
        coordinates = self.rc2.get_patch_coordinates()
        self.assertEqual(coordinates[0], 0)
        self.assertEqual(coordinates[1], self.lim2 ** 2 - 1)
        coordinates = self.rc3.get_patch_coordinates()
        self.assertEqual(coordinates[0], 0)
        self.assertEqual(coordinates[1], self.lim3 ** 3 - 1)
        coordinates = self.mc1.get_patch_coordinates()
        self.assertEqual(coordinates[0], 0)
        self.assertEqual(coordinates[1], self.lim1 - 1)
        coordinates = self.mc2.get_patch_coordinates()
        self.assertEqual(coordinates[0], 0)
        self.assertEqual(coordinates[1], self.lim2 ** 2 - 1)
        coordinates = self.mc3.get_patch_coordinates()
        self.assertEqual(coordinates[0], 0)
        self.assertEqual(coordinates[1], self.lim3 ** 3 - 1)
        coordinates = self.ba1.get_patch_coordinates()
        self.assertEqual(coordinates[0], 0)
        self.assertEqual(coordinates[1], self.lim1 - 1)
        coordinates = self.ba2.get_patch_coordinates()
        self.assertEqual(coordinates[0], 0)
        self.assertEqual(coordinates[1], self.lim2 ** 2 - 1)
        coordinates = self. ba3.get_patch_coordinates()
        self.assertEqual(coordinates[0], 0)
        self.assertEqual(coordinates[1], self.lim3 ** 3 - 1)

    def test_get_grid_item_support(self):
        self.assertEqual(self.rc1.get_grid_item_support(self.points1[0]),
                         self.grid1.get_support_by_index(0))
        self.assertEqual(self.rc1.get_grid_item_support(self.points1[-1]),
                         self.grid1.get_support_by_index(-1))
        self.assertTrue(numpy.array_equal(self.rc2.get_grid_item_support(self.points2[0]),
                                          self.grid2.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.rc2.get_grid_item_support(self.points2[-1]),
                                          self.grid2.get_support_by_index(-1)))
        self.assertTrue(numpy.array_equal(self.rc3.get_grid_item_support(self.points3[0]),
                                          self.grid3.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.rc3.get_grid_item_support(self.points3[-1]),
                                          self.grid3.get_support_by_index(-1)))
        self.assertEqual(self.mc1.get_grid_item_support(self.points1[0]),
                         self.grid1.get_support_by_index(0))
        self.assertEqual(self.mc1.get_grid_item_support(self.points1[-1]),
                         self.grid1.get_support_by_index(-1))
        self.assertTrue(numpy.array_equal(self.mc2.get_grid_item_support(self.points2[0]),
                                          self.grid2.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.mc2.get_grid_item_support(self.points2[-1]),
                                          self.grid2.get_support_by_index(-1)))
        self.assertTrue(numpy.array_equal(self.mc3.get_grid_item_support(self.points3[0]),
                                          self.grid3.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.mc3.get_grid_item_support(self.points3[-1]),
                                          self.grid3.get_support_by_index(-1)))
        self.assertEqual(self.ba1.get_grid_item_support(self.points1[0]),
                         self.grid1.get_support_by_index(0))
        self.assertEqual(self.ba1.get_grid_item_support(self.points1[-1]),
                         self.grid1.get_support_by_index(-1))
        self.assertTrue(numpy.array_equal(self.ba2.get_grid_item_support(self.points2[0]),
                                          self.grid2.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.ba2.get_grid_item_support(self.points2[-1]),
                                          self.grid2.get_support_by_index(-1)))
        self.assertTrue(numpy.array_equal(self.ba3.get_grid_item_support(self.points3[0]),
                                          self.grid3.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.ba3.get_grid_item_support(self.points3[-1]),
                                          self.grid3.get_support_by_index(-1)))

    def test_get_grid_item_support_by_index(self):
        self.assertEqual(self.rc1.get_grid_item_support_by_index(0),
                         self.grid1.get_support_by_index(0))
        self.assertEqual(self.rc1.get_grid_item_support_by_index(-1),
                         self.grid1.get_support_by_index(-1))
        self.assertTrue(numpy.array_equal(self.rc2.get_grid_item_support_by_index(0),
                                          self.grid2.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.rc2.get_grid_item_support_by_index(-1),
                                          self.grid2.get_support_by_index(-1)))
        self.assertTrue(numpy.array_equal(self.rc3.get_grid_item_support_by_index(0),
                                          self.grid3.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.rc3.get_grid_item_support_by_index(-1),
                                          self.grid3.get_support_by_index(-1)))
        self.assertEqual(self.mc1.get_grid_item_support_by_index(0),
                         self.grid1.get_support_by_index(0))
        self.assertEqual(self.mc1.get_grid_item_support_by_index(-1),
                         self.grid1.get_support_by_index(-1))
        self.assertTrue(numpy.array_equal(self.mc2.get_grid_item_support_by_index(0),
                                          self.grid2.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.mc2.get_grid_item_support_by_index(-1),
                                          self.grid2.get_support_by_index(-1)))
        self.assertTrue(numpy.array_equal(self.mc3.get_grid_item_support_by_index(0),
                                          self.grid3.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.mc3.get_grid_item_support_by_index(-1),
                                          self.grid3.get_support_by_index(-1)))
        self.assertEqual(self.ba1.get_grid_item_support_by_index(0),
                         self.grid1.get_support_by_index(0))
        self.assertEqual(self.ba1.get_grid_item_support_by_index(-1),
                         self.grid1.get_support_by_index(-1))
        self.assertTrue(numpy.array_equal(self.ba2.get_grid_item_support_by_index(0),
                                          self.grid2.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.ba2.get_grid_item_support_by_index(-1),
                                          self.grid2.get_support_by_index(-1)))
        self.assertTrue(numpy.array_equal(self.ba3.get_grid_item_support_by_index(0),
                                          self.grid3.get_support_by_index(0)))
        self.assertTrue(numpy.array_equal(self.ba3.get_grid_item_support_by_index(-1),
                                          self.grid3.get_support_by_index(-1)))

    def test_eq(self):
        self.assertRaises(NotImplementedError, self.dummy.__eq__, self.dummy)
        self.assertEqual(self.rc1, self.rc1)
        self.assertFalse(self.rc1 == self.rc2)
        self.assertEqual(self.rc2, self.rc2)
        self.assertFalse(self.rc2 == self.rc3)
        self.assertEqual(self.rc3, self.rc3)
        self.assertFalse(self.rc3 == self.rc1)
        self.assertEqual(self.mc1, self.mc1)
        self.assertFalse(self.mc1 == self.mc2)
        self.assertEqual(self.mc2, self.mc2)
        self.assertFalse(self.mc2 == self.mc3)
        self.assertEqual(self.mc3, self.mc3)
        self.assertFalse(self.mc3 == self.mc1)
        self.assertEqual(self.ba1, self.ba1)
        self.assertFalse(self.ba1 == self.ba2)
        self.assertEqual(self.ba2, self.ba2)
        self.assertFalse(self.ba2 == self.ba3)
        self.assertEqual(self.ba3, self.ba3)
        self.assertFalse(self.ba3 == self.ba1)

    def test_ne(self):
        self.assertRaises(NotImplementedError, self.dummy.__ne__, self.dummy)
        self.assertNotEqual(self.rc1, self.rc2)
        self.assertFalse(self.rc1 != self.rc1)
        self.assertNotEqual(self.rc2, self.rc3)
        self.assertFalse(self.rc2 != self.rc2)
        self.assertNotEqual(self.rc3, self.rc1)
        self.assertFalse(self.rc3 != self.rc3)

    def test_split(self):
        self.assertRaises(NotImplementedError, self.dummy.split)
        left_cluster = Cluster(self.grid1, self.cluster1.indices[:self.lim1 / 2])
        right_cluster = Cluster(self.grid1, self.cluster1.indices[self.lim1 / 2:])
        left_cub = Cuboid(numpy.array([0]), numpy.array([float(self.lim1 - 1) / (2 * self.lim1)]))
        right_cub = Cuboid(numpy.array([float(self.lim1 - 1) / (2 * self.lim1)]),
                           numpy.array([float(self.lim1 - 1) / self.lim1]))
        left_rc = RegularCuboid(left_cluster, left_cub)
        right_rc = RegularCuboid(right_cluster, right_cub)
        left_split, right_split = self.rc1.split()
        self.assertEqual(left_rc, left_split)
        self.assertEqual(right_rc, right_split)
        left_split, right_split = self.mc1.split()
        left_mc = MinimalCuboid(left_cluster)
        right_mc = MinimalCuboid(right_cluster)
        self.assertEqual(left_split, left_mc)
        self.assertEqual(right_split, right_mc)
        left_split, right_split = self.ba1.split()
        left_ba = Balanced(left_cluster)
        right_ba = Balanced(right_cluster)
        self.assertEqual(left_ba, left_split)
        self.assertEqual(right_ba, right_split)
        left_cluster = Cluster(self.grid2, self.cluster2.indices[:self.lim2 ** 2 / 2])
        right_cluster = Cluster(self.grid2, self.cluster2.indices[self.lim2 ** 2 / 2:])
        left_cub = Cuboid(numpy.array([0, 0]),
                          numpy.array([float(self.lim2 - 1) / (2 * self.lim2), float(self.lim2 - 1) / self.lim2]))
        right_cub = Cuboid(numpy.array([float(self.lim2 - 1) / (2 * self.lim2), 0]),
                           numpy.array([float(self.lim2 - 1) / self.lim2, float(self.lim2 - 1) / self.lim2]))
        left_rc = RegularCuboid(left_cluster, left_cub)
        right_rc = RegularCuboid(right_cluster, right_cub)
        left_split, right_split = self.rc2.split()
        self.assertEqual(left_rc, left_split)
        self.assertEqual(right_rc, right_split)
        left_split, right_split = self.mc2.split()
        left_mc = MinimalCuboid(left_cluster)
        right_mc = MinimalCuboid(right_cluster)
        self.assertEqual(left_mc, left_split)
        self.assertEqual(right_mc, right_split)
        left_split, right_split = self.ba2.split()
        left_ba = Balanced(left_cluster)
        right_ba = Balanced(right_cluster)
        self.assertEqual(left_ba, left_split)
        self.assertEqual(right_ba, right_split)
        left_cluster = Cluster(self.grid3, self.cluster2.indices[:self.lim3 ** 3 / 2])
        right_cluster = Cluster(self.grid3, self.cluster2.indices[self.lim3 ** 3 / 2:])
        left_cub = Cuboid(numpy.array([0, 0, 0]),
                          numpy.array([float(self.lim3 - 1) / (2 * self.lim3),
                                       float(self.lim3 - 1) / self.lim3,
                                       float(self.lim3 - 1) / self.lim3]))
        right_cub = Cuboid(numpy.array([float(self.lim3 - 1) / (2 * self.lim3), 0, 0]),
                           numpy.array([float(self.lim3 - 1) / self.lim3,
                                        float(self.lim3 - 1) / self.lim3,
                                        float(self.lim3 - 1) / self.lim3]))
        left_rc = RegularCuboid(left_cluster, left_cub)
        right_rc = RegularCuboid(right_cluster, right_cub)
        left_split, right_split = self.rc3.split()
        self.assertEqual(left_rc, left_split)
        self.assertEqual(right_rc, right_split)
        left_split, right_split = self.mc3.split()
        left_mc = MinimalCuboid(left_cluster)
        right_mc = MinimalCuboid(right_cluster)
        self.assertEqual(left_mc, left_split)
        self.assertEqual(right_mc, right_split)
        left_split, right_split = self.ba3.split()
        left_ba = Balanced(left_cluster)
        right_ba = Balanced(right_cluster)
        self.assertEqual(left_ba, left_split)
        self.assertEqual(right_ba, right_split)
        grid = Grid([0, 1, 5], [[1], [5], [0]])
        clust = Cluster(grid)
        regcub = RegularCuboid(clust)
        split1, split2 = regcub.split()
        split3 = split1.split()
        split4 = split2.split()
        self.assertEqual(len(split3), 1)
        self.assertEqual(len(split4), 1)
        test_ba = Balanced(split4[0].cluster)
        self.assertEqual(test_ba.split(), test_ba)

    def test_diameter(self):
        self.assertRaises(NotImplementedError, self.dummy.diameter)
        check = numpy.linalg.norm(numpy.array([float(self.lim1 - 1) / self.lim1]))
        self.assertEqual(self.rc1.diameter(), check)
        self.assertEqual(self.mc1.diameter(), check)
        self.assertEqual(self.ba1.diameter(), check)
        check = numpy.linalg.norm(numpy.array([float(self.lim2 - 1) / self.lim2, float(self.lim2 - 1) / self.lim2]))
        self.assertEqual(self.rc2.diameter(), check)
        self.assertEqual(self.mc2.diameter(), check)
        self.assertEqual(self.ba2.diameter(), check)
        check = numpy.linalg.norm(numpy.array([float(self.lim3 - 1) / self.lim3, float(self.lim3 - 1) / self.lim3,
                                               float(self.lim3 - 1) / self.lim3]))
        self.assertEqual(self.rc3.diameter(), check)
        self.assertEqual(self.mc3.diameter(), check)
        self.assertEqual(self.ba3.diameter(), check)

    def test_distance(self):
        self.assertRaises(NotImplementedError, self.dummy.distance, self.dummy)
        dist_check = numpy.linalg.norm(numpy.array([2 - float(self.lim1 - 1) / self.lim1]))
        dist_points = [numpy.array([2 + float(i) / self.lim1]) for i in range(self.lim1)]
        dist_links = [[dist_points[l] for l in [random.randint(0, self.lim1 - 1) for x in range(self.link_num)]]
                      for i in range(self.lim1)]
        dist_grid = Grid(dist_points, dist_links)
        dist_cluster = Cluster(dist_grid)
        dist_rc = RegularCuboid(dist_cluster)
        self.assertEqual(self.rc1.distance(dist_rc), dist_check)
        self.assertEqual(self.mc1.distance(dist_rc), dist_check)
        self.assertEqual(self.ba1.distance(dist_rc), dist_check)
        dist_points = [numpy.array([2 + float(i) / self.lim2, 2 + float(j) / self.lim2])
                       for i in range(self.lim2) for j in range(self.lim2)]
        dist_links = [[dist_points[l] for l in [random.randint(0, (self.lim2 - 1) ** 2)
                                                for x in range(self.link_num)]]
                      for j in range(self.lim2) for i in range(self.lim2)]
        dist_grid = Grid(dist_points, dist_links)
        dist_cluster = Cluster(dist_grid)
        dist_check = numpy.linalg.norm(numpy.array([2 - float(self.lim2 - 1) / self.lim2,
                                                    2 - float(self.lim2 - 1) / self.lim2]))
        dist_rc = RegularCuboid(dist_cluster)
        self.assertEqual(self.rc2.distance(dist_rc), dist_check)
        self.assertEqual(self.mc2.distance(dist_rc), dist_check)
        self.assertEqual(self.ba2.distance(dist_rc), dist_check)
        dist_points = [numpy.array([2 + float(i) / self.lim3, 2 + float(j) / self.lim3, 2 + float(k) / self.lim3])
                       for i in range(self.lim3) for j in range(self.lim3) for k in range(self.lim3)]
        dist_links = [[dist_points[l] for l in [random.randint(0, (self.lim3 - 1) ** 3)
                                                for x in range(self.link_num)]]
                      for k in range(self.lim3) for j in range(self.lim3) for i in range(self.lim3)]
        dist_grid = Grid(dist_points, dist_links)
        dist_cluster = Cluster(dist_grid)
        dist_check = numpy.linalg.norm(numpy.array([2 - float(self.lim3 - 1) / self.lim3,
                                                    2 - float(self.lim3 - 1) / self.lim3,
                                                    2 - float(self.lim3 - 1) / self.lim3]))
        dist_rc = RegularCuboid(dist_cluster)
        self.assertEqual(self.rc3.distance(dist_rc), dist_check)
        self.assertEqual(self.mc3.distance(dist_rc), dist_check)
        self.assertEqual(self.ba3.distance(dist_rc), dist_check)
