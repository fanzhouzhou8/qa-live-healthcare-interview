# -*- coding: utf-8 -*-
import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    charset="utf8mb4",
    autocommit=True,
)
cur = conn.cursor()
cur.execute("DROP DATABASE IF EXISTS qa_healthcare")
cur.execute(
    "CREATE DATABASE qa_healthcare DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
)
cur.execute("USE qa_healthcare")
cur.execute(
    """
CREATE TABLE doctor (
  id VARCHAR(32) PRIMARY KEY,
  username VARCHAR(64) NOT NULL UNIQUE,
  password VARCHAR(128) NOT NULL,
  name VARCHAR(64) NOT NULL,
  title VARCHAR(64) NOT NULL,
  department VARCHAR(64) NOT NULL,
  avatar VARCHAR(512) NOT NULL,
  experience VARCHAR(128) NOT NULL,
  specialties JSON NOT NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
"""
)

doctors = [
    (
        "doc001",
        "dr-zhang-wei",
        "123456",
        "张伟医生",
        "主任医师",
        "心内科",
        "https://images.pexels.com/photos/5215024/pexels-photo-5215024.jpeg?auto=compress&cs=tinysrgb&w=400",
        "15年临床经验",
        '["高血压", "冠心病", "心律失常"]',
        1,
    ),
    (
        "doc002",
        "dr-li-na",
        "123456",
        "李娜医生",
        "副主任医师",
        "儿科",
        "https://images.pexels.com/photos/5327585/pexels-photo-5327585.jpeg?auto=compress&cs=tinysrgb&w=400",
        "10年临床经验",
        '["儿童感冒", "儿童发育", "疫苗接种"]',
        1,
    ),
    (
        "doc003",
        "dr-wang-qiang",
        "123456",
        "王强医生",
        "主治医师",
        "骨科",
        "https://images.pexels.com/photos/5452293/pexels-photo-5452293.jpeg?auto=compress&cs=tinysrgb&w=400",
        "8年临床经验",
        '["骨折", "关节炎", "运动损伤"]',
        1,
    ),
    (
        "doc004",
        "dr-liu-min",
        "123456",
        "刘敏医生",
        "主任医师",
        "妇产科",
        "https://images.pexels.com/photos/5452201/pexels-photo-5452201.jpeg?auto=compress&cs=tinysrgb&w=400",
        "18年临床经验",
        '["孕期保健", "妇科炎症", "产后恢复"]',
        0,
    ),
    (
        "doc005",
        "dr-chen-jie",
        "123456",
        "陈杰医生",
        "副主任医师",
        "消化内科",
        "https://images.pexels.com/photos/5215024/pexels-photo-5215024.jpeg?auto=compress&cs=tinysrgb&w=400",
        "12年临床经验",
        '["胃炎", "肠道疾病", "肝病"]',
        1,
    ),
]

cur.executemany(
    """
INSERT INTO doctor
(id, username, password, name, title, department, avatar, experience, specialties, is_active)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,CAST(%s AS JSON),%s)
""",
    doctors,
)

cur.execute("SELECT id, name, department, specialties, is_active FROM doctor")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()
print("DONE")
