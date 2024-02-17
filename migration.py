# migration_script.py

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
        if table_exists(cur, "students"):
            cur.execute("ALTER TABLE STUDENTS RENAME COLUMN ST_ID TO STUDENT_ID")

            cur.execute("ALTER TABLE STUDENTS ALTER COLUMN ST_NAME TYPE VARCHAR(30)")
            cur.execute("ALTER TABLE STUDENTS ALTER COLUMN ST_LAST TYPE VARCHAR(30)")

        else:
            print('no')

        if table_exists(cur, "interests"):
            cur.execute("ALTER TABLE INTERESTS RENAME COLUMN INTEREST TO INTERESTS")
            cur.execute("ALTER TABLE INTERESTS ALTER COLUMN INTERESTS TYPE TEXT[] USING array[INTERESTS]")

            cur.execute("""
                SELECT
                    STUDENT_ID,
                    ARRAY_AGG(DISTINCT INTERESTS) AS INTERESTS
                FROM
                    INTERESTS
                GROUP BY
                    STUDENT_ID
                ORDER BY
                    STUDENT_ID;
            """)



            results = cur.fetchall()



            print(results)

            for student_id, interests in results:
                flattened_interests = '{{' + ','.join([interest[0] for interest in interests]) + '}}'
                cur.execute("UPDATE INTERESTS SET INTERESTS = %s WHERE STUDENT_ID = %s",
                            (flattened_interests, student_id))

            cur.execute("""
                DELETE FROM INTERESTS
                WHERE ctid NOT IN (
                    SELECT MIN(ctid)
                    FROM INTERESTS
                    GROUP BY STUDENT_ID, INTERESTS
                )
            """)
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


