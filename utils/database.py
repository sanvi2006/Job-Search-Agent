import sqlite3
from datetime import datetime

DB_PATH = "job_tracker.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            salary TEXT,
            status TEXT DEFAULT 'Applied',
            link TEXT,
            date_added TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_job(title, company, location="", salary="", status="Applied", link=""):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO saved_jobs (title, company, location, salary, status, link, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, company, location, salary, status, link, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"DB error: {e}")
        return False


def get_saved_jobs():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM saved_jobs ORDER BY date_added DESC")
        jobs = cursor.fetchall()
        conn.close()
        return jobs
    except Exception:
        return []


def update_job_status(job_id, status):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE saved_jobs SET status = ? WHERE id = ?", (status, job_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def delete_job(job_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saved_jobs WHERE id = ?", (job_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False