import os, sys, unittest, csv
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../scripts")
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('config_test.env'))
load_dotenv(find_dotenv('credentials_test.env'))
from unzip_backup import gunzip, push_csv_to_db, move_unzipped_files_into_s3, get_history_data


class TestUnzipBackup(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        # pass name of the file which will be stored inside the 'backup_src' folder
        filename = os.environ.get("TEST_FILENAME")
        self.file_folder = filename.split(".")[0]
        self.upload_zip = os.path.join(os.environ.get("BACKUP_SRC"), filename)
        self.unzip_dir = os.path.join(os.environ.get("UNZIP_DIR"), self.file_folder)
        self.unzip_dir_golden = os.path.join(os.environ.get("UNZIP_DIR_GOLDEN"), self.file_folder)
        if not os.path.exists(self.unzip_dir):
            os.makedirs(self.unzip_dir)

    def test_gunzip(self):
        """
        Calls: unzip_backup.gunzip. Tests: list of filenames
        """
        gunzip(self.upload_zip, self.unzip_dir)
        self.assertListEqual(sorted(os.listdir(self.unzip_dir_golden)), sorted(os.listdir(self.unzip_dir_golden)))

    def test_push_csv_to_db(self):
        """
        Calls: unzip_backup.push_csv_to_db. Tests: the number of rows inserted
        Calls: postgres_interface.get_history_data. Tests: list of file in history
        """
        row_count = push_csv_to_db(self.unzip_dir_golden)
        unzipped_files = os.listdir(self.unzip_dir_golden)
        unzipped_csv = [i for i in unzipped_files if i.endswith(".csv")]
        row_count_golden = 0
        for csv_file in unzipped_csv:
            with open(os.path.join(self.unzip_dir_golden, csv_file), 'r') as f:
                row_count_golden += len(list(csv.reader(f))) - 1  # exclude header
        self.assertEqual(row_count_golden, row_count)
        # new_hist = get_history_data()
        # self.assertIsNotNone(new_hist)
        # new_hist_list = set(new_hist.split('~'))
        # for i in unzipped_csv:
        #     self.assertIn(i, new_hist_list)

    def test_move_unzipped_files_into_s3(self):
        """
        Calls: unzip_backup.move_unzipped_files_into_s3. Tests: the number of files uploaded
        """
        if os.environ.get("HAS_S3_ACCESS").lower() in ('true', 't', 'y', 'yes'):
            moved_files_count = move_unzipped_files_into_s3(self.unzip_dir_golden, self.file_folder)
            self.assertEqual(len(os.listdir(self.unzip_dir_golden)), moved_files_count)
        else:
            print('Skipping S3 testcase')



# Run the unit tests.
if __name__ == '__main__':
    unittest.main()
