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
        FOREIGN KEY (department_id) REFERENCES Departments(department_id)
    )
    ''')

#        PRIMARY KEY (article_id, author_id, department_id)

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

def insert_department(departmentName, latitude, longitude):
    cursor.execute('''
    INSERT INTO Departments (departmentName, latitude, longitude)
    VALUES (?, ?, ?)
    ''', (departmentName, latitude, longitude))
    conn.commit()
    return cursor.lastrowid

def tie_article_author_department(article_id, author_id, department_id):
    cursor.execute('''
    INSERT INTO ArticleAuthors (article_id, author_id, department_id)
    VALUES (?, ?, ?)
    ''', (article_id, author_id, department_id))
    conn.commit()
    return cursor.lastrowid

# Retrieve all articles
def retrieve_all_articles():
    cursor.execute('SELECT * FROM Articles')
    return cursor.fetchall()

# Retrieve article by ID
def retrieve_article_by_id(article_id):
    cursor.execute('SELECT * FROM Articles WHERE article_id = ?', (article_id,))
    return cursor.fetchone()

# Retrieve all authors
def retrieve_all_authors():
    cursor.execute('SELECT * FROM Authors')
    return cursor.fetchall()

# Retrieve author by ID
def retrieve_author_by_id(author_id):
    cursor.execute('SELECT * FROM Authors WHERE author_id = ?', (author_id,))
    return cursor.fetchone()

# Retrieve all departments
def retrieve_all_departments():
    cursor.execute('SELECT * FROM Departments')
    return cursor.fetchall()

# Retrieve department by ID
def retrieve_department_by_id(department_id):
    cursor.execute('SELECT * FROM Departments WHERE department_id = ?', (department_id,))
    return cursor.fetchone()

# Retrieve all articles by a specific author
def retrieve_articles_by_author(author_id):
    cursor.execute('''
    SELECT a.article_id, a.articleTitle, a.journalTitle, a.datePublished, a.abstract
    FROM Articles a
    JOIN ArticleAuthors aa ON a.article_id = aa.article_id
    WHERE aa.author_id = ?
    ''', (author_id,))
    return cursor.fetchall()

# Retrieve all authors of a specific article
def retrieve_authors_by_article(article_id):
    cursor.execute('''
    SELECT au.author_id, au.authorName
    FROM Authors au
    JOIN ArticleAuthors aa ON au.author_id = aa.author_id
    WHERE aa.article_id = ?
    ''', (article_id,))
    return cursor.fetchall()

# Retrieve all departments associated with a specific article
def retrieve_departments_by_article(article_id):
    cursor.execute('''
    SELECT d.department_id, d.departmentName, d.latitude, d.longitude
    FROM Departments d
    JOIN ArticleAuthors aa ON d.department_id = aa.department_id
    WHERE aa.article_id = ?
    ''', (article_id,))
    return cursor.fetchall()

# Retrieve all articles associated with a specific department
def retrieve_articles_by_department(department_id):
    cursor.execute('''
    SELECT a.article_id, a.articleTitle, a.journalTitle, a.datePublished, a.abstract
    FROM Articles a
    JOIN ArticleAuthors aa ON a.article_id = aa.article_id
    WHERE aa.department_id = ?
    ''', (department_id,))
    return cursor.fetchall()

if __name__ == "__main__":
    instantiate()