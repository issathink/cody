import unittest
from src.tool import get_time_links
from src.algo import nb_in_out

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

expected_nb_in = [3, 3, 2, 3]
expected_nb_out = [3, 3, 3, 2]


class MyTestCase(unittest.TestCase):
    def test_nb_in_out(self):

        (links, vertexes) = get_time_links("./../data/test2.dyn", 100)
        nb_vertexes = len(vertexes)

        result = nb_in_out(links, nb_vertexes)

        for i in range(nb_vertexes):
            self.assertEqual(expected_nb_in[i], result[i].get(i)[0])
            self.assertEqual(expected_nb_out[i], result[i].get(i)[1])

if __name__ == '__main__':
    unittest.main()
