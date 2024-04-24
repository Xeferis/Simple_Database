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
    
    def add_table(self, tbl_name: str, col: list) -> bool:
        if not self.__check_cols(col):
            raise ValueError("Invalid Columnname!")
        cur = self.db.cursor()
        clmns = ", ".join(col)
        sql_stmnt = f"""
                    CREATE TABLE
                    {tbl_name}
                    (
                        {clmns}
                    )
                    """
        res = cur.execute(sql_stmnt)
        if res.fetchone is None:
            return False
        else:
            return True
    
    def __check_cols(self, col: list) -> bool:
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

        if any(x.upper() in forbidden for x in col):
            return False
        else:
            return True

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
    test1.add_table("Test", ["Title","Name","Age"])
