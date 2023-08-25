# A simple employee database system using Python and MySQL
import pymysql
from time import sleep
from datetime import datetime
import pickle

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

banner = \
    f"""
        {BLUE}
            
        ███████ ███    ███ ██████  ██       ██████  ██    ██ ███████ ███████ 
        ██      ████  ████ ██   ██ ██      ██    ██  ██  ██  ██      ██      
        █████   ██ ████ ██ ██████  ██      ██    ██   ████   █████   █████   
        ██      ██  ██  ██ ██      ██      ██    ██    ██    ██      ██      
        ███████ ██      ██ ██      ███████  ██████     ██    ███████ ███████ 
                                                                             
                                                                             
        ██████   █████  ████████  █████  ██████   █████  ███████ ███████     
        ██   ██ ██   ██    ██    ██   ██ ██   ██ ██   ██ ██      ██          
        ██   ██ ███████    ██    ███████ ██████  ███████ ███████ █████       
        ██   ██ ██   ██    ██    ██   ██ ██   ██ ██   ██      ██ ██          
        ██████  ██   ██    ██    ██   ██ ██████  ██   ██ ███████ ███████     
                                                                             
                                                                             
        ███████ ██    ██ ███████ ████████ ███████ ███    ███                 
        ██       ██  ██  ██         ██    ██      ████  ████                 
        ███████   ████   ███████    ██    █████   ██ ████ ██                 
             ██    ██         ██    ██    ██      ██  ██  ██                 
        ███████    ██    ███████    ██    ███████ ██      ██                 
                                                                             
                                                                             
        {RESET}
    """

menu = \
    f"""
        1. Add a new entry
        2. View an entry
        3. Update an entry
        4. Delete an entry
        5. View all entries
        6. Delete all entries {RED}(WARNING!){RESET}
        7. Export database
        8. Export to CSV
        9. Exit
    """


def take_input():
    user_input = input(f"{GREEN}Enter your choice: \n{RESET}")
    # If the user enters a non-integer value or an integer outside 1 to 7, keep asking for input
    while not user_input.isdigit() or int(user_input) not in range(1, 10):
        print(f"{RED}Invalid input! Please make a correct choice!\n{RESET}")
        print(menu)
        user_input = input(f"{GREEN}Enter your choice: \n{RESET}")
    return int(user_input)


def select_option(option, conn):
    match option:
        case 1:
            add_entry(conn)
        case 2:
            view_entry(conn)
        case 3:
            update_entry(conn)
        case 4:
            delete_entry(conn)
        case 5:
            view_all_entries(conn)
        case 6:
            delete_all_entries(conn)
        case 7:
            export_db(conn)
        case 8:
            export_csv(conn)
        case 9:
            exit_prog()


def add_entry(conn):
    # Add a new entry to the database
    print(f"{GREEN}Enter the following details:{RESET}")
    employee_id = input("Employee ID: ")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    dob = input("Date of birth (YYYY-MM-DD): ")
    gender = input("Gender: ")
    aadhaar_number = input("Aadhaar number: ")
    email = input("Email: ")
    phone = input("Phone: ")
    department = input("Department: ")
    designation = input("Designation: ")
    start_date = input("Start date (YYYY-MM-DD): ")
    end_date = input("End date (YYYY-MM-DD): ")
    employment_status = input("Employment status: ")
    salary = input("Salary: ")

    # Insert the new entry into the database
    try:
        with conn.cursor() as cursor:
            # Add all the values to the database
            add_entry_query = """
                INSERT INTO Employee (
                    EmployeeID,
                    First_name,
                    Last_name,
                    DOB,
                    Gender,
                    Aadhaar_number,
                    Email,
                    Phone,
                    Department,
                    Designation,
                    Start_date,
                    End_date,
                    Employment_status,
                    Salary
                )
                VALUES (
                    %s, %s, %s, STR_TO_DATE(%s, '%%Y-%%m-%%d'), %s, %s, %s, %s, %s, %s, STR_TO_DATE(%s, '%%Y-%%m-%%d'), STR_TO_DATE(%s, '%%Y-%%m-%%d'), %s, %s
                );
            """
            cursor.execute(add_entry_query, (employee_id, first_name, last_name, dob, gender, aadhaar_number, email,
                                             phone, department, designation, start_date, end_date, employment_status,
                                             salary))
            conn.commit()
            print(f"{GREEN}Entry added successfully!{RESET}")
    except pymysql.Error as e:
        print(f"{RED}Error adding entry!{RESET}")
        print(e)



