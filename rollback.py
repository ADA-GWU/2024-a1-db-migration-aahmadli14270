# migration_script.py

import pg8000

def migrate_database():
    # Connect to the PostgreSQL database
    conn = pg8000.connect(
        database="postgres",
        user="postgres",
        password="admin",
        host="localhost",
        port="5433"
    )
    cur = conn.cursor()

    try:
        # Rename ST_ID to STUDENT_ID
        if table_exists(cur, "students"):
            # Rename STUDENT_ID back to ST_ID
            cur.execute("ALTER TABLE STUDENTS RENAME COLUMN STUDENT_ID TO ST_ID")

            # Change length of ST_NAME and ST_LAST columns back to VARCHAR(20)
            cur.execute("ALTER TABLE STUDENTS ALTER COLUMN ST_NAME TYPE VARCHAR(20)")
            cur.execute("ALTER TABLE STUDENTS ALTER COLUMN ST_LAST TYPE VARCHAR(20)")

        else:
            print('no')
)


        if table_exists(cur, "interests"):
            cur.execute("ALTER TABLE INTERESTS RENAME COLUMN INTERESTS TO INTEREST")
            cur.execute("ALTER TABLE INTERESTS ALTER COLUMN INTEREST TYPE VARCHAR(50)")

            cur.execute("""
                        CREATE TABLE INTERESTS_FLATTENED (
                            STUDENT_ID INTEGER,
                            INTEREST VARCHAR(100)
                        )
                    """)

            cur.execute("SELECT STUDENT_ID, INTERESTS FROM INTERESTS")
            results = cur.fetchall()

            for student_id, interests_arr in results:
                interests = interests_arr[2:-2].split(",")
                for interest in interests:
                    interest = interest.strip('{}"')
                    if interest:
                        cur.execute("INSERT INTO INTERESTS_FLATTENED (STUDENT_ID, INTEREST) VALUES (%s, %s)",
                                    (student_id, interest))

            cur.execute("DROP TABLE INTERESTS")

            cur.execute("ALTER TABLE INTERESTS_FLATTENED RENAME TO INTERESTS")


        else:
            print('no')



        conn.commit()
        print("RollBack completed successfully.")

    except Exception as e:
        conn.rollback()
        print("Error during rollback:", e)

    finally:
        cur.close()
        conn.close()

def table_exists(cursor, table_name):
    """Check if the specified table exists in the database."""
    cursor.execute(
        "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)",
        (table_name,)
    )
    return cursor.fetchone()[0]

if __name__ == "__main__":
    migrate_database()




