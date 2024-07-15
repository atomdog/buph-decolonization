import sqlite3
conn = sqlite3.connect('pubmed.db')
cursor = conn.cursor()

# Create Articles Table
def instantiate():
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
        latitude REAL,
        longitude REAL
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


def insert_article(articleTitle, journalTitle, datePublished, abstract):
    cursor.execute('''
    INSERT INTO Articles (articleTitle, journalTitle, datePublished, abstract)
    VALUES (?, ?, ?, ?)
    ''', (articleTitle, journalTitle, datePublished, abstract))
    conn.commit()
    return cursor.lastrowid

def insert_author(authorName):
    cursor.execute('''
    INSERT INTO Authors (authorName)
    VALUES (?)
    ''', (authorName,))
    conn.commit()
    return cursor.lastrowid

def insert_department(departmentName, location):
    cursor.execute('''
    INSERT INTO Departments (departmentName, location)
    VALUES (?, ?)
    ''', (departmentName, location))
    conn.commit()
    return cursor.lastrowid

def insert_article_author(article_id, author_id, department_id):
    cursor.execute('''
    INSERT INTO ArticleAuthors (article_id, author_id, department_id)
    VALUES (?, ?, ?)
    ''', (article_id, author_id, department_id))
    conn.commit()

if __name__ == "__main__":
    instantiate()