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


def test_naming(db):
    assert db.db_name == "test"


def test_addTable(db):
    db.add_table(
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
    db.add_table(
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
    assert db.tables == ["Test", "Test2"]


def test_add_and_remove_table(db):
    table_name = 'users'
    columns = {
        "id": {
            "type": "INTEGER",
            "primarykey": True,
            "autoincrement": True,
            "mandatory": True
        },
        "name": {
            "type": "TEXT",
            "mandatory": True
        },
        "age": {
            "type": "INTEGER",
            "mandatory": False
        }
    }

    # Tabelle hinzufügen
    result = db.add_table(table_name, columns)
    assert result, "Die Tabelle wurde nicht erfolgreich hinzugefügt"
    assert db.__check_tbl(table_name), "Die Tabelle existiert in der Datenbank"
    assert table_name in db.tables, "Die Tabelle ist nicht in der internen Tabelle-Liste"

    # Tabelle entfernen
    result = db.remove_table(table_name)
    assert result, "Die Tabelle wurde nicht erfolgreich entfernt"
    assert not db.__check_tbl(table_name), "Die Tabelle existiert nicht in der Datenbank"
    assert table_name not in db.tables, "Die Tabelle ist noch in der internen Tabelle-Liste"


def test_db_gen(db):
    assert os.path.exists("./database/test.db") is True
