import unittest

from files_executor import chunk_list, parse_input_output_pair

class TestFilesExecutor(unittest.TestCase):

    def test_parse_input_output_pairs_empty_input(self):
        assert ("i1", "o1") == parse_input_output_pair("i1:o1")

    def test_chunk_list_with_single_chunk(self):
        test_map = dict()
        first_chunk = list(range(250))
        test_map[(range(250), 1)] = [first_chunk]

        for (some_list, num_of_chunks), expected in test_map.items():
            chunks = chunk_list(some_list, num_of_chunks)
            assert len(expected) == len(chunks)
            for i in range(len(chunks)):
                self.assertListEquals(expected[i], chunks[i])

    def test_chunk_list_with_multiple_chunk(self):
        test_map = dict()
        first_chunk = list(range(250))
        first_chunk.append(1000)
        second_chunk = list(range(250, 500))
        second_chunk.append(1001)
        third_chunk = list(range(500, 750))
        forth_chunk = list(range(750, 1000))
        test_map[(range(1002), 4)] = [first_chunk, second_chunk, third_chunk, forth_chunk]

        for (some_list, num_of_chunks), expected in test_map.items():
            chunks = chunk_list(some_list, num_of_chunks)
            assert len(chunks) == len(expected)
            for i in range(len(chunks)):
                self.assertListEquals(expected[i], chunks[i])

    def assertListEquals(self, L1, L2):
        assert len(L1) == len(L2)
        assert sorted(L1) == sorted(L2)
