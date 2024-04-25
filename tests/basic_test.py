import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from sqlite_helper import generator as gen


@pytest.fixture()
def db():
    print("setup")
    db = gen("test")
    yield db
    print("teardown")
    db.close()
    os.remove("./database/test.db")
    os.rmdir("./database")


def test_db_gen(db):
    assert os.path.exists("./database/test.db") is True
