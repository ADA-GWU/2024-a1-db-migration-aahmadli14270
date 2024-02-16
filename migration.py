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
        # if table_exists(cur, "students"):
        #     # Rename ST_ID to STUDENT_ID
        #     cur.execute("ALTER TABLE STUDENTS RENAME COLUMN ST_ID TO STUDENT_ID")
        #
        #     # Change length of ST_NAME and ST_LAST columns
        #     cur.execute("ALTER TABLE STUDENTS ALTER COLUMN ST_NAME TYPE VARCHAR(30)")
        #     cur.execute("ALTER TABLE STUDENTS ALTER COLUMN ST_LAST TYPE VARCHAR(30)")
        #
        # else:
        #     print('no')

        # if table_exists(cur, "interests"):
        #     # Change name and type of INTEREST column
        #     cur.execute("ALTER TABLE INTERESTS RENAME COLUMN INTEREST TO INTERESTS")
        #     cur.execute("ALTER TABLE INTERESTS ALTER COLUMN INTERESTS TYPE TEXT[] USING array[INTERESTS]")
        # else:
        #     print('no')
        #
        # # Migrate data in INTERESTS table to array format
        # cur.execute("UPDATE INTERESTS SET INTERESTS = ARRAY[INTERESTS]")

        if table_exists(cur, "interests"):
            # Change name and type of INTEREST column
            cur.execute("ALTER TABLE INTERESTS RENAME COLUMN INTEREST TO INTERESTS")
            cur.execute("ALTER TABLE INTERESTS ALTER COLUMN INTERESTS TYPE TEXT[] USING array[INTERESTS]")

            # Aggregate interests for each STUDENT_ID
            cur.execute("""
                SELECT STUDENT_ID, array_agg(interest) AS interests
                FROM (
                    SELECT DISTINCT STUDENT_ID, INTERESTS AS interest
                    FROM INTERESTS
                ) AS subquery
                GROUP BY STUDENT_ID
            """)
            results = cur.fetchall()

            # Update INTERESTS table with aggregated interests
            for student_id, interests in results:
                cur.execute("UPDATE INTERESTS SET INTERESTS = %s WHERE STUDENT_ID = %s", (interests, student_id))
        else:
            print('no')

        # Query to retrieve the contents of INTERESTS table
        #     cur.execute("SELECT * FROM INTERESTS")
        #     interests_data = cur.fetchall()
        #
        #     # Print the contents of INTERESTS table
        #     print("Contents of INTERESTS table:")
        #     for row in interests_data:
        #         print(row)
        # else:
        #     print("INTERESTS table does not exist in the database.")


        # Commit the changes
        conn.commit()
        print("Migration completed successfully.")

    except Exception as e:
        conn.rollback()
        print("Error during migration:", e)

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


