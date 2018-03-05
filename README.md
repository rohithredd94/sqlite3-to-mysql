# sqlite3-to-mysql
Python Script to convert sqlite3 SQL dump to MySQL compatible format (Handles Foreign Key constraints)

### Python Compatibility:
* Python 2 and 3

## Usage
**Step 0: Clone the repo**
    
    root@localhost:~$ git clone https://github.com/rohithredd94/sqlite3-to-mysql.git
    root@localhost:~$ cd sqlite3-to-mysql/
**Step 1: Dump sqlite database**

    root@localhost:~/sqlite3-to-mysql$ sqlite3 db.sqlite3
    SQLite version 3.13.0 2016-05-18 10:57:30
    Enter ".help" for usage hints.
    sqlite> .output sqlite3_dump.sql
    sqlite> .dump
    sqlite> .exit

**Step 2: Convert to MySQL Format**

Syntax: python3 <input sql file> <output sql file>

Example:

    root@localhost:~/sqlite3-to-mysql$ python sqlite_to_mysql.py sqlite3_dump.sql mysql_source.sql

The MySQL compatible file is now stored in mysql_source.sql

**Note:** SQLite dump doesn't consider foreign key constraints and so the order of the tables in dump might be messed up. The user has to **manually** rearrange the tables before importing to MySQL.

**Step 3: Import to MySQL**

    root@localhost:~/sqlite3-to-mysql$ mysql -u root -p
    Enter password:
    mysql> create database test;
    Query OK, 1 row affected (0.00 sec)

    mysql> use database test;
    Database Changed
    mysql> source mysql_source.sql

The database should now be populated.
