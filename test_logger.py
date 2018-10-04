import unittest

from logger import Logger


class TestLogger(unittest.TestCase):
    def test_structure_content(self):
        logger = Logger('')
        empty_lines = []
        empty_structure = []
        assert (logger.structure_lines(empty_lines) == empty_structure)

        lines = [
            "ERROR;tag1;message1\n",
            "INFO;tag2;message1\n",
            "INFO;tag2;message2\n",
            "ERROR;tag2;message3\n"
        ]
        expected_structured_content = [
            ['ERROR', 'tag1', 'message1'],
            ['INFO', 'tag2', 'message1'],
            ['INFO', 'tag2', 'message2'],
            ['ERROR', 'tag2', 'message3']
        ]
        structured_content = logger.structure_lines(lines)
        assert (len(structured_content) == len(expected_structured_content))
        for i in range(len(structured_content)):
            assert (
                structured_content[i] == expected_structured_content[i]
            )

    def test_filter_info(self):
        logger = Logger('')
        empty_lines = []
        empty_infos = []
        assert (logger.filter_infos(empty_lines) == empty_infos)

        structured_lines = [
            ['ERROR', 'tag1', 'message1'],
            ['INFO', 'tag2', 'message1'],
            ['INFO', 'tag2', 'message2'],
            ['ERROR', 'tag2', 'message3']
        ]
        expected_infos = [
            ['INFO', 'tag2', 'message1'],
            ['INFO', 'tag2', 'message2']
        ]
        filtered_infos = logger.filter_infos(structured_lines)
        assert (len(filtered_infos) == len(expected_infos))
        for i in range(len(filtered_infos)):
            assert (
                filtered_infos[i] == expected_infos[i]
            )

    def test_filter_tag(self):
        logger = Logger('')
        empty_lines = []
        empty_tags = []
        assert (logger.filter_infos(empty_lines) == empty_tags)

        structured_lines = [
            ['ERROR', 'tag1', 'message1'],
            ['INFO', 'tag2', 'message1'],
            ['INFO', 'tag2', 'message2'],
            ['ERROR', 'tag2', 'message3']
        ]
        expected_tags = [
            ['INFO', 'tag2', 'message1'],
            ['INFO', 'tag2', 'message2'],
            ['ERROR', 'tag2', 'message3']
        ]
        filtered_tags = logger.filter_tag(structured_lines, 'tag2')
        assert (len(filtered_tags) == len(expected_tags))
        for i in range(len(filtered_tags)):
            assert (
                filtered_tags[i] == expected_tags[i]
            )

    def test_filter_info_by_tag(self):
        logger = Logger('')
        empty_lines = []
        empty_info_by_tag = []
        assert (logger.filter_infos(empty_lines) == empty_info_by_tag)

        structured_lines = [
            ['ERROR', 'tag1', 'message1'],
            ['INFO', 'tag2', 'message1'],
            ['INFO', 'tag2', 'message2'],
            ['ERROR', 'tag2', 'message3']
        ]
        expected_info_by_tag = [
            ['INFO', 'tag2', 'message1'],
            ['INFO', 'tag2', 'message2']
        ]
        filtered_info_by_tag = logger.info_by_tag(structured_lines, 'tag2')
        assert (len(filtered_info_by_tag) == len(expected_info_by_tag))
        for i in range(len(filtered_info_by_tag)):
            assert (
                filtered_info_by_tag[i] == expected_info_by_tag[i]
            )
