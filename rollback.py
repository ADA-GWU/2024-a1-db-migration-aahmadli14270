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

        # if table_exists(cur, "interests"):
        #     # Change name and type of INTEREST column
        #     cur.execute("ALTER TABLE INTERESTS RENAME COLUMN INTEREST TO INTERESTS")
        #     cur.execute("ALTER TABLE INTERESTS ALTER COLUMN INTERESTS TYPE TEXT[] USING array[INTERESTS]")
        #
        #     # Aggregate interests for each STUDENT_ID
        #     cur.execute("""
        #         SELECT
        #             STUDENT_ID,
        #             ARRAY_AGG(DISTINCT INTERESTS) AS INTERESTS
        #         FROM
        #             INTERESTS
        #         GROUP BY
        #             STUDENT_ID
        #         ORDER BY
        #             STUDENT_ID;
        #     """)
        #
        #
        #
        #     results = cur.fetchall()
        #
        #
        #
        #     print(results)
        #
        #     # Update INTERESTS table with aggregated interests
        #     for student_id, interests in results:
        #         # Flatten the nested arrays and convert to a string representation
        #         flattened_interests = '{{' + ','.join([interest[0] for interest in interests]) + '}}'
        #         cur.execute("UPDATE INTERESTS SET INTERESTS = %s WHERE STUDENT_ID = %s",
        #                     (flattened_interests, student_id))
        #
        #     cur.execute("""
        #         DELETE FROM INTERESTS
        #         WHERE ctid NOT IN (
        #             SELECT MIN(ctid)
        #             FROM INTERESTS
        #             GROUP BY STUDENT_ID, INTERESTS
        #         )
        #     """)
        # else:
        #     print('no')



        # Commit the changes
        conn.commit()
        print("RollBack completed successfully.")

    except Exception as e:
        conn.rollback()
        print("Error during rollback:", e)

    finally:
        # Close the database connection
        cur.close()
        conn.close()

def table_exists(cursor, table_name):
    """Check if the specified table exists in the database."""
    cursor.execute(
        "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)",
        (table_name,)
    )
    return cursor.fetchone()[0]

# Call the migrate_database function to execute the migration
if __name__ == "__main__":
    migrate_database()


