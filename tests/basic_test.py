import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from sqlite_helper import generate_db as gen, operate_db as op

def test_GitHub_action():
    assert True

@pytest.fixture()
def db():
    print("setup")
    gen_db = gen("test")
    op_db = op("test")
    yield {"gen": gen_db,"op": op_db}
    print("teardown")
    gen_db.close()
    op_db.close()
    os.remove("./database/test.db")
    os.rmdir("./database")


def test_naming(db):
    assert db["gen"].db_name == "test"


def test_addTable(db):
    db["gen"].add_table(
        "Test", {
            "ID": {
                "primarykey": True,
                "autoincrement": True,
                "type": "INTEGER",
                "mandatory": False,
                "foreignkey": (
                    False,
                    {
                        "table": "",
                        "column": ""
                    }
                )
            },
            "Title": {
                "primarykey": False,
                "autoincrement": False,
                "type": "CHAR(20)",
                "mandatory": True,
                "foreignkey": (
                    False,
                    {
                        "table": "",
                        "column": ""
                    }
                )
            },
            "Name": {
                "primarykey": False,
                "autoincrement": False,
                "type": "TEXT",
                "mandatory": True,
                "foreignkey": (
                    False,
                    {
                        "table": "",
                        "column": ""
                    }
                )
            },
            "Age": {
                "primarykey": False,
                "autoincrement": False,
                "type": "INTEGER",
                "mandatory": False,
                "foreignkey": (
                    False,
                    {
                        "table": "",
                        "column": ""
                    }
                )
            }
        }
    )
    db["gen"].add_table(
        "Test2", {
            "F_ID": {
                "primarykey": False,
                "autoincrement": False,
                "type": "INTEGER",
                "mandatory": False,
                "foreignkey": (
                    True,
                    {
                        "table": "Test1",
                        "column": "ID"
                    }
                )
            },
            "Title": {
                "primarykey": False,
                "autoincrement": False,
                "type": "CHAR(20)",
                "mandatory": True,
                "foreignkey": (
                    False,
                    {
                        "table": "",
                        "column": ""
                    }
                )
            },
        }
    )
    assert db["gen"].tables == ["Test", "Test2"]


def test_add_and_remove_table(db):
    table_name = 'users'
    columns = {
            "F_ID": {
                "primarykey": False,
                "autoincrement": False,
                "type": "INTEGER",
                "mandatory": False,
                "foreignkey": (
                    True,
                    {
                        "table": "Test1",
                        "column": "ID"
                    }
                )
            },
            "Title": {
                "primarykey": False,
                "autoincrement": False,
                "type": "CHAR(20)",
                "mandatory": True,
                "foreignkey": (
                    False,
                    {
                        "table": "",
                        "column": ""
                    }
                )
            },
        }

    # Tabelle hinzufügen
    result = db["gen"].add_table(table_name, columns)
    assert result, "Die Tabelle wurde nicht erfolgreich hinzugefügt"
    assert table_name in db["gen"].tables, "Die Tabelle ist nicht in der internen Tabelle-Liste"

    # Tabelle entfernen
    result = db["gen"].remove_table(table_name)
    assert result, "Die Tabelle wurde nicht erfolgreich entfernt"
    assert table_name not in db["gen"].tables, "Die Tabelle ist noch in der internen Tabelle-Liste"


def test_db_gen(db):
    assert os.path.exists("./database/test.db") is True

def test_fill_content_errors(db):
    excinfo = []
    test_vals = [
        "placeholder content",
        1,
        [2, 3],
        ["test", 1],
        [{"name": "test"}, 1]
        ]
    db["gen"].add_table(
                "error_test_tbl", {
                        "ID": {
                            "primarykey": True,
                            "autoincrement": True,
                            "type": "INTEGER",
                            "mandatory": False,
                            "foreignkey": (
                                False,
                                {
                                    "table": "",
                                    "column": ""
                                }
                            )
                        },
                        "name": {
                            "primarykey": False,
                            "autoincrement": False,
                            "type": "CHAR(20)",
                            "mandatory": True,
                            "foreignkey": (
                                False,
                                {
                                    "table": "",
                                    "column": ""
                                }
                            )
                        },
                    }
            )
    # Type Errors
    for i, val in enumerate(test_vals):
        excinfo.append("")
        with pytest.raises(TypeError) as excinfo[i]:
            db["op"].add_content("error_test_tbl", val)
    for e_info in excinfo:
        assert str(e_info.value) == "Wrong Datatype given! dict or list of dict needed!"
    
    with pytest.raises(ConnectionError) as excinfo_cnct:  
            db["op"].add_content("test_tbl", {"Title", "test"})
    assert str(excinfo_cnct.value) == "Table does not exist or could not be found!"

@pytest.mark.skip(reason="Current Placeholder. 'get_content' function needed first!")
def test_table_content(db):
    db["gen"].add_table(
                "test_content_tbl", {
                        "ID": {
                            "primarykey": True,
                            "autoincrement": True,
                            "type": "INTEGER",
                            "mandatory": False,
                            "foreignkey": (
                                False,
                                {
                                    "table": "",
                                    "column": ""
                                }
                            )
                        },
                        "Title": {
                            "primarykey": False,
                            "autoincrement": False,
                            "type": "CHAR(20)",
                            "mandatory": True,
                            "foreignkey": (
                                False,
                                {
                                    "table": "",
                                    "column": ""
                                }
                            )
                        },
                    }
            )
    db["op"].add_content("test_content_tbl", {"Title": "test"})
    db["op"].add_content("test_content_tbl", [
                                    {"Title": "test1"},
                                    {"Title": "test2"},
                                    {"Title": "test3"},
                                    {"Title": "test4"}
                                    ])
    assert False

if __name__ == "__main__":
    pytest.main([r"./tests/basic_test.py", '-v'])
