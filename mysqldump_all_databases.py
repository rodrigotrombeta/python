import mysql.connector
import os
import time
import subprocess
import shutil

# Git: https://gist.github.com/rodrigotrombeta/31471bef5d2a3143e4e0fcf1041af1b4

##################
# Connect to MySQL instance and retrieve databases to be dumped.
HOST="192.168.1.132"
PORT='3306'
DB_USER="root"
DB_PASS="*****"

conn = mysql.connector.connect(host=HOST,port=PORT,user=DB_USER,password=DB_PASS,database="mysql")
cursor = conn.cursor()

# Query
database_list=("SELECT distinct table_schema FROM information_schema.tables where table_schema not in ('information_schema','mysql','performance_schema') ")
cursor.execute(database_list)

# Save results in an array
list_of_databases = cursor.fetchall()
list_of_databases = [ position[0] for position in list_of_databases ]

# close connection and cursor
conn.close()
cursor.close()

list_size=len(list_of_databases)
# print("Number of databases:", list_size)

##################
# DUMP DATABASES:
def dump_databases(database):
  dir_timestamp = time.strftime('%Y-%m-%d')
  backup_path = os.path.join("/mnt/data",dir_timestamp)
  if os.path.exists(backup_path) and os.path.isdir(backup_path):
    shutil.rmtree(backup_path)
  os.mkdir(backup_path)
  for database_name in list_of_databases:
    os.popen("mysqldump -h %s -P %s -u %s -p%s %s > %s/%s.sql" % (HOST,PORT,DB_USER,DB_PASS,database_name,backup_path,database_name))
    print("\n|| Database dumped to "+backup_path+"/"+database_name+".sql")

##################
if __name__=="__main__":
 dump_databases(list_of_databases)
