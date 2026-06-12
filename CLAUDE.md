# uncle-auth — คู่มือโปรเจกต์สำหรับ Claude Code

เว็บระบบสมาชิก (register / login / change password) เขียนด้วย Flask
ไฟล์นี้คือ context ถาวรที่ Claude ต้องอ่านและทำตามทุกครั้ง

## โครงสร้างโปรเจกต์ (หลัง refactor EP.7)
- `app.py` — ชั้น routes ของเว็บ (slim) เรียกใช้ accounts.py เท่านั้น
- `accounts.py` — business logic (register, authenticate, change_password)
- `security.py` — hash / verify รหัสผ่าน (อย่าเก็บรหัสเป็น plain text เด็ดขาด)
- `storage.py` — อ่าน/เขียน users.json
- `templates/` — หน้าเว็บ (Jinja2)
- `tests/` — integration test (รันด้วย `pytest`)

## กฎการเขียนโค้ด
- routes ห้ามเรียก storage / security ตรง ๆ ให้ผ่าน accounts.py เสมอ
- ทุก feature ใหม่ต้องมี test และ test เดิมต้องไม่แดง
- รหัสผ่านต้องถูก hash ก่อนเก็บเสมอ

## กฎ Git (สำคัญ — ทำตามทุกครั้ง)
- ห้ามทำงานบน branch main โดยตรง แตก branch ใหม่เสมอ
- ตั้งชื่อ branch: `feature/<ชื่อสั้น>` หรือ `fix/<ชื่อสั้น>`
- commit message ใช้รูปแบบ Conventional Commits:
  `feat:` เพิ่มของใหม่ / `fix:` แก้บั๊ก / `refactor:` ปรับโครงสร้าง
  `test:` เพิ่ม/แก้เทสต์ / `docs:` แก้เอกสาร
- 1 commit = 1 เรื่อง (atomic) ห้ามเหมารวมหลายเรื่องใน commit เดียว
- ก่อนเปิด PR ต้องรัน `pytest` ให้เขียวก่อนเสมอ
- PR description ต้องมี 3 ส่วน: What (ทำอะไร) / Why (ทำไม) / Test plan (ทดสอบยังไง)

## คำสั่งที่ใช้บ่อย
- รันเว็บ: `python app.py`  (เปิด http://localhost:5000)
- รันเทสต์: `pytest -v`
