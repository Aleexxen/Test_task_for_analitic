import psycopg2
from config import user, password, db_name, host


try:
    # connect to exist database
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    # the cursor for performing database operations
    with connection.cursor() as cursor:

        # example for first variant of evil student
        cursor.execute(
            """SELECT student_name, student_surname
            FROM Students INNER JOIN Orders ON Orders.student = Students.student_id
            GROUP BY student_name, student_surname
            ORDER BY COUNT(student_name)
            DESC LIMIT 1"""
        )

        # # example for second variant of evil student
        # cursor.execute(
        #     """SELECT student_name, student_surname
        #     FROM Students INNER JOIN Orders
        #     ON Students.student_id = Orders.student
        #     GROUP BY student_name, student_surname ORDER BY SUM(return_date - order_date)
        #     DESC LIMIT 1"""
        # )

        result = cursor.fetchall()
        print(f"Evil reader: {result[0][0]} {result[0][1]}", )
except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL:", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
