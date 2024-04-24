import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from sqlite_helper import generator as gen


def db_gen_test():
    test1 = gen("test")
    test1.close()
    assert os.path.exists("./database/test.db") == True
    os.remove("./database/test.db")
    os.rmdir("./database")
