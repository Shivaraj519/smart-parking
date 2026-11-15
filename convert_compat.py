import re
import os
import sys

def convert_to_sqlite(mysql_file, sqlite_file):
    with open(mysql_file, 'r', encoding='utf-8') as f:
        sql = f.read()

    # Remove MySQL specific directives
    sql = re.sub(r'DROP DATABASE .*?;', '', sql)
    sql = re.sub(r'CREATE DATABASE .*?;', '', sql)
    sql = re.sub(r'USE .*?;', '', sql)
    sql = re.sub(r'ENGINE=InnoDB', '', sql)
    sql = re.sub(r'CHARACTER SET .*? COLLATE .*?;', ';', sql)
    sql = re.sub(r'AUTO_INCREMENT', 'AUTOINCREMENT', sql)
    sql = re.sub(r'INT AUTOINCREMENT PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT', sql)
    sql = re.sub(r'ENUM\([^)]+\)', 'TEXT', sql)
    sql = re.sub(r'BOOLEAN DEFAULT (TRUE|FALSE)', r'INTEGER DEFAULT \1', sql)
    sql = sql.replace('TRUE', '1').replace('FALSE', '0')
    sql = re.sub(r'NOW\(\)', "datetime('now')", sql)
    sql = re.sub(r'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP', 'CURRENT_TIMESTAMP', sql)

    # Separate DELIMITER blocks (procedures & triggers)
    parts = sql.split('DELIMITER $$')
    schema_clean = parts[0]

    with open(sqlite_file, 'w', encoding='utf-8') as f:
        f.write(schema_clean)

if __name__ == '__main__':
    convert_to_sqlite('schema.sql', 'schema_sqlite_compat.sql')
    print('Converted schema for testing/fallback if needed.')
