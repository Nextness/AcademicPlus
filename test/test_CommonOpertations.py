import AcademicPlus.CommonOperations as cmnops
import unittest
import shutil
import os

CURPATH = os.getcwd()
TMPPATH = f"{CURPATH}\\tmp"


class TestSaveFileUnsafe(unittest.TestCase):

    def setUp(self) -> None:
        os.mkdir("tmp")
        self.save_location = f"{TMPPATH}"
        self.file = f"{self.save_location}\\file.json"

    def tearDown(self) -> None:
        shutil.rmtree(TMPPATH)

    def test_file_is_saved(self):
        file_content = {"Name": "Testing, the Testerson"}
        result = cmnops._save_file_unsafe(file_content, self.file)
        self.assertEqual(result, 0)

    def test_file_is_not_saved(self):
        result = cmnops._save_file_unsafe(1, self.file)
        self.assertEqual(result, 1)