def view_entry(conn):
    # Select the details of an entity based on Employee ID
    try:
        with conn.cursor() as cursor:
            employee_id = input("Enter the Employee ID: ")
            query = """
                    SELECT * FROM Employee WHERE EmployeeID = %s;
                    """
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()
            if result:
                print(f"""
                        {BLUE}Employee ID:{RESET} {result[0]}
                        {BLUE}First Name:{RESET} {result[1]}
                        {BLUE}Last Name:{RESET} {result[2]}
                        {BLUE}DOB:{RESET} {result[3]}
                        {BLUE}Gender:{RESET} {result[4]}
                        {BLUE}Aadhaar:{RESET} {result[5]}
                        {BLUE}Email:{RESET} {result[6]}
                        {BLUE}Phone:{RESET} {result[7]}
                        {BLUE}Department:{RESET}{result[8]}
                        {BLUE}Designation:{RESET} {result[9]}
                        {BLUE}Start Date:{RESET} {result[10]}
                        {BLUE}End Date:{RESET} {result[11]}
                        {BLUE}Employment Status:{RESET} {result[12]}
                        {BLUE}Salary:{RESET} {result[13]}
                    """)
            else:
                print(f"{RED} Employee not found! {RESET}")
    except pymysql.Error as e:
        print(f"{RED}Error adding entry!{RESET}")
        print(e)



def update_entry(conn):
    try:
        with conn.cursor() as cursor:
            employee_id = input("Enter the Employee ID: ")
            first_name = input("Enter the first name: ")
            last_name = input("Enter the last name: ")
            dob = input("Enter the date of birth (YYYY-MM-DD): ")
            gender = input("Enter gender: ")
            aadhaar_number = input("Enter Aadhaar number: ")
            email = input("Enter email: ")
            phone = input("Enter phone number: ")
            department = input("Enter department: ")
            designation = input("Enter designation: ")
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            employment_status = input("Enter employment status: ")
            salary = input("Enter salary: ")

            query = """
                UPDATE Employee SET First_name = %s, Last_name = %s, dob = STR_TO_DATE(%s, '%%Y-%%m-%%d'), gender = %s, aadhaar_number = %s, email = %s, phone = %s, department = %s, designation = %s, start_date = STR_TO_DATE(%s, '%%Y-%%m-%%d'), end_date = STR_TO_DATE(%s, '%%Y-%%m-%%d'), employment_status = %s, salary = %s WHERE EmployeeID = %s;
                """
            cursor.execute(query, (first_name, last_name, dob, gender, aadhaar_number, email, phone, department, designation, start_date, end_date, employment_status, salary, employee_id))
            conn.commit()
            print(f"{GREEN}Entry updated successfully!{RESET}")
    except pymysql.Error as e:
        print(f"{RED}Error updating entry!{RESET}")
        print(e)


def delete_entry(conn):
    try:
        with conn.cursor() as cursor:
            employee_id = input("Enter the Employee ID: ")
            query = """
                DELETE FROM Employee WHERE EmployeeID = %s;
                """
            cursor.execute(query, (employee_id,))
            conn.commit()
            print(f"{GREEN}Entry deleted successfully!{RESET}")
    except pymysql.Error as e:
        print(f"{RED}Error deleting entry!{RESET}")
        print(e)


