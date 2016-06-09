import unittest
from src.tool import get_time_links
from src.method_one import compute_vertex_nb_in

"""
    The test file is ./data/test2.dyn
    This is our final matrix
    [1, 1,  2, 2]
    [1, 1,  2, 2]
    [3, 2,  1, 4]
    [4, 2, -1, 1]
    Each line represent if a node is accessible (!=1 means accessible) [out]
    Each column is who can access this node [in]
"""

expected_res = [3, 3, 2, 3]


class MyTestCase(unittest.TestCase):
    def test_nb_in(self):

        (links, vertexes) = get_time_links("./../data/test2.dyn", 100)
        nb_vertexes = len(vertexes)

        for i in range(nb_vertexes):
            result = compute_vertex_nb_in(links, nb_vertexes, i)
            self.assertEqual(expected_res[i], result[0])


if __name__ == '__main__':
    unittest.main()
