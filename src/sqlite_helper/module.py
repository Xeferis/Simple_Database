import os
import sqlite3 as sql3
from typing import Union


class establish_db():

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.tables = []
        if not os.path.exists("./database"):
            os.makedirs("./database")
        if self._check_db():
            print(f"Connecting to {self.db_name}.db")
        else:
            print(f"Generating {self.db_name}.db")
        self.db = sql3.connect(f"./database/{self.db_name}.db")

    # PLACEHOLDER!
    # ---
    def _check_db(self) -> bool:
        exst = False
        return exst
    # ---

    def _check_tbl(self, tbl_name) -> bool:
        cur = self.db.cursor()
        sql_stmnt = f"""
                SELECT name FROM sqlite_master WHERE type='table' AND name='{tbl_name}';
                """
        res = cur.execute(sql_stmnt)
        if res.fetchone() is None:
            print("Tabelle ist nicht vorhanden")
            cur.close()
            return False
        else:
            cur.close()
            print("Tabelle ist vorhanden")
            return True

    def close(self):
        self.db.close()


class generate_db(establish_db):

    def __init__(self, db_name: str) -> None:
        super().__init__(db_name)
        

    def add_table(self, tbl_name: str, col: dict) -> bool:
        """
        Dictionary Aufbau

        "col_name": {
                "primarykey": bool,
                "autoincrement": bool,
                "type": DATATYPEasSTRING,
                "mandatory": bool,
                "foreignkey": (
                    bool,
                    {
                        "table": REFERENCE_TABLENAMEasSTRING,
                        "column": REFERENCE_COLUMNNAMEasSTRING
                    }
                )
            },
        """
        if not self.__check_cols(col):
            raise SyntaxError("Invalid value in columns!")
        cur = self.db.cursor()
        clmns = ", ".join(self.__col2string(col))
        sql_stmnt = f"""
                    CREATE TABLE
                    {tbl_name}
                    (
                        {clmns}
                    );
                    """
        res = cur.execute(sql_stmnt)
        if res.fetchone is None:
            return False
        else:
            self.tables.append(tbl_name)
            return True

    def remove_table(self, tbl_name) -> bool:
        cur = self.db.cursor()
        sql_stmnt = f"""
                    DROP TABLE {tbl_name};
                    """
        if self._check_tbl(tbl_name):
            cur.execute(sql_stmnt)
            if not self._check_tbl(tbl_name):
                self.tables.remove(tbl_name)
                return True
        return False

    def __col2string(self, col: dict) -> list:
        out = []
        frngky = []
        for c in col:
            tmp = []
            tmp.append(c)
            tmp.append(col[c]["type"])
            if col[c]["primarykey"] and col[c]["foreignkey"][0]:
                raise ValueError("You can only use one primary or foreign!")

            if col[c]["primarykey"]:
                tmp.append("PRIMARY KEY")

            if (col[c]["autoincrement"] and col[c]["type"] == "INTEGER"
                    and col[c]["primarykey"] and not col[c]["mandatory"]):
                tmp.append("AUTOINCREMENT")

            if col[c]["mandatory"]:
                tmp.append("NOT NULL")

            if (col[c]["foreignkey"][0] and not col[c]["primarykey"]
                    and not col[c]["autoincrement"]):
                frngky.append(
                    f"""FOREIGN KEY({c}) REFERENCES
                    {col[c]['foreignkey'][1]['table']}
                    ({col[c]['foreignkey'][1]['column']})
                    """)

            out.append(" ".join(tmp))
        return out + frngky

    def __check_cols(self, col: dict) -> bool:
        keys_valid = False
        datatypes_valid = False
        columns_valid = False

        sql_datatypes = [
            "INT", "INTEGER", "TINYINT", "SMALLINT", "MEDIUMINT", "BIGINT",
            "UNSIGNED BIG INT", "INT2", "INT8", "CHARACTER", "VARCHAR",
            "VARYING CHARACTER", "NCHAR", "NATIVE CHARACTER",
            "NVARCHAR", "TEXT", "CLOB", "CHAR", "BLOB", "REAL", "DOUBLE",
            "DOUBLE PRECISION", "FLOAT", "NUMERIC", "DECIMAL", "BOOLEAN",
            "DATE", "DATETIME"
        ]

        forbidden = [
            "ABORT", "ACTION", "ADD", "AFTER", "ALL", "ALTER", "ALWAYS",
            "ANALYZE", "AND", "AS", "ASC", "ATTACH", "AUTOINCREMENT",
            "BEFORE", "BEGIN", "BETWEEN", "BY", "CASCADE", "CASE", "CAST",
            "CHECK", "COLLATE", "COLUMN", "COMMIT", "CONFLICT", "CONSTRAINT",
            "CREATE", "CROSS", "CURRENT", "CURRENT_DATE", "CURRENT_TIME",
            "CURRENT_TIMESTAMP", "DATABASE", "DEFAULT", "DEFERRABLE",
            "DEFERRED", "DELETE", "DESC", "DETACH", "DISTINCT", "DO", "DROP",
            "EACH", "ELSE", "END", "ESCAPE", "EXCEPT", "EXCLUDE", "EXCLUSIVE",
            "EXISTS", "EXPLAIN", "FAIL", "FILTER", "FIRST", "FOLLOWING", "FOR",
            "FOREIGN", "FROM", "FULL", "GENERATED", "GLOB", "GROUP", "GROUPS",
            "HAVING", "IF", "IGNORE", "IMMEDIATE", "IN", "INDEX", "INDEXED",
            "INITIALLY", "INNER", "INSERT", "INSTEAD", "INTERSECT", "INTO",
            "IS", "ISNULL", "JOIN", "KEY", "LAST", "LEFT", "LIKE", "LIMIT",
            "MATCH", "MATERIALIZED", "NATURAL", "NO", "NOT", "NOTHING",
            "NOTNULL", "NULL", "NULLS", "OF", "OFFSET", "ON", "OR", "ORDER",
            "OTHERS", "OUTER", "OVER", "PARTITION", "PLAN", "PRAGMA",
            "PRECEDING", "PRIMARY", "QUERY", "RAISE", "RANGE", "RECURSIVE",
            "REFERENCES", "REGEXP", "REINDEX", "RELEASE", "RENAME", "REPLACE",
            "RESTRICT", "RETURNING", "RIGHT", "ROLLBACK", "ROW", "ROWS",
            "SAVEPOINT", "SELECT", "SET", "TABLE", "TEMP", "TEMPORARY", "THEN",
            "TIES", "TO", "TRANSACTION", "TRIGGER", "UNBOUNDED", "UNION",
            "UNIQUE", "UPDATE", "USING", "VACUUM", "VALUES", "VIEW", "VIRTUAL",
            "WHEN", "WHERE", "WINDOW", "WITH", "WITHOUT"
        ]

        dict_check = {"col_name": {
                "primarykey": bool,
                "autoincrement": bool,
                "type": str,
                "mandatory": bool,
                "foreignkey": (
                    bool,
                    {
                        "table": str,
                        "column": str
                    }
                )
            },
        }

        for val in col:
            for e1 in dict_check.values():

                if all(e1k in col[val].keys() for e1k in e1.keys()):
                    keys_valid = True
                else:
                    raise KeyError("Key don't match needed layout or spelling")

                if keys_valid:

                    for cvt in col[val]:

                        if cvt == "type":

                            if "(" in col[val][cvt]:
                                clnd = col[val][cvt].split("(")[0]
                            else:
                                clnd = col[val][cvt]
                            if clnd in sql_datatypes:
                                datatypes_valid = True
                            else:
                                raise TypeError(f"""
                                        SQL Datatype not correct - see {val},
                                        {clnd} not matching validationvalues!
                                        """)

                        if cvt == "foreignkey":

                            if type(col[val][cvt][0]) is e1[cvt][0]:
                                datatypes_valid = True
                            else:
                                raise TypeError(f"""
                        Datatype don't match needed type - see:
                        {col[val][cvt][0]}(type: {type(col[val][cvt][0])})
                        not matching {e1[cvt][0]}
                        """)

                            for cvt2 in col[val][cvt][1]:
                                if (type(col[val][cvt][1][cvt2])
                                        is e1[cvt][1][cvt2]):

                                    datatypes_valid = True
                                else:
                                    raise TypeError(f"""
                        Datatype doesn't match needed type - see:
                        {col[val][cvt][1][cvt2]}
                        (type: {type(col[val][cvt][1][cvt2])})
                        not matching {e1[cvt][1][cvt2]}
                        """)

                        elif type(col[val][cvt]) is e1[cvt]:
                            datatypes_valid = True
                        else:
                            raise TypeError(f"""
                                        Datatype don't match needed type - see
                                         {col[val][cvt]}(type:
                                         {type(col[val][cvt])})
                                         not matching {e1[cvt]}
                                        """)

        if not any(x.upper() in forbidden for x in col):
            columns_valid = True
        else:
            raise ValueError("Invalid value in column naming!")

        if all([keys_valid, datatypes_valid, columns_valid]):
            return True
        else:
            return False

class operate_db(establish_db):

    def __init__(self, db_name: str) -> None:
        super().__init__(db_name)

    def add_content(self, tbl_name: str, content: dict | list[dict]) -> bool | TypeError:
        errors = [
            TypeError("Wrong Datatype given! dict or list of dict needed!"),
            ConnectionError("Table does not exist or could not be found!")
        ]
        if self._check_tbl(tbl_name):
            if type(content) == dict:
                pass
            elif type(content) == list:
                for elem in content:
                    if type(elem) == dict:
                        pass
                    else:
                        raise errors[0]
            else:
                raise errors[0]
        else:
            raise errors[1]
        return True
