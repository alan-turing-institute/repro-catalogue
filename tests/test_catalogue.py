import unittest
import catalogue.catalogue as ct
import os
import filecmp

class Test_Hashing(unittest.TestCase):
    @classmethod
    def SetUp(self):
        os.mkdir("HashTesting")
        self.fixtures = "fixtures"
        self.engagefixtures = os.path.join(self.fixtures, "engagefixtures")
        self.comparefixtures = os.path.join(self.fixtures, "comparefixtures")
        self.fixture1 = os.path.join(self.fixtures, "fixture1.json")
        self.fixture2 = os.path.join(self.fixtures, "fixture2.json")
        self.hash1 = ""
        self.json1 = os.path.join("HashTesting", "test1")
        self.json2 = os.path.join("HashTesting", "test2")
        ct.store_hash({"foo": 1234}, "HashTesting", "test1")
        ct.store_hash({"foo": 1234}, "HashTesting", "test2")
        
    @classmethod
    def TearDown(self):
        os.remove(self.json1)
        os.remove(self.json2)
        os.rmdir("HashTesting")
        
    def test_load_hash_consistent(self):
        assert ct.load_hash(self.fixture1) == ct.load_hash(self.fixture2)

    def test_store_hash_consistent(self):
        assert filecmp.cmp(self.json1, self.json2)

    def test_store_hash_fixture(self):
        assert filecmp.cmp(self.json1, self.fixture1)

    def test_load_hash_fixture(self):
        assert ct.load_hash(self.fixture1) == {"foo": 1234}

    def test_store_and_load(self):
        assert ct.load_hash(self.json1) == {"foo": 1234}

    def test_hash_file(self):
        assert ct.hash_file(self.fixture1).digest() == self.hash1

    def test_hash_file_consistent(self):
        assert ct.hash_file(self.fixture1).digest() == ct.hash_file(self.fixture2).digest()

    def test_hash_dir_by_file(self):
        d = ct.hash_dir_by_file(self.fixtures, kwargs={"subdirs": [self.engagefixtures,self.comparefixtures]})
        d["fixture1.json"] = self.hash1
        d["fixture2.json"] = self.hash2

    def test_modified_walk_fixtures(self):
        d = ct.modified_walk("fixtures", kwargs={"subdirs": [self.engagefixtures,self.comparefixtures]})
        assert d = ["fixture1.json", "fixture2.json"]
        
        

    
