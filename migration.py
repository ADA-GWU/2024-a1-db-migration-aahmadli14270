#v2.py

import pg8000

def migrate_database():
    conn = pg8000.connect(
        database="postgres",
        user="postgres",
        password="admin",
        host="localhost",
        port="5433"
    )
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE NEW_STUDENTS (
                STUDENT_ID INT PRIMARY KEY,
                ST_NAME VARCHAR(30),
                ST_LAST VARCHAR(30)
            )
        """)

        cur.execute("""
            INSERT INTO NEW_STUDENTS (STUDENT_ID, ST_NAME, ST_LAST)
            SELECT ST_ID, ST_NAME, ST_LAST FROM STUDENTS
        """)

        cur.execute("DROP TABLE STUDENTS")

        cur.execute("ALTER TABLE NEW_STUDENTS RENAME TO STUDENTS")


        #############

        if table_exists(cur, "interests"):
            cur.execute("""
                        CREATE TABLE NEW_INTERESTS (
                            STUDENT_ID INT,
                            INTERESTS TEXT[]
                        )
                    """)

            cur.execute("""
                        INSERT INTO NEW_INTERESTS (STUDENT_ID, INTERESTS)
                        SELECT STUDENT_ID, ARRAY_AGG(DISTINCT INTEREST) FROM INTERESTS GROUP BY STUDENT_ID
                    """)

            cur.execute("DROP TABLE INTERESTS")

            cur.execute("ALTER TABLE NEW_INTERESTS RENAME TO INTERESTS")
        else:
            print('no')



        conn.commit()
        print("Migration completed successfully.")

    except Exception as e:
        conn.rollback()
        print("Error during migration:", e)

    finally:
        cur.close()
        conn.close()

def table_exists(cursor, table_name):
    cursor.execute(
        "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)",
        (table_name,)
    )
    return cursor.fetchone()[0]

if __name__ == "__main__":
    migrate_database()


