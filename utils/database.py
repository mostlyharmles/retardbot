# utils/database.py
import sqlite3
from config import DATABASE_PATH


def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS user_tokens
                 (user_id INTEGER PRIMARY KEY, tokens INTEGER)"""
    )
    conn.commit()
    conn.close()


def get_user_tokens(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT tokens FROM user_tokens WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0


def set_user_tokens(user_id, tokens):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO user_tokens (user_id, tokens) VALUES (?, ?)",
        (user_id, tokens),
    )
    conn.commit()
    conn.close()
    return tokens == 0  # Return True if tokens are 0, False otherwise


def reset_all_user_tokens():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("UPDATE user_tokens SET tokens = 0")
    affected_rows = c.rowcount
    conn.commit()
    conn.close()
    return affected_rows
