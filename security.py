"""
security.py
จัดการเรื่องความปลอดภัยของรหัสผ่าน: hash และ verify
แยกออกมาเป็น module เดี่ยว ๆ ตั้งแต่ EP.7 (Refactoring)
"""

from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(plain_password: str) -> str:
    """แปลงรหัสผ่าน plain text เป็น hash ที่ปลอดภัย (pbkdf2)"""
    if not plain_password:
        raise ValueError("password ห้ามเป็นค่าว่าง")
    return generate_password_hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ตรวจว่ารหัสผ่านที่กรอกมา ตรงกับ hash ที่เก็บไว้หรือไม่"""
    if not plain_password or not hashed_password:
        return False
    return check_password_hash(hashed_password, plain_password)
