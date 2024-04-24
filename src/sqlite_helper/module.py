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
        clmns = self.__col2string(col)
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
        for c in col:
            tmp = []
            tmp.append(c["name"])
            tmp.append(c["type"])
            if c["primarykey"]:
                tmp.append("PRIMARY KEY")
            if c["autoincrement"] and c["type"] == "INTEGER" and c["primarykey"] and not c["mandatory"]:
                tmp.append("AUTOINCREMENT")
            if c["mandatory"]:
                tmp.append("NOT NULL")
        return " ".join(tmp)


    def __check_cols(self, col: dict) -> bool:
        keys_valid = False
        datatypes_valid = False
        columns_valid = False
        
        forbidden = [
            "ABORT", "ACTION", "ADD", "AFTER", "ALL", "ALTER", "ALWAYS", "ANALYZE",
            "AND", "AS", "ASC", "ATTACH", "AUTOINCREMENT", "BEFORE", "BEGIN",
            "BETWEEN", "BY", "CASCADE", "CASE", "CAST", "CHECK", "COLLATE", "COLUMN",
            "COMMIT", "CONFLICT", "CONSTRAINT", "CREATE", "CROSS", "CURRENT", "CURRENT_DATE", 
            "CURRENT_TIME", "CURRENT_TIMESTAMP", "DATABASE", "DEFAULT", "DEFERRABLE",
            "DEFERRED", "DELETE", "DESC", "DETACH", "DISTINCT", "DO", "DROP", "EACH",
            "ELSE", "END", "ESCAPE", "EXCEPT", "EXCLUDE", "EXCLUSIVE", "EXISTS", "EXPLAIN",
            "FAIL", "FILTER", "FIRST", "FOLLOWING", "FOR", "FOREIGN", "FROM", "FULL",
            "GENERATED", "GLOB", "GROUP", "GROUPS", "HAVING", "IF", "IGNORE", "IMMEDIATE",
            "IN", "INDEX", "INDEXED", "INITIALLY", "INNER", "INSERT", "INSTEAD", "INTERSECT",
            "INTO", "IS", "ISNULL", "JOIN", "KEY", "LAST", "LEFT", "LIKE", "LIMIT", "MATCH",
            "MATERIALIZED", "NATURAL", "NO", "NOT", "NOTHING", "NOTNULL", "NULL", "NULLS",
            "OF", "OFFSET", "ON", "OR", "ORDER", "OTHERS", "OUTER", "OVER", "PARTITION",
            "PLAN", "PRAGMA", "PRECEDING", "PRIMARY", "QUERY", "RAISE", "RANGE", "RECURSIVE",
            "REFERENCES", "REGEXP", "REINDEX", "RELEASE", "RENAME", "REPLACE", "RESTRICT", 
            "RETURNING", "RIGHT", "ROLLBACK", "ROW", "ROWS", "SAVEPOINT", "SELECT", "SET",
            "TABLE", "TEMP", "TEMPORARY", "THEN", "TIES", "TO", "TRANSACTION", "TRIGGER",
            "UNBOUNDED", "UNION", "UNIQUE", "UPDATE", "USING", "VACUUM", "VALUES", "VIEW", 
            "VIRTUAL", "WHEN", "WHERE", "WINDOW", "WITH", "WITHOUT"
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
                    raise KeyError("Key don't match need layout or spelling")
                
                if keys_valid and all(type(col[val][cvt]) is e1[cvt] for cvt in col[val]):
                    datatypes_valid = True
                else:
                    raise TypeError("Datatype don't match needed type")

        if not any(x.upper() in forbidden for x in col):
            columns_valid = True
        else:
            raise ValueError("Invalid value in column naming!")
        
        if all([keys_valid, datatypes_valid, columns_valid]):
            return True
        else:
            return False

    def __check_db(self) -> bool:
        exst = False
        return exst

    def close(self):
        self.db.close()


class establish():

    def __init__(self, db_name: str) -> None:
        if not __check_db(db_name):
            raise ConnectionError("Database does not exist. Check name or generate a database first!")
        
if __name__ == "__main__":
    test1 = generator("Test")
    test1.add_table(
        "Test", {
            "Title": {
                "primarykey": False,
                "autoincrement": False,
                "type": "CHAR(25)",
                "mandatory": True,
                "foreignkey": (
                    False, 
                    {
                        "table": "",
                        "column": ""
                    }
                )
            },
            "Name": {"primarykey": False, "type": "CHAR(30)", "mandatory": True, "foreignkey": (False, {"table": "", "column": ""})},
            "Age": {"primarykey": False, "type": "INTEGER", "mandatory": False, "foreignkey": (False, {"table": "", "column": ""})}
        }
    )
