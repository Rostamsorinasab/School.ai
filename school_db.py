import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "school.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables IF NOT EXISTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        name TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        class_id TEXT NOT NULL,
        grade INTEGER NOT NULL,
        FOREIGN KEY (id) REFERENCES users (id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        grade INTEGER NOT NULL,
        topic TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_option TEXT NOT NULL,
        FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        quiz_id INTEGER NOT NULL,
        score REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES users (id),
        FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        grade_val REAL NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (student_id) REFERENCES users (id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES users (id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (sender_id) REFERENCES users (id),
        FOREIGN KEY (receiver_id) REFERENCES users (id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        text TEXT NOT NULL,
        target TEXT NOT NULL,
        date TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        type TEXT NOT NULL,
        grade INTEGER NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        assignment_title TEXT NOT NULL,
        file_path TEXT,
        score REAL,
        feedback TEXT,
        date TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES users (id)
    )
    """)
    
    conn.commit()
    conn.close()

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    if user_count > 0:
        conn.close()
        return

    # Users
    users = [
        # Admin
        ("0012345678", "admin123", "admin", "علی احمدی (مدیر)"),
        # Teacher
        ("2280123456", "math123", "teacher", "رستم سوری نسب (دبیر ریاضی)"),
        # Student 1 (9th grade)
        ("3410123456", "123", "student", "جواد آژینه"),
        # Parent 1
        ("p_3410123456", "123", "parent", "ولیِ جواد آژینه"),
        # Other Students
        ("3410123451", "123", "student", "امیر عباسی"),
        ("3410123452", "123", "student", "مهدی قاسمی"),
        ("3410123453", "123", "student", "علیرضا رضایی"),
        ("3410123454", "123", "student", "حسین بهرامی"),
        ("3410123455", "123", "student", "امید مکرانی"),
        ("3410123457", "123", "student", "محمد هوتی"),
        ("p_3410123451", "123", "parent", "ولیِ امیر عباسی"),
        ("p_3410123452", "123", "parent", "ولیِ مهدی قاسمی"),
        ("p_3410123453", "123", "parent", "ولیِ علیرضا رضایی"),
        ("p_3410123454", "123", "parent", "ولیِ حسین بهرامی"),
        ("p_3410123455", "123", "parent", "ولیِ امید مکرانی"),
        ("p_3410123457", "123", "parent", "ولیِ محمد هوتی"),
    ]
    
    cursor.executemany("INSERT OR IGNORE INTO users (username, password, role, name) VALUES (?, ?, ?, ?)", users)
    
    # Students detail map
    students = [
        (3, "9-1", 9),
        (5, "9-1", 9),
        (6, "9-1", 9),
        (7, "8-1", 8),
        (8, "8-1", 8),
        (9, "7-1", 7),
        (10, "7-1", 7),
    ]
    cursor.executemany("INSERT OR IGNORE INTO students (id, class_id, grade) VALUES (?, ?, ?)", students)
    
    # Seed Announcements
    announcements = [
        ("اطلاعیه شروع کلاس‌های آنلاین ریاضی", "قابل توجه دانش‌آموزان عزیز متوسطه اول، با توجه به نزدیک شدن به امتحانات مستمر، کلاس‌های رفع اشکال آنلاین در سامانه فعال گردیده است. لطفاً حضور خود را ثبت نمایید.", "all", "1405/07/02"),
        ("جلسه انجمن اولیا و مربیان مدرسه", "از اولیای گرامی دعوت می‌شود در جلسه هم‌اندیشی بهبود وضعیت تحصیلی ریاضی دانش‌آموزان شرکت فرمایند.", "parents", "1405/07/05"),
        ("مسابقات خلاقیت ریاضی جاسک", "بخشنامه مسابقات شهرستانی خلاقیت ریاضی ابلاغ شد. دانش‌آموزان علاقه‌مند جهت ثبت‌نام به آقای سوری نسب مراجعه نمایند.", "students", "1405/07/10"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO announcements (title, text, target, date) VALUES (?, ?, ?, ?)", announcements)
    
    # Seed Events
    events = [
        ("امتحان مستمر فصل اول (توان و ریشه)", "1405/07/12", "exam", 9),
        ("کارگاه رفع اشکال مکتوب هندسه هشتم", "1405/07/15", "event", 8),
        ("امتحان مستمر هماهنگ پایه هفتم", "1405/07/18", "exam", 7),
    ]
    cursor.executemany("INSERT OR IGNORE INTO events (title, date, type, grade) VALUES (?, ?, ?, ?)", events)
    
    # Seed Grades
    grades = [
        (3, "ریاضی - مستمر هفته اول", 15.43, "1405/07/01", "ارزیابی کلاسی و تمرین‌های ریاضی"),
        (3, "ریاضی - مستمر هفته دوم", 17.27, "1405/07/08", "ارزیابی کلاسی و تمرین‌های ریاضی"),
        (3, "ریاضی - مستمر هفته سوم", 16.22, "1405/07/15", "ارزیابی کلاسی و تمرین‌های ریاضی"),
        (3, "ریاضی - مستمر هفته چهارم", 17.62, "1405/07/22", "ارزیابی کلاسی و تمرین‌های ریاضی"),
        
        (5, "ریاضی - مستمر هفته اول", 18.5, "1405/07/01", "عملکرد عالی در کلاس"),
        (5, "ریاضی - مستمر هفته دوم", 19.0, "1405/07/08", "تمرین‌های کلاسی"),
        (5, "ریاضی - مستمر هفته سوم", 18.0, "1405/07/15", "ارزیابی کلاسی"),
        (5, "ریاضی - مستمر هفته چهارم", 19.1, "1405/07/22", "آزمون کلاسی"),
        
        (6, "ریاضی - مستمر هفته اول", 14.5, "1405/07/01", "نیاز به تلاش بیشتر"),
        (6, "ریاضی - مستمر هفته دوم", 15.0, "1405/07/08", "خوب"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO grades (student_id, subject, grade_val, date, description) VALUES (?, ?, ?, ?, ?)", grades)
    
    # Seed Quizzes
    cursor.execute("SELECT COUNT(*) FROM quizzes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO quizzes (title, grade, topic) VALUES (?, ?, ?)", ("آزمون خودکار مبحث توان و ریشه نهم", 9, "توان و ریشه"))
        quiz_id = cursor.lastrowid
        
        questions = [
            (quiz_id, "حاصل عبارت 2 به توان 3 ضربدر 2 به توان 4 کدام است؟", "2 به توان 12", "4 به توان 7", "2 به توان 7", "4 به توان 12", "C"),
            (quiz_id, "ریشه سوم عدد منفی 8 کدام است؟", "-2", "2", "-4", "وجود ندارد", "A"),
            (quiz_id, "کدام عدد بین رادیکال 2 و رادیکال 3 قرار دارد؟", "1.2", "1.5", "1.8", "2.1", "B"),
            (quiz_id, "ساده شده رادیکال 50 کدام است؟", "2 رادیکال 5", "5 رادیکال 2", "25 رادیکال 2", "10 r", "B"),
        ]
        cursor.executemany("INSERT INTO quiz_questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option) VALUES (?, ?, ?, ?, ?, ?, ?)", questions)
        cursor.execute("INSERT INTO quiz_attempts (student_id, quiz_id, score, date) VALUES (?, ?, ?, ?)", (3, quiz_id, 20.0, "1405/07/12"))
    
    # Seed Attendance
    attendance = [
        (3, "حاضر", "1405/07/01"),
        (3, "غایب", "1405/07/08"),
        (3, "حاضر", "1405/07/15"),
        (3, "حاضر", "1405/07/22"),
        
        (5, "حاضر", "1405/07/01"),
        (5, "حاضر", "1405/07/08"),
        (5, "حاضر", "1405/07/15"),
        (5, "حاضر", "1405/07/22"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO attendance (student_id, status, date) VALUES (?, ?, ?)", attendance)
    
    # Seed Submissions (Worksheets)
    cursor.execute("SELECT COUNT(*) FROM submissions")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO submissions (student_id, assignment_title, file_path, score, feedback, date) VALUES (?, ?, ?, ?, ?, ?)",
                       (3, "کاربرگ مبحث قوانین توان", "assignment_jawad.pdf", 19.5, "بسیار خوش‌خط و دقیق حل شده است. روی سوال ۴ مجدداً تمرکز کنید.", "1405/07/08"))
    
    # Seed Messages
    messages = [
        (2, 4, "سلام جناب آژینه، لطفاً وضعیت تکالیف ریاضی جواد را پیگیری کنید.", "1405/07/03"),
        (4, 2, "سلام استاد سوری نسب بزرگوار، چشم حتماً پیگیری می‌کنم. از زحمات شما سپاسگزارم.", "1405/07/04"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO messages (sender_id, receiver_id, text, date) VALUES (?, ?, ?, ?)", messages)
    
    conn.commit()
    conn.close()

def ensure_db_initialized():
    init_db()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        has_users = cursor.fetchone() is not None
        if has_users:
            cursor.execute("SELECT COUNT(*) FROM users")
            user_cnt = cursor.fetchone()[0]
            if user_cnt == 0:
                seed_data()
        else:
            seed_data()
        conn.close()
    except Exception:
        seed_data()

if __name__ == "__main__":
    ensure_db_initialized()
    print("Database initialized and ensured successfully!")
