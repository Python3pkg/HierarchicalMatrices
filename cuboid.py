"""cuboid.py: :class:`Cuboid` and :func:`minimal_cuboid`
"""
import numpy
from numpy.core.multiarray import array


class Cuboid(object):
    """Cuboid that is parallel to the axis in Cartesian coordinates.

    Characterized by two diagonal corners.

    - **Attributes**:

        low_corner: numpy.array with minimal values in each dimension

        high_corner: numpy.array with maximal values in each dimension
    """
    def __init__(self, low_corner, high_corner):
        """Build a cuboid.

        :param low_corner: low corner
        :type low_corner: numpy.array
        :param high_corner: high corner
        :type high_corner: numpy.array
        """
        self.low_corner = array(low_corner, float)
        self.high_corner = array(high_corner, float)

    def __eq__(self, other):
        """Test for equality

        :param other: other cuboid
        :type other: Cuboid
        :return: equal
        :rtype: bool
        """
        low_eq = self.low_corner == other.low_corner
        high_eq = self.high_corner == other.high_corner
        return low_eq.all() and high_eq.all()

    def __contains__(self, point):
        """Check if point is inside the cuboid

        True if point is between low_corner and high_corner

        :param point: point of correct dimension
        :type point: numpy.array

        :return: contained
        :rtype: bool
        """
        lower = self.low_corner <= point
        higher = point <= self.high_corner
        return lower.all() and higher.all()

    def __repr__(self):
        """Representation of Cuboid"""
        return "Cuboid({0},{1})".format(str(self.low_corner), str(self.high_corner))

    def __str__(self):
        """Return string representation"""
        return "Cuboid with:\n\tlow corner: {0},\n\thigh corner{1}.".format(str(self.low_corner),
                                                                            str(self.high_corner))

    def split(self, axis=None):
        """Split the cuboid in half

        If axis is specified, the cuboid is split along the given axis, else the maximal axis is chosen.

        :param axis: axis along which to split (optional)
        :type axis: int
        :return: cuboid1, cuboid2
        :rtype: tuple(Cuboid, Cuboid)
        """
        if axis:
            index = axis
        else:
            # determine dimension in which to split
            index = numpy.argmax(abs(self.high_corner - self.low_corner))
        # determine value at splitting point
        split = (self.high_corner[index] + self.low_corner[index]) / 2
        low_corner1 = array(self.low_corner)
        low_corner2 = array(self.low_corner)
        low_corner2[index] = split
        high_corner1 = array(self.high_corner)
        high_corner2 = array(self.high_corner)
        high_corner1[index] = split
        return Cuboid(low_corner1, high_corner1), Cuboid(low_corner2, high_corner2)

    def diameter(self):
        """Return the diameter of the cuboid.

        Diameter is the Euclidean distance between low_corner and high_corner.

        :return: diameter
        :rtype: float
        """
        return numpy.linalg.norm(self.high_corner - self.low_corner)

    def distance(self, other):
        """Return distance to other Cuboid.

        Distance is the minimal Euclidean distance between points in self and points in other.

        :param other: other cuboid
        :type other: Cuboid

        :return: distance
        :rtype: float
        """
        dimension = len(self.low_corner)
        distance1 = self.low_corner - other.low_corner
        distance2 = self.low_corner - other.high_corner
        distance3 = self.high_corner - other.low_corner
        distance4 = self.high_corner - other.high_corner
        distance_matrix = array((distance1, distance2, distance3, distance4))
        checks = abs(numpy.sum(numpy.sign(distance_matrix), 0)) == 4 * numpy.ones(dimension)
        distance_vector = array(checks, dtype=float)
        min_vector = numpy.amin(abs(distance_matrix), axis=0)
        return numpy.linalg.norm(min_vector * distance_vector)


def minimal_cuboid(cluster):
    """Build minimal cuboid

    Build minimal cuboid around cluster that is parallel to the axis in Cartesian coordinates

    :param cluster: cluster to build cuboid around
    :type cluster: Cluster
    :return: minimal cuboid
    :rtype: Cuboid
    """
    points = cluster.grid.points
    low_corner = numpy.array(points[0], float, ndmin=1)
    high_corner = numpy.array(points[0], float, ndmin=1)
    for p in points:
        p = numpy.array(p, float, ndmin=1)
        lower = p >= low_corner
        if not lower.all():
            for i in xrange(len(low_corner)):
                if not lower[i]:
                    low_corner[i] = p[i]
        higher = p <= high_corner
        if not higher.all():
            for i in xrange(len(high_corner)):
                if not higher[i]:
                    high_corner[i] = p[i]
    return Cuboid(low_corner, high_corner)
