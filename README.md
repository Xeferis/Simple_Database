# Simple_Database  

[Report Bugs](https://github.com/Xeferis/Simple_Database/issues/new/choose)  

A Module wich can be used to generate, establish connection and use SQLite Databases in Python with minimal effort.

Alpha state - see [Milestones](https://github.com/Xeferis/Simple_Database/milestones) for planned developments.

# Documentation

It's also found in the [Wiki](https://github.com/Xeferis/Simple_Database/wiki).

### Collection of Classes and Functions
<details>
<summary><h2>class: establish_db()</h2></summary>  

Parameters:  
`db_name: str`  

To initialize a Database you have to give it a name or, if a database already exists, provide a name.  
🛑 Normally not used standalone, it inherits to the other classes! 🛑

_Excample:_  
```
db = establish_db("expml")  
``` 

<details>
<summary><h3>Functions</h3></summary>  

* ### `close()`  

</details>

Just use the "close" tag on the database clase to close this connection  

_Excample:_
```
db = establish_db("expml")
#some code  
db.close()  
```

</details>

<details>
<summary><h2>class: generate_db()</h2></summary>  

Parameters:  
`db_name: str`

This class is used to build up a database. Fill it with tables or delete tables.
It inherits from "establish_db" so it also needs the database name to generate a database or open a connection.

_Excample:_
```
db = generate_db("expml")
```

<details>
<summary><h3>Functions</h3></summary>  

* ### `add_table()`  
Parameters:  
`tbl_name: str`  
`col: dict`  

Return:  
`bool`   


Adding tables to your database by giving it a name and the column information. The dict for the column information ist structured like this:  
```  
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
```
  
_Excample:_
```
db = generate_db("expml")
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
db.close()
```


* ### `remove_table()`
 
Parameters:  
`tbl_name: str`   

Return:  
`bool`   

This will remove a table of the database by its given name. 

IMPORTANT: It will delete the table no matter what! Watch out if it has foreign relations

Will return true if deletion was successful

_Excample:_
```
db = generate_db("expml")
db.remove_table(tbl_name: str)
db.close()
```

</details>

</details>

<details>
<summary><h2>class: operate_db()</h2></summary>

Parameters:  
`db_name: str`

This class is used to operate a database. You can add, del, get and search content in a database

_Excample:_
```
db = operate_db("expml")
```

<details>
<summary><h3>Functions</h3></summary>  

* ### `add_content()`
 
Parameters:  
`tbl_name: str` 
`cntnt: dict | list[dict]`  
`with_foreign_key: bool | tuple -> defaults to false`   
   
You can add single lines of data or add a whole batch of data as a list. With the foreign key parameter you can give it a table and the key that should be added. It tests if the key exists in the destination table. 

_Excample 1 (Single Data):_
```
# DB is already initialized and table "Users" is added
data1 = {'Name': 'John', 'Age': 30}
db.add_content('Users', data1)
```

_Excample 2 (Batch Data):_
```
# DB is already initialized and table "Users" is added
data2 = [{'Name': 'John', 'Age': 30},
{'Name': 'Sarah', 'Age': 27},
{'Name': 'Genji', 'Age': 35}]
db.add_content('Users', data1)
```

_Excample 3 (Foreign key):_
```
# DB is already initialized and table "Users" & "Department" are added.
# The Department ID 423 is also already added
data3 = {'Name': 'John', 'Age': 30}
db.add_content('Users', data1, ("Department" {"DID": 423}))
db.close()
```

* ### `update_content()`
 
Parameters:  
`tbl_name: str` 
`search: dict`
`cntnt: dict | dict`  
 
   
You can update datasets by searching for it and then fill the new information.

_Excample 1:_
```
# DB is already initialized and table "Users" is added.
# The database has a dataset with the id 456 and a current name of "bob"
tbl = "users"
dataset2update = {"id": 456}
data2update = {"name": "john"}
db.update_content(tbl, dataset2update, data2update)
# Now the dataset with the id 465 should have the name "john" and not "bob" anymore
```

* ### `del_content()`
 
Parameters:  
`tbl_name: str` 
`search: dict`

You can remove content with this function by searching for attributes. All datasets that will be found are going to be deleted.

IMPORTANT: There is no confirmation. If it finds something it deletes it.
   

_Excample:_
```
# DB is already initialized and table "Users" is added.
# The Dataset for the name "Bob" is added.
data2delete = {'name': 'Bob'}
db.del_content('Users', data2delete)
# Now all Data where the name was "Bob" has been deleted!
```

* ### `get_content()`
 
Parameters:  
`tbl_name: str` 

Returns:  
`list`
   

With this you get all the data from a specific table.

_Excample:_
```
# DB is already initialized and table "Users" is added.
# The Database is filled with data
data = db.get_content('Users')
print(data)
# Now all Data will be printed
```

* ### `search_table()`
 
Parameters:  
`tbl_name: str` 
`search: dict`

Returns:  
`list`
   
You can search for specific datasets and all the found data will be returned as list

_Excample:_
```
# DB is already initialized and table "Users" is added.
# The Database is filled with data
data2search = {'name': 'Bob'}
found_data = db.search_content('Users', data2search)
print(found_data)
# Now all Datasets with the name "Bob" will be printed
```

</details>

</details>
