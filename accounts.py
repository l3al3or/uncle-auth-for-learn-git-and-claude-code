"""
accounts.py
ชั้น business logic ของระบบบัญชีผู้ใช้
ทำหน้าที่เชื่อม security.py (รหัสผ่าน) เข้ากับ storage.py (เก็บข้อมูล)
แยกออกมาเป็น module เดี่ยว ๆ ตั้งแต่ EP.7 (Refactoring)

หลักการ: app.py (routes) จะเรียกใช้ฟังก์ชันในไฟล์นี้เท่านั้น
ไม่ยุ่งกับ storage หรือ security ตรง ๆ
"""

from datetime import datetime

import security
import storage


class AccountError(Exception):
    """error กลางของระบบบัญชี ใช้ส่งข้อความให้ผู้ใช้เห็น"""
    pass


def register_user(username: str, password: str) -> None:
    """สมัครสมาชิกใหม่"""
    username = (username or "").strip()
    if not username:
        raise AccountError("กรุณากรอกชื่อผู้ใช้")
    if not password:
        raise AccountError("กรุณากรอกรหัสผ่าน")

    users = storage.load_users()
    if username in users:
        raise AccountError("ชื่อผู้ใช้นี้ถูกใช้แล้ว")

    users[username] = {
        "password_hash": security.hash_password(password),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    storage.save_users(users)


def authenticate(username: str, password: str) -> bool:
    """ตรวจสอบ login ว่า username/password ถูกต้องหรือไม่"""
    username = (username or "").strip()
    users = storage.load_users()
    user = users.get(username)
    if not user:
        return False
    return security.verify_password(password, user["password_hash"])


def change_password(username: str, old_password: str, new_password: str) -> None:
    """เปลี่ยนรหัสผ่าน: ต้องยืนยันรหัสเดิมให้ถูกก่อน"""
    username = (username or "").strip()
    users = storage.load_users()
    user = users.get(username)
    if not user:
        raise AccountError("ไม่พบผู้ใช้นี้")

    if not security.verify_password(old_password, user["password_hash"]):
        raise AccountError("รหัสผ่านเดิมไม่ถูกต้อง")

    if not new_password:
        raise AccountError("กรุณากรอกรหัสผ่านใหม่")

    user["password_hash"] = security.hash_password(new_password)
    storage.save_users(users)
