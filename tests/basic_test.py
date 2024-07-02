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


def test_foreign_key_assignment(db):
    db["gen"].add_table("foreign_key_table", {
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
    })
    db["gen"].add_table("test_table", {
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
        "T_name": {
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
        "F_ID": {
            "primarykey": False,
            "autoincrement": False,
            "type": "CHAR(20)",
            "mandatory": True,
            "foreignkey": (
                True,
                {
                    "table": "foreign_key_table",
                    "column": "ID"
                }
            )
        },
    })
    db["op"].add_content("foreign_key_table", {"name": "foreign_key_test_value"})
    tbl_name = "test_table"
    foreign_key_table = "foreign_key_table"
    content = {"T_name": "Foreignkeyrelation", "F_ID": 1}
    foreign_key_info = [foreign_key_table, {"column": "ID", "pos_in_cntnt": 1}]

    # Führen Sie die add_content Methode aus
    db["op"].add_content(tbl_name, content, with_foreign_Key=foreign_key_info)

    fk_table_content = db["op"].search_table(foreign_key_table, {"ID": 1})
    assert fk_table_content is not None, "Foreign Key Eintrag existiert nicht in foreign_key_table."

    # Überprüfen, ob der Eintrag in der test_table existiert und die Foreign Key Zuordnung korrekt ist
    test_table_content = db["op"].search_table(tbl_name, {"F_ID": 1})
    assert test_table_content is not None, "Eintrag existiert nicht in test_table oder Foreign Key Zuordnung ist inkorrekt."
    assert test_table_content[0]["T_name"] == "Foreignkeyrelation", "T_name Wert stimmt nicht überein."


def test_foreign_key_assignment_multiple(db):
    db["gen"].add_table("foreign_key_table", {
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
    })
    db["gen"].add_table("test_table", {
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
        "T_name": {
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
        "F_ID": {
            "primarykey": False,
            "autoincrement": False,
            "type": "CHAR(20)",
            "mandatory": True,
            "foreignkey": (
                True,
                {
                    "table": "foreign_key_table",
                    "column": "ID"
                }
            )
        },
    })
    db["op"].add_content("foreign_key_table", [{"name": "foreign_key_test_value1"},
                                               {"name": "foreign_key_test_value2"}])
    tbl_name = "test_table"
    foreign_key_table = "foreign_key_table"
    content = [{"T_name": "Foreignkeyrelation1", "F_ID": 1},
               {"T_name": "Foreignkeyrelation2", "F_ID": 2}]
    foreign_key_info = [foreign_key_table, {"column": "ID", "pos_in_cntnt": 1}]

    # Führen Sie die add_content Methode aus
    db["op"].add_content(tbl_name, content, with_foreign_Key=foreign_key_info)

    for i in range(1, 3):
        fk_table_content = db["op"].search_table("foreign_key_table", {"ID": i})
        assert fk_table_content is not None, f"Foreign Key Eintrag {i} existiert nicht in foreign_key_table."

    # Überprüfen, ob die Einträge in der test_table existieren und die Foreign Key Zuordnung korrekt ist
    for i in range(1, 3):
        test_table_content = db["op"].search_table(tbl_name, {"F_ID": i})
        assert test_table_content is not None, f"Eintrag {i} existiert nicht in test_table oder Foreign Key Zuordnung ist inkorrekt."
        assert test_table_content[0]["T_name"] == f"Foreignkeyrelation{i}", f"T_name Wert für Eintrag {i} stimmt nicht überein."


if __name__ == "__main__":
    pytest.main([r"./tests/basic_test.py", '-v'])
