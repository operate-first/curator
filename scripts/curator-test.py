import os
import unittest
from unzip_backup import backup_src, unzip_dir, get_history_file, gunzip, push_csv_to_db, move_unzipped_files_into_s3, update_history_data, get_history_data


class TestUnzipBackup(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        # pass a name of the file which will be stored inside the 'backup_src' folder
        filename = "xyz.tar.gz"
        self.backup_full_path = os.path.join(backup_src, filename)
        self.file_folder = filename.split(".")[0]
        self.unzip_folder_dir = os.path.join(unzip_dir, self.file_folder)
        if not os.path.exists(self.unzip_folder_dir):
            os.makedirs(self.unzip_folder_dir)

    def test_get_history_file(self):
        get_history_file()
        is_exists = os.path.exists(os.path.join(unzip_dir, 'history.txt'))
        # check whether the history file is downloaded and present in the directory. this will confirm us whether able to connect with boto s3
        self.assertEqual(True, is_exists)

    def test_gunzip(self):
        gunzip(self.backup_full_path, self.unzip_folder_dir, False)
        unzipped_files = os.listdir(self.unzip_folder_dir)
        # the files should be present inside unzipped folder. So, the # of files should be > 0
        self.assertGreater(len(unzipped_files), 0)

    def test_push_csv_to_db(self):
        row_count = push_csv_to_db(self.unzip_folder_dir)
        # the records should be inserted and the count should be > 0
        self.assertGreater(row_count, 0)

    def test_get_history_data(self):
        history_data = get_history_data(self.unzip_folder_dir)
        # the records should be inserted and the count should be > 0
        self.assertNotEqual(history_data, "")

    def test_update_history_data(self):
        query = "UPDATE HISTORY set filenames={}".format("test data")
        is_updated = update_history_data()
        # the records should be inserted and the count should be > 0
        self.assertTrue(is_updated)

    def test_move_unzipped_files_into_s3(self):
        moved_files_count = move_unzipped_files_into_s3(
            self.unzip_folder_dir, self.file_folder)
        self.assertEqual(moved_files_count, len(
            os.listdir(self.unzip_folder_dir)))  # check whether all the files are moved into s3 bucket. This will confirm us whetehr we can able to push a file into s3 bucket or not


# Run the unit tests.
if __name__ == '__main__':
    unittest.main()