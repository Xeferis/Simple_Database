import sys
import os
import pytest
from unittest.mock import MagicMock, patch
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from sqlite_helper import generate_db as gen, operate_db as op


def test_GitHub_action():
    assert True

@pytest.fixture
def mock_db():
    class MockDB:
        def cursor(self):
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [{"column1": "value1"}]
            return mock_cursor
    return MockDB()

@pytest.fixture
def obj(mock_db):
    obj = op("test")
    obj.db = mock_db
    yield obj
    os.remove("./database/test.db")
    os.rmdir("./database")

@pytest.fixture()
def db():
    print("setup")
    gen_db = gen("test")
    op_db = op("test")
    yield {"gen": gen_db, "op": op_db}
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
    assert table_name in db["gen"].tables, \
        "Die Tabelle ist nicht in der internen Tabelle-Liste"

    # Tabelle entfernen
    result = db["gen"].remove_table(table_name)
    assert result, "Die Tabelle wurde nicht erfolgreich entfernt"
    assert table_name not in db["gen"].tables, \
        "Die Tabelle ist noch in der internen Tabelle-Liste"


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
        assert str(e_info.value) == \
            "Wrong Datatype given! dict or list of dict needed!"

    with pytest.raises(ConnectionError) as excinfo_cnct:
        db["op"].add_content("test_tbl", {"Title", "test"})

    assert str(excinfo_cnct.value) == \
        "Table does not exist or could not be found!"


def test_table_column_comparision(db):
    db["gen"].add_table(
                "test_clmn1", {
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
    db["gen"].add_table(
                "test_clmn2", {
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
                        "Age": {
                            "primarykey": False,
                            "autoincrement": False,
                            "type": "INT",
                            "mandatory": True,
                            "foreignkey": (
                                False,
                                {
                                    "table": "",
                                    "column": ""
                                }
                            )
                        },
                        "Birth": {
                            "primarykey": False,
                            "autoincrement": False,
                            "type": "DATE",
                            "mandatory": True,
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
    assert db["op"]._compare_cols("test_clmn1", ["Title"])
    assert db["op"]._compare_cols("test_clmn1", ["Title", "Name",
                                                 "Age", "Birth"])


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

    result = db["op"].get_content("test_content_tbl")
    expected_titles = ["test", "test1", "test2", "test3", "test4"]
    print(result)
    assert len(result) == len(expected_titles), "Number of entries \
                                                    is not correct!"
    for i, entry in enumerate(result):
        assert entry["Title"] == expected_titles[i], "Entry is not correct!"


def test_get_content_existing_table(obj):
    obj._check_tbl = MagicMock(return_value=True)
    result = obj.get_content("existing_table")
    assert result == [{"column1": "value1"}]


def test_get_content_nonexistent_table(obj):
    obj._check_tbl = MagicMock(return_value=False)
    result = obj.get_content("nonexistent_table")
    assert result == [], "The table does not exist, \
                            so the result should be an empty list."


def test_search_table_existing_table(obj):
    obj._check_tbl = MagicMock(return_value=True)
    search_query = {"column1": "value1"}
    result = obj.search_table("existing_table", search_query)
    assert result == [{"column1": "value1"}], "The search \
                            query should return the correct result."


def test_search_table_nonexistent_table(obj):
    obj._check_tbl = MagicMock(return_value=False)
    search_query = {"column1": "value1"}
    result = obj.search_table("nonexistent_table", search_query)
    assert result == [], "The table does not exist, so the \
                            result should be an empty list."


def test_del_content(db):
    cur = db["op"].db.cursor()
    cur.execute('CREATE TABLE test_tbl (id INTEGER PRIMARY KEY, name TEXT)')

    cur.executemany('INSERT INTO test_tbl (name) VALUES (?)',
                    [('Alice',), ('Bob',), ('Charlie',)])
    db["op"].db.commit()

    db["op"].del_content('test_tbl', {'name': 'Bob'})
    cur.execute('SELECT * FROM test_tbl WHERE name = ?', ('Bob',))
    assert cur.fetchone() is None, "The entry was not deleted."

    cur.execute('SELECT COUNT(*) FROM test_tbl')
    count = cur.fetchone()[0]
    assert count == 2, "The number of entries, after deletion, is not correct."

if __name__ == "__main__":
    pytest.main([r"./tests/basic_test.py", '-v'])
