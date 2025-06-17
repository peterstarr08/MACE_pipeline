import sqlite3
from config import db_path
from pathlib import Path

if not db_path.exists():
    raise FileNotFoundError(f'Database file {db_path} not found. Can\' do shit')

def get_connection():
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#Table wise writing
def insert_raw_dataset(data: tuple):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "insert into raw_dataset (repr, label) values (?,?)", data
        )
        conn.commit()

def insert_dataset(data: tuple):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "insert into dataset (repr, label, operation) values (?,?,?)", data
        )
        conn.commit()

#Table wise reading
def get_dataset(label: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "select repr, label, operation from dataset where label=(?)", (label,)
        )
        return cursor.fetchone()


def get_raw_dataset(label: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "select repr, label from raw_dataset where label=(?)", (label,)
        )
        return cursor.fetchone()


def get_label():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "select label from raw_dataset"
        )
        return cursor.fetchall()