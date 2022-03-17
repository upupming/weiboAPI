import mysql.connector
from .config import *

MYDB = mysql.connector.connect(**config['mysql']['CONNECTION'])
MYCURSOR = MYDB.cursor()

def create_db_if_not_exists():
    MYCURSOR.execute('create database if not exists seq2emoji')
def create_table_if_not_exists():
    """
    返回指向表的 MYDB 和 MYCURSOR
    """
    global MYDB, MYCURSOR
    MYDB = mysql.connector.connect(**config['mysql']['CONNECTION'], database='seq2emoji')
    MYCURSOR = MYDB.cursor()
    
    # Crawling
    MYCURSOR.execute("""
        create table if not exists Crawling (
            uid varchar(255) not null unique,
            uname varchar
            (255) CHARACTER SET utf8mb4 collate utf8mb4_unicode_520_ci,
            primary key (uid)
        )
    """)
    MYCURSOR.execute("SELECT * FROM Crawling")
    myresult = MYCURSOR.fetchall()
    # 当前没有正在抓取的用户，就初始化一下
    if len(myresult) == 0:
        MYCURSOR.execute('insert into Crawling (uid, uname) values (%s, %s)', (config['crawl']['START_USER'], None))
        MYDB.commit()
    # Crawled
    MYCURSOR.execute("""
        create table if not exists Crawled (
            uid varchar(255) not null unique,
            uname varchar
            (255) CHARACTER SET utf8mb4 collate utf8mb4_unicode_520_ci,
            primary key (uid)
        )
    """)
    # Weibo
    MYCURSOR.execute("""
        create table if not exists Weibo (
            uid varchar(255),
            mid varchar(255) not null unique,
            text text CHARACTER SET utf8mb4 collate utf8mb4_unicode_520_ci,
            img_emoji json,
            primary key (mid)
        )
    """)
    # Comment
    MYCURSOR.execute("""
        create table if not exists Comment (
            mid varchar(255) not null,
            cid varchar(255) not null unique,
            text text CHARACTER SET utf8mb4 collate utf8mb4_unicode_520_ci,
            img_emoji json,
            primary key (cid)
        )
    """)

    return (MYDB, MYCURSOR)
