import sqlite3

@staticmethod
def __check_db(name: str, path: str) -> bool:
    exst = False
    return exst

class generator():

    def __init__(self, name: str, path: str) -> None:
        if __check_db:
            pass
        else:
            self.__db(name, path)
    
    def __db(self, name: str, path: str) -> bool:
        scss = False
        return scss
    
    def add_table(self, name: str, col: dict) -> bool:
        scss = False
        return scss


class establish():

    def __init__(self) -> None:
        if not __check_db:
            raise ConnectionError("Database does not exist. Please check the path or generate a database first!")
