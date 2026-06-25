"""
accounts.py
ชั้น business logic ของระบบบัญชีผู้ใช้
ทำหน้าที่เชื่อม security.py (รหัสผ่าน) เข้ากับ storage.py (เก็บข้อมูล)
แยกออกมาเป็น module เดี่ยว ๆ ตั้งแต่ EP.7 (Refactoring)

หลักการ: app.py (routes) จะเรียกใช้ฟังก์ชันในไฟล์นี้เท่านั้น
ไม่ยุ่งกับ storage หรือ security ตรง ๆ
"""

from datetime import datetime, timedelta

import security
import storage


class AccountError(Exception):
    """error กลางของระบบบัญชี ใช้ส่งข้อความให้ผู้ใช้เห็น"""
    pass


LOCKOUT_THRESHOLD = 5
LOCKOUT_DURATION_MINUTES = 15


def _parse_locked_until(value):
    if not value:
        return None
    return datetime.fromisoformat(value)


def _is_locked(user: dict) -> bool:
    locked_until = _parse_locked_until(user.get("locked_until"))
    if not locked_until:
        return False
    return datetime.now() < locked_until


def _reset_lock_state(user: dict, users: dict) -> None:
    if user.get("failed_attempts") != 0 or user.get("locked_until") is not None:
        user["failed_attempts"] = 0
        user["locked_until"] = None
        storage.save_users(users)


def _record_failed_attempt(user: dict, users: dict) -> None:
    attempts = user.get("failed_attempts", 0) + 1
    user["failed_attempts"] = attempts
    if attempts >= LOCKOUT_THRESHOLD:
        user["locked_until"] = (
            datetime.now() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
        ).isoformat(timespec="seconds")
    storage.save_users(users)


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
        "failed_attempts": 0,
        "locked_until": None,
    }
    storage.save_users(users)


def authenticate(username: str, password: str) -> bool:
    """ตรวจสอบ login ว่า username/password ถูกต้องหรือไม่"""
    username = (username or "").strip()
    users = storage.load_users()
    user = users.get(username)
    if not user:
        return False

    if _is_locked(user):
        return False

    return security.verify_password(password, user["password_hash"])


def login(username: str, password: str) -> bool:
    """ลองล็อกอินและบังคับใช้นโยบายล็อกบัญชี"""
    username = (username or "").strip()
    users = storage.load_users()
    user = users.get(username)
    if not user:
        return False

    if _is_locked(user):
        raise AccountError(
            "บัญชีถูกล็อกชั่วคราว โปรดลองใหม่อีกครั้งหลังจาก 15 นาที"
        )

    if not security.verify_password(password, user["password_hash"]):
        _record_failed_attempt(user, users)
        return False

    _reset_lock_state(user, users)
    return True


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
