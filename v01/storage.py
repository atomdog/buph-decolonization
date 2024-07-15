import sqlite3
conn = sqlite3.connect('pubmed.db')
cursor = conn.cursor()

# Create Articles Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Articles (
    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
    articleTitle TEXT NOT NULL,
    journalTitle TEXT,
    datePublished TEXT,
    abstract TEXT
)
''')

# Create Authors Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    authorName TEXT NOT NULL
)
''')

# Create Departments Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    departmentName TEXT NOT NULL,
    location TEXT
)
''')

# Create ArticleAuthors Table (many-to-many relationship)
cursor.execute('''
CREATE TABLE IF NOT EXISTS ArticleAuthors (
    article_id INTEGER,
    author_id INTEGER,
    department_id INTEGER,
    FOREIGN KEY (article_id) REFERENCES Articles(article_id),
    FOREIGN KEY (author_id) REFERENCES Authors(author_id),
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    PRIMARY KEY (article_id, author_id)
)
''')