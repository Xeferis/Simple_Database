import os
import sqlite3 as sql3


class establish_db():
    """Base class - Should not be uses standalone!
    """

    def __init__(self, db_name: str) -> None:
        """Establishing a connection to a database or create a new one

        Args:
            db_name (str): Just type the name. Bsp: "test" (The folder and the suffix will be added automatically)
        """
        self.db_name = db_name
        self.tables = []
        if not os.path.exists("./database"):
            os.makedirs("./database")
        if self._check_db():
            print(f"Connecting to {self.db_name}.db")
        else:
            print(f"Generating {self.db_name}.db")
        self.db = sql3.connect(f"./database/{self.db_name}.db")

    def _check_db(self) -> bool:
        """Internal Use only
        
        Checks if a database exists

        Returns:
            bool: does exist ?
        """
        return os.path.exists(f"./database/{self.db_name}.db")

    def _check_tbl(self, tbl_name) -> bool:
        """Internal Use only
        
        Checks if a specific table exists

        Returns:
            bool: does exist ?
        """
        cur = self.db.cursor()
        sql_stmnt = f"""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='{tbl_name}';
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
        """Closes the database connection
        """
        self.db.close()


class generate_db(establish_db):
    """Used for database generation

    Args:
        establish_db (class): parent class
    """

    def __init__(self, db_name: str) -> None:
        super().__init__(db_name)

    def add_table(self, tbl_name: str, col: dict) -> bool:
        """With this function you can add tables to a Database

        Args:
            tbl_name (str): Tablename
            col (dict): Columns as Dict

            Supported Datatypes: 

            "INT", "INTEGER", "TINYINT", "SMALLINT", "MEDIUMINT", "BIGINT",
            "UNSIGNED BIG INT", "INT2", "INT8", "CHARACTER", "VARCHAR",
            "VARYING CHARACTER", "NCHAR", "NATIVE CHARACTER",
            "NVARCHAR", "TEXT", "CLOB", "CHAR", "BLOB", "REAL", "DOUBLE",
            "DOUBLE PRECISION", "FLOAT", "NUMERIC", "DECIMAL", "BOOLEAN",
            "DATE", "DATETIME"

            Dictionary Aufbau:

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

        Raises:
            SyntaxError: Invalid value inside the column specification

        Returns:
            bool: true if creation was successful
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
        self.db.commit()
        if res.fetchone is None:
            return False
        else:
            self.tables.append(tbl_name)
            return True

    def remove_table(self, tbl_name) -> bool:
        """_summary_

        Args:
            tbl_name (_type_): _description_

        Returns:
            bool: _description_
        """
        cur = self.db.cursor()
        sql_stmnt = f"""
                    DROP TABLE {tbl_name};
                    """
        if self._check_tbl(tbl_name):
            cur.execute(sql_stmnt)
            self.db.commit()
            if not self._check_tbl(tbl_name):
                self.tables.remove(tbl_name)
                return True
        return False

    def __col2string(self, col: dict) -> list:
        """Internal use only

        converts the column dictionary to a sql string

        Args:
            col (dict): input as dict. Formated like in Add_table

        Raises:
            ValueError: Only one Primary or Foreign key can be used

        Returns:
            list: Contents are the SQL statements
        """
        datatype_int = ["INT", "INTEGER", "TINYINT", "SMALLINT", "MEDIUMINT", "BIGINT",
            "UNSIGNED BIG INT", "INT2", "INT8"]        
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

            if (col[c]["autoincrement"] and col[c]["type"] in datatype_int
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
        """Checks if the Columsn got the right format

        Args:
            col (dict): input as dict. Formated like in Add_table

        Raises:
            KeyError: "Key don't match needed layout or spelling"
            TypeError: Datatype doesn't match needed
            ValueError: "Invalid value in column naming!"

        Returns:
            bool: valid columns if true
        """        
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
    """Used to operate the database

    Args:
        establish_db (class): parentclass
    """    

    def __init__(self, db_name: str) -> None:
        super().__init__(db_name)

    def del_content(self, tbl_name: str, search: dict) -> None:
        """Delete datasets based of a searchterm from the database

        IMPORTANT: Deletes directly!

        Args:
            tbl_name (str): Table where you would delete data
            search (dict): search term - see documentation for explaination
        """        
        cur = self.db.cursor()
        if self._check_tbl(tbl_name):
            sql_stmnt = f"""
                    DELETE FROM {tbl_name}
                    WHERE {list(search.keys())[0]} = ?;
                    """
            cur.execute(sql_stmnt, list(search.values()))

    def get_content(self, tbl_name: str) -> list:
        """Gets all datasets out of a table

        Args:
            tbl_name (str): Table you want to return

        Returns:
            list: returns a list of dicts with columnname and values
        """        
        self.db.row_factory = sql3.Row
        cur = self.db.cursor()
        if self._check_tbl(tbl_name):
            sql_stmnt = f"""
                    SELECT * FROM {tbl_name};
                    """
            cur.execute(sql_stmnt)
            data = list(map(dict, cur.fetchall()))
            return data
        else:
            return []

    def search_table(self, tbl_name: str, search: dict) -> list:
        """Search a table for a specific dataset

        Args:
            tbl_name (str): Table to search in
            search (dict): search term - see documentation for explaination

        Returns:
            list: returns a list of dicts with columnname and values
        """        
        self.db.row_factory = sql3.Row
        cur = self.db.cursor()
        if self._check_tbl(tbl_name):
            sql_stmnt = f"""
                    SELECT * FROM {tbl_name}
                    WHERE {list(search.keys())[0]} = ?;
                    """
            cur.execute(sql_stmnt, list(search.values()))
            data = list(map(dict, cur.fetchall()))
            return data
        else:
            return []

    def add_content(self, tbl_name: str, cntnt: dict | list[dict],
                    with_foreign_Key: bool | tuple = False) -> None:
        """_summary_

        Args:
            tbl_name (str): table to add to
            cntnt (dict | list[dict]): content you want to add. Single or list - see docs
            with_foreign_Key (bool | tuple, optional): Defaults to False.
        
        Explaination:

        with_foreign_Key: bool | list = False
        if is list:
            list[0] = "table": str
            list[1] = {"column": str, "pos_in_cntnt": int}
        """
        errors = [
            TypeError("Wrong Datatype given! dict or list of dict needed!"),
            ConnectionError("Table does not exist or could not be found!"),
            LookupError("Foreignkey does not exist or could not be found!"),
            TypeError("Wrong Datatype given! bool or list needed!"),
            LookupError("Columns do not match destination table!"),
            LookupError("Foreignkey does not exist or could not be found!")
        ]
        cur = self.db.cursor()
        if not with_foreign_Key:
            pass
        elif type(with_foreign_Key) is list and type(cntnt) is dict:
            result = self.search_table(with_foreign_Key[0],
                                       {
                                           with_foreign_Key[1]["column"]: cntnt[list(cntnt.keys())[with_foreign_Key[1]["pos_in_cntnt"]]]
                                           })
            if not result:
                raise errors[5]
        elif type(with_foreign_Key) is list and type(cntnt) is list:
            for d in cntnt:
                result = self.search_table(with_foreign_Key[0],
                                        {
                                            with_foreign_Key[1]["column"]: d[list(d.keys())[with_foreign_Key[1]["pos_in_cntnt"]]]
                                            })
                if not result:
                    raise errors[5]
        else:
            raise errors[3]
        if self._check_tbl(tbl_name):
            if type(cntnt) is dict:
                if not self._compare_cols(tbl_name, list(cntnt.keys())):
                    raise errors[4]
                sql_stmnt = f"""
                        INSERT INTO
                        {tbl_name}
                        ({",".join(list(cntnt.keys()))})
                        VALUES (
                            {','.join(['?' for x in cntnt.values()])}
                        );
                        """
                cur.execute(sql_stmnt, list(cntnt.values()))
            elif type(cntnt) is list:
                for elem in cntnt:
                    if type(elem) is dict:
                        if not self._compare_cols(tbl_name, list(elem.keys())):
                            raise errors[4]
                        sql_stmnt = f"""
                                INSERT INTO
                                {tbl_name}
                                ({",".join(list(elem.keys()))})
                                VALUES (
                                    {','.join(['?' for x in elem.values()])}
                                );
                                """
                        cur.execute(sql_stmnt, list(elem.values()))
                    else:
                        raise errors[0]
            else:
                raise errors[0]
        else:
            raise errors[1]
        self.db.commit()

    def _compare_cols(self, tbl_name: str, clmns: list) -> bool:
        """Comparing input columns with the destination Table

        Args:
            tbl_name (str): Table you want to compare to
            clmns (list): List of actual columns to compare

        Returns:
            bool: if columns match return true else false
        """
        i = 0
        cur = self.db.cursor()
        cur.execute(f"PRAGMA table_info({tbl_name});")
        actual_cols = cur.fetchall()
        for col in actual_cols:
            pos, name, data_type, notnull, dflt, pk = col
            if pk != 1:
                if name != clmns[i]:
                    return False
                i += 1
        return True
