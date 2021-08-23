import os
import unittest
import sys
from unzip_backup import backup_src, unzip_dir, gunzip, push_csv_to_db, move_unzipped_files_into_s3, get_history_data
import csv

class TestUnzipBackup(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        # pass name of the file which will be stored inside the 'backup_src' folder
        filename = "20210616T125440-cost-mgmt.tar.gz"
        self.backup_full_path = os.path.join(backup_src, filename)
        self.file_folder = filename.split(".")[0]
        self.unzip_folder_dir = os.path.join(unzip_dir, self.file_folder)
        if not os.path.exists(self.unzip_folder_dir):
            os.makedirs(self.unzip_folder_dir)

    def test_gunzip(self):
        gunzip(self.backup_full_path, self.unzip_folder_dir, push_to_db=False)
        unzipped_files = os.listdir(self.unzip_folder_dir)
        # the files should be present inside unzipped folder. So, the # of files should be > 0
        self.assertGreater(len(unzipped_files), 0)

    def test_push_csv_to_db(self):
        row_count = push_csv_to_db(self.unzip_folder_dir)
        unzipped_files = os.listdir(self.unzip_folder_dir)
        # the records should be inserted and the count should be > 0
        unzipped_csv = [i for i in unzipped_files if i.endswith(".csv")]
        total_rows = 0
        for csv_file in unzipped_csv:
            with open(os.path.join(self.unzip_folder_dir, csv_file), 'r') as f:
                total_rows += len(list(csv.reader(f))) - 1  # exclude header
        self.assertEqual(total_rows, row_count)

    # def test_get_history_file(self):
    #     unzipped_file_hist = get_history_data().split("\n")
    #     # check whether the history file is downloaded and present in the directory. this will confirm us whether able to connect with boto s3
    #     for bsubdir, bdirs, bfiles in os.walk(backup_src):
    #         for bf in bfiles:
    #             self.assertEqual(True, bf in unzipped_file_hist)

    # def test_move_unzipped_files_into_s3(self):
    #     moved_files_count = move_unzipped_files_into_s3(
    #         self.unzip_folder_dir, self.file_folder)
    #     self.assertEqual(moved_files_count, len(
    #         os.listdir(self.unzip_folder_dir)))  # check whether all the files are moved into s3 bucket. This will confirm us whetehr we can able to push a file into s3 bucket or not


# Run the unit tests.
if __name__ == '__main__':
    unittest.main()
    
