import unittest

import web.filters


class TestPrettyBoolean(unittest.TestCase):
    def test(self):
        assert "Oui" == web.filters.pretty_boolean(True)
        assert "Oui" == web.filters.pretty_boolean([1, 2])

        assert "Non" == web.filters.pretty_boolean(False)
        assert "Non" == web.filters.pretty_boolean([])


class TestShuffle(unittest.TestCase):
    def test(self):
        ORIGIN = [1, 2, 3, 4, 5]
        shuffleds = []

        for i in range(4):
            _shuffled = web.filters.shuffle(ORIGIN)
            assert set(ORIGIN) == set(_shuffled)
            shuffleds.append(_shuffled)
        assert not (shuffleds[0] == shuffleds[1] == shuffleds[2] == shuffleds[3])

