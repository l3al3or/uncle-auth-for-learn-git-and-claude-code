# SETUP — เตรียมเครื่องสำหรับ Week 8 (Git & GitHub)

## 1. ตรวจ Git (ติดตั้งไว้ตั้งแต่ EP.1)
    git --version

## 2. ติดตั้ง GitHub CLI (gh) — ของใหม่ของ EP นี้
ใช้สั่งสร้าง PR และคุยกับ GitHub จาก terminal

macOS:
    brew install gh

Windows (PowerShell):
    winget install --id GitHub.cli

ตรวจว่าได้:
    gh --version

## 3. login เข้า GitHub
    gh auth login
เลือก: GitHub.com -> HTTPS -> Login with a web browser
ทำตามขั้นตอนจนเห็น "Logged in as <username>"

ตรวจสถานะ:
    gh auth status

## 4. ตั้งชื่อผู้เขียน commit (ถ้ายังไม่เคยตั้ง)
    git config --global user.name "ชื่อคุณ"
    git config --global user.email "อีเมลที่ใช้กับ GitHub"

## 5. (OPTIONAL — สำหรับผู้สอน demo เท่านั้น) ใช้ @claude review บน GitHub
นักเรียน "ไม่ต้องทำ" ข้อนี้ใน workshop — workshop ทำ review ในเครื่อง (local) ครบแล้ว
ข้อนี้ไว้สำหรับผู้สอนที่อยาก demo @claude บน GitHub สดให้ดู (ใช้แผน Pro/Max)
สร้าง OAuth token จาก subscription ของตัวเอง:
    claude setup-token
เก็บค่าที่ได้ไปใส่เป็น repository secret ชื่อ CLAUDE_CODE_OAUTH_TOKEN
(อย่า commit token ลงโค้ดเด็ดขาด — ทบทวน API Key Safety จาก EP.5)
