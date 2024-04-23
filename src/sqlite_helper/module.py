import sqlite3

@staticmethod
def __check_db(name: str) -> bool:
    exst = False
    return exst

class generator():

    def __init__(self, db_name: str) -> None:
        if __check_db(db_name):
            pass
        else:
            self.__gen_db()
    
    def __gen_db(self) -> bool:
        scss = False
        return scss
    
    def add_table(self, tbl_name: str, col: dict) -> bool:
        scss = False
        return scss


class establish():

    def __init__(self, db_name: str) -> None:
        if not __check_db(db_name):
            raise ConnectionError("Database does not exist. Check name or generate a database first!")
