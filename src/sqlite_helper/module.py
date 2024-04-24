import os
import sqlite3 as sql3


class generator():

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        if not os.path.exists("./database"):
            os.makedirs("./database")
        if self.__check_db():
            print(f"Connecting to {self.db_name}.db")
        else:
            print(f"Generating {self.db_name}.db")
        self.db = sql3.connect(f"./database/{self.db_name}.db")

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
            return True

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
                        {col[val][cvt][1][cvt2]}(type: {type(col[val][cvt][1][cvt2])})
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

    # PLACEHOLDER!
    # ---
    def __check_db(self) -> bool:
        exst = False
        return exst
    # ---

    def close(self):
        self.db.close()


class establish():

    def __init__(self, db_name: str) -> None:
        pass
        """
        if not __check_db(db_name):
            raise ConnectionError("Database does not exist.
            Check name or generate a database first!")
        """


if __name__ == "__main__":
    test1 = generator("Test")
    test1.add_table(
        "Test", {
            "ID": {
                "primarykey": "True",
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
    test1.add_table(
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
