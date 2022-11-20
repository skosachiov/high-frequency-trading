import unittest

import hft_producer

class TestHFTGenerator(unittest.TestCase):

    def test_single_set_generation(self):
        d = hft_producer.hft_dataset(100)
        self.assertTrue(1 <= d['prices']['values'][9] and d['prices']['values'][9] <= 100)

    def test_series_of_datasets(self):
        r = hft_producer.hft_datastream(100, 0.001, 10)
        self.assertEqual(r, 100-1)

if __name__ == '__main__':
    unittest.main()