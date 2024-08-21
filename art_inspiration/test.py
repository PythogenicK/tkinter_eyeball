import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
import sqlite3
from numpy import random

bg_color = "#3d6466"
connection = sqlite3.connect("data/productions.db")
cursor = connection.cursor()
id_gen = random.randint(1,99999)


def get_all_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    conn.close()
    
    return [table[0] for table in tables]
