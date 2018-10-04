import unittest

from dir_executor import generate_input_output_pairs, generate_output_path, \
        generate_output_file_name, generate_output_dir


class TestDirExecutor(unittest.TestCase):

    def test_generate_output_file_name(self):
        test_map = {
            ('file.ext', ''): 'file.out',
            ('file.ext', 'out'): 'file.out',
            ('/dir/file.ext', 'out'): 'file.out',
            ('/dir/subdir/file.ext', 'out2'): 'file.out2'
        }

        for (input_file, output_extension), output_file in test_map.items():
            assert generate_output_file_name(input_file, output_extension) == output_file

    def test_generate_output_dir(self):
        test_map = {
            ('file.ext', ''): '',
            ('file.ext', 'out'): 'out',
            ('/dir/file.ext', ''): '/dir',
            ('/dir/subdir/file.ext', 'out2'): 'out2'
        }

        for (input_file, output_dir), expected in test_map.items():
            assert generate_output_dir(input_file, output_dir) == expected

    def test_generate_output_path(self):
        test_map = {
            ('file.ext', '', ''): 'file.out',
            ('file.ext', '', 'out'): 'file.out',
            ('/dir/file.ext', '', 'out'): '/dir/file.out',
            ('/dir/subdir/file.ext', '/dir2', 'out2'): '/dir2/file.out2'
        }

        for (in_file, out_dir, out_extension), output_path in test_map.items():
            assert output_path == generate_output_path(in_file, out_dir, out_extension)

    def test_generate_input_output_pairs(self):
        test_map = {
            (('file.ext', '/dir/file.ext', '/dir/subdir/file1.ext'), '', ''):
                [
                    ('file.ext', 'file.out'),
                    ('/dir/file.ext', '/dir/file.out'),
                    ('/dir/subdir/file1.ext', '/dir/subdir/file1.out')
                ],
            (('file.ext', '/dir/file.ext', '/dir/subdir/file1.ext'), '/out_dir', 'xxx'):
                [
                    ('file.ext', '/out_dir/file.xxx'),
                    ('/dir/file.ext', '/out_dir/file.xxx'),
                    ('/dir/subdir/file1.ext', '/out_dir/file1.xxx')
                ],
            ((), 'out_dir', 'xxx'): []

        }

        for (in_files, out_dir, out_extension), expected_pairs in test_map.items():
            input_output_pairs = generate_input_output_pairs(
                list(in_files), out_dir, out_extension)
            self.assertListEquals(input_output_pairs, expected_pairs)

    def assertListEquals(self, L1, L2):
        assert len(L1) == len(L2)
        assert sorted(L1) == sorted(L2)
