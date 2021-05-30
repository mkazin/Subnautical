import unittest
import utilities as geo


class GeometryTestCase(unittest.TestCase):
    def test_geographical_distance(self):
        """ This is a simple pythagoras calculation. """
        self.assertEqual(4, geo.geographical_distance(5, 3))
        self.assertEqual(3, geo.geographical_distance(5, 4))

    def test_pol2cart(self):
        x, y = geo.pol2cart(1, 0)
        self.assertAlmostEqual(0, x)
        self.assertAlmostEqual(-1, y)

        x, y = geo.pol2cart(1, 90)
        self.assertAlmostEqual(-1, x)
        self.assertAlmostEqual(0, y)

        x, y = geo.pol2cart(1, 180)
        self.assertAlmostEqual(0, x)
        self.assertAlmostEqual(1, y)

        x, y = geo.pol2cart(1, 270)
        self.assertAlmostEqual(1, x)
        self.assertAlmostEqual(0, y)



    def test_bearing(self):
        self.assertEqual(0, geo.reverse_bearing(180))
        self.assertEqual(180, geo.reverse_bearing(0))
        self.assertEqual(270, geo.reverse_bearing(90))
        self.assertEqual(90, geo.reverse_bearing(270))

        self.assertEqual(45, geo.reverse_bearing(225))
        self.assertEqual(225, geo.reverse_bearing(45))
        self.assertEqual(135, geo.reverse_bearing(315))
        self.assertEqual(315, geo.reverse_bearing(135))

        self.assertEqual(5, geo.reverse_bearing(185))
        self.assertEqual(185, geo.reverse_bearing(5))


if __name__ == '__main__':
    unittest.main()
