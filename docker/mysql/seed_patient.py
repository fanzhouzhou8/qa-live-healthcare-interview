# -*- coding: utf-8 -*-
import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="qa_healthcare",
    charset="utf8mb4",
    autocommit=True,
)
cur = conn.cursor()
cur.execute(
    """
CREATE TABLE IF NOT EXISTS patient (
  id VARCHAR(32) PRIMARY KEY,
  username VARCHAR(64) NOT NULL UNIQUE,
  password VARCHAR(128) NOT NULL,
  name VARCHAR(64) NOT NULL,
  birthday DATE NULL,
  phone VARCHAR(32) NULL,
  gender VARCHAR(16) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
"""
)
cur.execute("DELETE FROM patient")

patients = [
    ("patient001", "patient_zhaoming", "123456", "赵明", "1985-03-15", "138****1234", "男"),
    ("patient002", "patient_sunli", "123456", "孙丽", "1990-07-22", "139****5678", "女"),
    ("patient003", "patient_zhoujie", "123456", "周杰", "1978-11-08", "137****9012", "男"),
    ("patient004", "patient_wufang", "123456", "吴芳", "1995-05-20", "136****3456", "女"),
    ("patient005", "patient_zhenghao", "123456", "郑浩", "1988-09-12", "135****7890", "男"),
]

cur.executemany(
    """
INSERT INTO patient (id, username, password, name, birthday, phone, gender)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""",
    patients,
)

cur.execute("SELECT id, username, name FROM patient")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()
print("DONE")