def view_all_entries(conn):
    try:
        with conn.cursor() as cursor:
            # SE:ECT * FROM Employee;
            query = """
                SELECT * FROM Employee;
                """
            cursor.execute(query)
            result = cursor.fetchall()
            if result:
                print(f"{BLUE}Employee ID\tFirst Name\tLast Name\tDOB\tGender\tAadhaar\tEmail\tPhone\tDepartment\tDesignation\tStart Date\tEnd Date\tEmployment Status\tSalary{RESET}")
                for row in result:
                    print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}\t{row[7]}\t{row[8]}\t{row[9]}\t{row[10]}\t{row[11]}\t{row[12]}\t{row[13]}")
            else:
                print(f"{RED}No entries found!{RESET}")
    except pymysql.Error as e:
        print(f"{RED}Error viewing entries!{RESET}")
        print(e)


def delete_all_entries(conn):
    choice = input(f"{RED}Are you sure you want to delete all entries? (y/n): {RESET}")
    if choice.lower() == 'y':
        try:
            with conn.cursor() as cursor:
                query = """
                    DELETE FROM Employee;
                    """
                cursor.execute(query)
                conn.commit()
                print(f"{GREEN}All entries deleted successfully!{RESET}")
        except pymysql.Error as e:
            print(f"{RED}Error deleting entries!{RESET}")
            print(e)
    else:
        pass


def export_db(conn):
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT * FROM Employee;
                """
            cursor.execute(query)
            result = cursor.fetchall()
            if result:
                with open(f"employee {datetime.now()}.pickle", "wb") as f:
                    pickle.dump(result, f)
                print(f"{GREEN}Database exported successfully!{RESET}")
            else:
                print(f"{RED}No entries found!{RESET}")
    except pymysql.Error as e:
        print(f"{RED}Error exporting database!{RESET}")
        print(e)


def export_csv(conn):
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT * FROM Employee;
                """
            cursor.execute(query)
            result = cursor.fetchall()
            if result:
                with open(f"employee {datetime.now()}.csv", "w") as f:
                    f.write("Employee ID,First Name,Last Name,DOB,Gender,Aadhaar,Email,Phone,Department,Designation,Start Date,End Date,Employment Status,Salary\n")
                    for row in result:
                        f.write(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},{row[7]},{row[8]},{row[9]},{row[10]},{row[11]},{row[12]},{row[13]}\n")
                print(f"{GREEN}Database exported successfully!{RESET}")
            else:
                print(f"{RED}No entries found!{RESET}")
    except pymysql.Error as e:
        print(f"{RED}Error exporting database!{RESET}")
        print(e)


def exit_prog():
    print(f"{GREEN}Thank you for using the program!{RESET}")
    exit()


def check_db():
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'rootpass',
        'charset': 'utf8mb4',
    }
    try:
        init_conn = pymysql.connect(**db_config)
        with init_conn.cursor() as cursor:

            create_db_query = "CREATE DATABASE IF NOT EXISTS employee_db;"
            cursor.execute(create_db_query)
            init_conn.commit()

            init_conn.select_db('employee_db')

            # Create a new table with three numeric columns
            create_table_query = """
                CREATE TABLE IF NOT EXISTS Employee (
                    EmployeeID INT PRIMARY KEY,
                    First_name VARCHAR(50),
                    Last_name VARCHAR(50),
                    DOB DATE,
                    Gender VARCHAR(10),
                    Aadhaar_number INT,
                    Email VARCHAR(100),
                    Phone VARCHAR(10),
                    Department VARCHAR(50),
                    Designation VARCHAR(50),
                    Start_date DATE,
                    End_date DATE,
                    Employment_status VARCHAR(20),
                    Salary DECIMAL(10, 2)
                );
                    """
            cursor.execute(create_table_query)
            init_conn.commit()

    except pymysql.err.OperationalError:
        print(
            f"{RED}Error connecting to database!{RESET}\n\
            Try running the following command and try again:\n\n\
            sudo docker-compose up --build -d")
        exit()


def db_connect():
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'rootpass',
        'db': 'employee_db',
        'charset': 'utf8mb4',
    }
    return pymysql.connect(**db_config)


if __name__ == '__main__':
    check_db()
    conn = db_connect()
    print(banner)
    sleep(1)
    while True:
        print(menu)
        a = take_input()
        select_option(a, conn)
        sleep(1)

