"""
storage.py
ชั้นเก็บข้อมูล (persistence layer): อ่าน/เขียน users ลงไฟล์ JSON
แยกออกมาเป็น module เดี่ยว ๆ ตั้งแต่ EP.7 (Refactoring)

โครงสร้างข้อมูล users.json:
{
    "username": {
        "password_hash": "...",
        "created_at": "2026-01-01T10:00:00"
    }
}
"""

import json
import os

# path ของไฟล์ข้อมูล (override ได้ใน test ด้วยการ set ค่านี้)
DB_PATH = os.path.join(os.path.dirname(__file__), "users.json")


def _get_path() -> str:
    return DB_PATH


def load_users() -> dict:
    """โหลด users ทั้งหมดจากไฟล์ ถ้าไฟล์ยังไม่มีให้คืน dict ว่าง"""
    path = _get_path()
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)


def save_users(users: dict) -> None:
    """บันทึก users ทั้งหมดลงไฟล์ (เขียนทับทั้งก้อน)"""
    path = _get_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
