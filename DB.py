import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import Toplevel, Frame, Label, Entry, Button
import mysql.connector
from datetime import datetime
import re
import random

# Establish database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hamed356",
    database="bank"
)
cursor = conn.cursor()
def is_valid(identity):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='hamed356',
            database='bank'
        )
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM CustomerTable WHERE Account_Number = %s"
        cursor.execute(query, (identity,))
        result = cursor.fetchone()[0]
        conn.close()
        return result == 0  # Returns True if identity doesn't exist, False if it exists
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False


def search_table(search_term, start_date=None, end_date=None):
    for item in tree.get_children():
        tree.delete(item)

    filtered_data = data
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            filtered_data = [row for row in data if start_date <= row[2] <= end_date]
        except ValueError:
            pass  # Handle invalid date format

    for row in filtered_data:
        if any(search_term.lower() in str(cell).lower() for cell in row):
            tree.insert('', 'end', values=row)

# Database connection function
def fetch_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='hamed356',  # Replace with your MySQL password
            database='bank'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BalanceChangeLog")
        rows = cursor.fetchall()
        # Convert date strings to datetime objects
        for i in range(len(rows)):
            row = list(rows[i])
            row[2] = datetime.strptime(row[2], "%Y-%m-%d").date()  # Assuming Change Date is at index 2
            rows[i] = tuple(row)
        return rows
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def is_valid(customer_account_number):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='hamed356',  # Update with your MySQL root password
            database='bank'
        )
        cursor = conn.cursor()

        query = "SELECT * FROM CustomerTable WHERE Account_Number = %s"
        cursor.execute(query, (customer_account_number,))
        row = cursor.fetchone()

        if row is not None:
            return False  # Account number already exists
        else:
            return True  # Account number is valid
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False  # Assume invalid if there's an error
    finally:
        cursor.close()
        conn.close()


def check_leap(year):
    return ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0)


def check_date(date):
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Check if date is empty or not in the correct format
    if not date or len(date.split("/")) != 3:
        return False

    try:
        day, month, year = map(int, date.split("/"))
    except ValueError:
        return False  # If conversion fails, return False

    # Check if year, month, and day are in valid ranges
    current_year = 2024  # Replace with current year if needed
    if not (0 <= year <= current_year) or not (1 <= month <= 12):
        return False

    # Adjust for leap year
    if check_leap(year):
        days_in_months[1] = 29

    return 1 <= day <= days_in_months[month - 1]
def display_account_summary(identity, choice):
    output_message = ""
    try:
        cursor.execute('''SELECT Account_Number, Card_Number, Account_Type, Name, Gender, DOB, Address, Balance, Date_Of_Creation FROM CustomerTable WHERE Account_Number = %s''', (identity,))
        row = cursor.fetchone()
        if row is not None:
            if choice == 1:
                output_message += "Account Number: " + row[0] + "\n"
                output_message += "Card Number: " + str(row[1]) + "\n"
                output_message += "Account Type: " + row[2] + "\n"
                output_message += "Name: " + row[3] + "\n"
                output_message += "Gender: " + row[4] + "\n"
                output_message += "Date of Birth: " + str(row[5]) + "\n"
                output_message += "Address: " + row[6] + "\n"
                output_message += "Balance: " + str(row[7]) + "\n"
                output_message += "Date of Account Creation: " + str(row[8]) + "\n"
            else:
                output_message += "Current Balance: " + str(row[7]) + "\n"
        else:
            output_message = "# No account associated with the entered account number exists! #"
    except mysql.connector.Error as err:
        output_message = f"Error: {err}"
    return output_message

class welcomeScreen:
    def __init__(self, window=None):
        self.master = window
        window.geometry("600x450+383+106")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Welcome to BANK")
        p1 = PhotoImage(file='./images/bank1.png')
        window.iconphoto(True, p1)
        window.configure(background="#023047")
        window.configure(cursor="arrow")

        self.Canvas1 = tk.Canvas(window, background="#E6E6FA", borderwidth="0", insertbackground="black",
                                 relief="ridge", selectbackground="blue", selectforeground="white")
        self.Canvas1.place(relx=0.190, rely=0.228, relheight=0.496, relwidth=0.622)

        self.Button1 = tk.Button(self.Canvas1, command=self.selectEmployee, activebackground="#ececec",
                                 activeforeground="#000000", background="#023047", disabledforeground="#a3a3a3",
                                 foreground="#fbfbfb", borderwidth="0", highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''EMPLOYEE''')
        self.Button1.configure(font="-family {Segoe UI} -size 10 -weight bold")
        self.Button1.place(relx=0.325, rely=0.200, height=30, width=100)

        self.Button2 = tk.Button(self.Canvas1, command=self.selectCustomer, activebackground="#ececec",
                                 activeforeground="#000000", background="#023047", disabledforeground="#a3a3a3",
                                 foreground="#fbfbfb", borderwidth="0", highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''CUSTOMER''')
        self.Button2.configure(font="-family {Segoe UI} -size 10 -weight bold")
        self.Button2.place(relx=0.325, rely=0.400, height=30, width=100)

        self.Button3 = tk.Button(self.Canvas1, command=self.selectATM, activebackground="#ececec",
                                 activeforeground="#000000", background="#023047", disabledforeground="#a3a3a3",
                                 foreground="#fbfbfb", borderwidth="0", highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''ATM''')
        self.Button3.configure(font="-family {Segoe UI} -size 10 -weight bold")
        self.Button3.place(relx=0.325, rely=0.600, height=30, width=100)

        self.Label1 = tk.Label(self.Canvas1, background="#E6E6FA", disabledforeground="#a3a3a3",
                               font="-family {Segoe UI} -size 13 -weight bold", foreground="#000000",
                               text='''Please select your operation''')
        self.Label1.place(relx=0.150, rely=0.050, height=31, width=250)

    def selectEmployee(self):
        self.master.withdraw()
        adminLogin(Toplevel(self.master))

    def selectCustomer(self):
        self.master.withdraw()
        CustomerLogin(Toplevel(self.master))

    def selectATM(self):
        self.master.withdraw()
        ATMLogin(Toplevel(self.master))
class ATMLogin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+338+92")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("ATM")
        window.configure(background="#00254a")

        global Canvas1
        Canvas1 = tk.Canvas(window, background="#ffffff", insertbackground="black", relief="ridge",
                            selectbackground="blue", selectforeground="white")
        Canvas1.place(relx=0.108, rely=0.142, relheight=0.715, relwidth=0.798)

        Label1 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3",
                          font="-family {Segoe UI} -size 14 -weight bold", foreground="#00254a",
                          text="ATM Login")
        Label1.place(relx=0.135, rely=0.05, height=41, width=154)

        global Label2
        Label2 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        Label2.place(relx=0.067, rely=0.200, height=300, width=233)
        global _img0
        _img0 = tk.PhotoImage(file="./images/ATM .png")
        Label2.configure(image=_img0)

        self.Entry1 = tk.Entry(Canvas1, background="#e2e2e2", borderwidth="2", disabledforeground="#a3a3a3",
                               font="TkFixedFont", foreground="#000000", highlightbackground="#b6b6b6",
                               highlightcolor="#004080", insertbackground="black")
        self.Entry1.place(relx=0.607, rely=0.453, height=20, relwidth=0.26)

        self.Entry1_1 = tk.Entry(Canvas1, show='*', background="#e2e2e2", borderwidth="2",
                                 disabledforeground="#a3a3a3", font="TkFixedFont", foreground="#000000",
                                 highlightbackground="#d9d9d9", highlightcolor="#004080", insertbackground="black",
                                 selectbackground="blue", selectforeground="white")
        self.Entry1_1.place(relx=0.607, rely=0.623, height=20, relwidth=0.26)

        self.Label3 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label3.place(relx=0.556, rely=0.453, height=21, width=34)

        global _img1
        _img1 = tk.PhotoImage(file="./images/card1.png")
        self.Label3.configure(image=_img1)

        self.Label4 = tk.Label(Canvas1)
        self.Label4.place(relx=0.556, rely=0.623, height=21, width=34)
        global _img2
        _img2 = tk.PhotoImage(file="./images/lock1.png")
        self.Label4.configure(image=_img2, background="#ffffff")

        self.Label5 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label5.place(relx=0.670, rely=0.142, height=71, width=74)
        global _img3
        _img3 = tk.PhotoImage(file="./images/bank1.png")
        self.Label5.configure(image=_img3)

        self.Button = tk.Button(Canvas1, text="Login", borderwidth="0", width=10, background="#00254a",
                                foreground="#ffffff",
                                font="-family {Segoe UI} -size 10 -weight bold",
                                command=lambda: self.login(self.Entry1.get(), self.Entry1_1.get()))
        self.Button.place(relx=0.765, rely=0.755)

        self.Button_back = tk.Button(Canvas1, text="Back", borderwidth="0", width=10, background="#00254a",
                                     foreground="#ffffff",
                                     font="-family {Segoe UI} -size 10 -weight bold",
                                     command=self.back)
        self.Button_back.place(relx=0.545, rely=0.755)

        global ATM_img
        ATM_img = tk.PhotoImage(file="./images/ATM.png")

    def back(self):
        self.master.withdraw()
        welcomeScreen(Toplevel(self.master))

    @staticmethod
    def setImg():
        settingIMG = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        settingIMG.place(relx=0.067, rely=0.283, height=181, width=233)
        settingIMG.configure(image=customer_img)

    def login(self, card_number, customer_PIN):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hamed356",
                database="bank"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                check_query = ("SELECT COUNT(*) FROM CustomerTable WHERE Card_Number = %s AND PIN = %s")
                cursor.execute(check_query, (card_number, customer_PIN))
                result = cursor.fetchone()

                if result[0] > 0:
                    global customer_cardNO
                    customer_cardNO = str(card_number)
                    self.master.withdraw()
                    atmmenu(Toplevel(self.master))
                    print(f"User with card number {card_number} logged in.")
                else:
                    print("Invalid credentials")

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()

class atmmenu:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("ATM")
        window.configure(background="#00254a")

        self.Labelframe1 = tk.LabelFrame(window, relief='groove', font="-family {Segoe UI} -size 13 -weight bold",
                                         foreground="#000000", text='''Select your option''', background="#fffffe")
        self.Labelframe1.place(relx=0.081, rely=0.081, relheight=0.415, relwidth=0.848)

        self.Button1 = tk.Button(self.Labelframe1, command=self.selectWithdraw, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Withdraw''')
        self.Button1.place(relx=0.667, rely=0.195, height=34, width=181, bordermode='ignore')

        self.Button2 = tk.Button(self.Labelframe1, command=self.selectDeposit, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Deposit''')
        self.Button2.place(relx=0.04, rely=0.195, height=34, width=181, bordermode='ignore')

        self.Button6 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#39a9fc", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text='''Check your balance''', command=self.checkBalance)
        self.Button6.place(relx=0.04, rely=0.683, height=34, width=181, bordermode='ignore')

        self.Button3 = tk.Button(self.Labelframe1, command=self.exit, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Exit''')
        self.Button3.place(relx=0.667, rely=0.683, height=34, width=181, bordermode='ignore')

        global Frame1_1_2
        Frame1_1_2 = tk.Frame(window, relief='groove', borderwidth="2", background="#fffffe")
        Frame1_1_2.place(relx=0.081, rely=0.547, relheight=0.415, relwidth=0.848)

    def selectDeposit(self):
        depositMoney(Toplevel(self.master))

    def selectWithdraw(self):
        withdrawMoney(Toplevel(self.master))
    def checkBalance(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hamed356",
                database="bank"
            )
            cursor = conn.cursor()
            query = """
            SELECT Balance FROM CustomerTable  WHERE Account_Number = %s """
            cursor.execute(query, (customer_cardNO,))
            row = cursor.fetchone()

            if row:
                output = (

                    f"Current balance : {row[0]}\n"

                )
            else:
                output = "Account not found."

            self.printMessage(output)
            print("Check balance function called.")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.printMessage(f"Error: {err}")
        self.printMessage(output)
        print("check balance function called.")
    def exit(self):
        self.master.withdraw()
        ATMLogin(Toplevel(self.master))




class Error:
    def __init__(self, window=None):
        global master
        self.window = window
        master = window
        window.geometry("411x117+485+248")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Error")
        window.configure(background="#f2f3f4")

        self.Button1 = tk.Button(window, background="#d3d8dc", borderwidth="1", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 9", foreground="#000000",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''OK''', command=self.goback)
        self.Button1.place(relx=0.779, rely=0.598, height=24, width=67)

        global _img0
        _img0 = PhotoImage(file="./images/error_image.png")
        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               image=_img0, text='''Label''')
        self.Label1.place(relx=0.024, rely=0.0, height=60, width=60)

    def setMessage(self, message_shown):
        Label2 = tk.Label(master, background="#f2f3f4", disabledforeground="#a3a3a3",
                          font="-family {Segoe UI} -size 16", foreground="#000000", highlightcolor="#646464646464",
                          text=message_shown)
        Label2.place(relx=0.210, rely=0.171, height=41, width=175)

    def goback(self):
        master.withdraw()


class adminLogin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+338+92")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Admin")
        window.configure(background="#336699")

        global Canvas1
        Canvas1 = tk.Canvas(window, background="#ffffff", insertbackground="black", relief="ridge",
                            selectbackground="blue", selectforeground="white")
        Canvas1.place(relx=0.108, rely=0.142, relheight=0.715, relwidth=0.798)

        self.Label1 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3",
                               font="-family {Segoe UI} -size 14 -weight bold", foreground="#00254a",
                               text="Employee Login")
        self.Label1.place(relx=0.135, rely=0.142, height=41, width=154)

        global Label2
        Label2 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        Label2.place(relx=0.067, rely=0.283, height=181, width=233)
        global _img0
        _img0 = PhotoImage(file="./images/adminLogin1.png")
        Label2.configure(image=_img0)

        self.Entry1 = tk.Entry(Canvas1, background="#e2e2e2", borderwidth="2", disabledforeground="#a3a3a3",
                               font="TkFixedFont", foreground="#000000", highlightbackground="#b6b6b6",
                               highlightcolor="#004080", insertbackground="black")
        self.Entry1.place(relx=0.607, rely=0.453, height=20, relwidth=0.26)

        self.Entry1_1 = tk.Entry(Canvas1, show='*', background="#e2e2e2", borderwidth="2",
                                 disabledforeground="#a3a3a3", font="TkFixedFont", foreground="#000000",
                                 highlightbackground="#d9d9d9", highlightcolor="#004080", insertbackground="black",
                                 selectbackground="blue", selectforeground="white")
        self.Entry1_1.place(relx=0.607, rely=0.623, height=20, relwidth=0.26)

        self.Label3 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label3.place(relx=0.556, rely=0.453, height=21, width=34)
        global _img1
        _img1 = PhotoImage(file="./images/user1.png")
        self.Label3.configure(image=_img1)

        self.Label4 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label4.place(relx=0.556, rely=0.623, height=21, width=34)
        global _img2
        _img2 = PhotoImage(file="./images/lock1.png")
        self.Label4.configure(image=_img2)

        self.Label5 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label5.place(relx=0.670, rely=0.142, height=71, width=74)
        global _img3
        _img3 = PhotoImage(file="./images/bank1.png")
        self.Label5.configure(image=_img3)

        self.Button = tk.Button(Canvas1, text="Login", borderwidth="0", width=10, background="#336699",
                                foreground="#00254a",
                                font="-family {Segoe UI} -size 10 -weight bold",
                                command=lambda: self.login(self.Entry1.get(), self.Entry1_1.get()))
        self.Button.place(relx=0.765, rely=0.755)

        self.Button_back = tk.Button(Canvas1, text="Back", borderwidth="0", width=10, background="#336699",
                                     foreground="#00254a",
                                     font="-family {Segoe UI} -size 10 -weight bold",
                                     command=self.back)
        self.Button_back.place(relx=0.545, rely=0.755)

        global admin_img
        admin_img = tk.PhotoImage(file="./images/adminLogin1.png")

        @staticmethod
        def setImg():
            settingIMG = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
            settingIMG.place(relx=0.067, rely=0.283, height=181, width=233)
            settingIMG.configure(image=admin_img)

    def back(self):
        self.master.withdraw()
        welcomeScreen(Toplevel(self.master))



    def login(self, admin_name, admin_password):
        global admin_nameNO
        admin_nameNO = admin_name

        # Connect to the database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hamed356",
                database="bank"
            )
            cursor = conn.cursor()

            # Check credentials
            query ='''SELECT * FROM employeeTable WHERE Name = %s AND password = %s'''
            cursor.execute(query, (admin_name, admin_password))
            result = cursor.fetchone()

            if result:
                self.master.withdraw()
                adminMenu(Toplevel(self.master))
                print("Admin login successful.")
            else:
                Error(Toplevel(self.master))
                Error.setMessage(self, message_shown="Invalid Credentials!")
                self.setImg()
                print("Admin login failed.")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown=f"Database error: {err}")
            self.setImg()
            print(f"Database error: {err}")
class CustomerLogin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+338+92")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Customer")
        window.configure(background="#00254a")

        global Canvas1
        Canvas1 = tk.Canvas(window, background="#ffffff", insertbackground="black", relief="ridge",
                            selectbackground="blue", selectforeground="white")
        Canvas1.place(relx=0.108, rely=0.142, relheight=0.715, relwidth=0.798)

        Label1 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3",
                          font="-family {Segoe UI} -size 14 -weight bold", foreground="#00254a",
                          text="Customer Login")
        Label1.place(relx=0.135, rely=0.142, height=41, width=154)

        global Label2
        Label2 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        Label2.place(relx=0.067, rely=0.283, height=220, width=220)
        global _img0
        _img0 = tk.PhotoImage(file="./images/customer.png")
        Label2.configure(image=_img0)

        self.Entry1 = tk.Entry(Canvas1, background="#e2e2e2", borderwidth="2", disabledforeground="#a3a3a3",
                               font="TkFixedFont", foreground="#000000", highlightbackground="#b6b6b6",
                               highlightcolor="#004080", insertbackground="black")
        self.Entry1.place(relx=0.607, rely=0.453, height=20, relwidth=0.26)

        self.Entry1_1 = tk.Entry(Canvas1, show='*', background="#e2e2e2", borderwidth="2",
                                 disabledforeground="#a3a3a3", font="TkFixedFont", foreground="#000000",
                                 highlightbackground="#d9d9d9", highlightcolor="#004080", insertbackground="black",
                                 selectbackground="blue", selectforeground="white")
        self.Entry1_1.place(relx=0.607, rely=0.623, height=20, relwidth=0.26)

        self.Label3 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label3.place(relx=0.556, rely=0.453, height=21, width=34)

        global _img1
        _img1 = tk.PhotoImage(file="./images/user1.png")
        self.Label3.configure(image=_img1)

        self.Label4 = tk.Label(Canvas1)
        self.Label4.place(relx=0.556, rely=0.623, height=21, width=34)
        global _img2
        _img2 = tk.PhotoImage(file="./images/lock1.png")
        self.Label4.configure(image=_img2, background="#ffffff")

        self.Label5 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label5.place(relx=0.670, rely=0.142, height=71, width=74)
        global _img3
        _img3 = tk.PhotoImage(file="./images/bank1.png")
        self.Label5.configure(image=_img3)

        self.Button = tk.Button(Canvas1, text="Login", borderwidth="0", width=10, background="#00254a",
                                foreground="#ffffff",
                                font="-family {Segoe UI} -size 10 -weight bold",
                                command=lambda: self.login(self.Entry1.get(), self.Entry1_1.get()))
        self.Button.place(relx=0.765, rely=0.755)

        self.Button_back = tk.Button(Canvas1, text="Back", borderwidth="0", width=10, background="#00254a",
                                     foreground="#ffffff",
                                     font="-family {Segoe UI} -size 10 -weight bold",
                                     command=self.back)
        self.Button_back.place(relx=0.545, rely=0.755)

        global customer_img
        customer_img = tk.PhotoImage(file="./images/customer.png")

    def back(self):
        self.master.withdraw()
        welcomeScreen(Toplevel(self.master))

    @staticmethod
    def setImg():
        settingIMG = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        settingIMG.place(relx=0.067, rely=0.283, height=181, width=233)
        settingIMG.configure(image=customer_img)

    def login(self, customer_account_number, customer_PIN):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hamed356",
                database="bank"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                check_query = ("SELECT COUNT(*) FROM CustomerTable WHERE Account_Number = %s AND pin = %s")
                cursor.execute(check_query, (customer_account_number, customer_PIN))
                result = cursor.fetchone()

                if result[0] > 0:
                    update_query = ("UPDATE CustomerTable SET logged_in = 1 WHERE Account_Number = %s")
                    cursor.execute(update_query, (customer_account_number,))
                    connection.commit()
                    global customer_accNO
                    customer_accNO = str(customer_account_number)
                    self.master.withdraw()
                    customerMenu(Toplevel(self.master))
                    print(f"User with account number {customer_account_number} logged in.")
                else:
                    print("Invalid credentials")

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()


class adminMenu:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Admin Section")
        window.configure(background="#336699")

        self.Labelframe1 = tk.LabelFrame(window, relief='groove', font="-family {Segoe UI} -size 13 -weight bold",
                                         foreground="#001c37", text="Select your option", background="#fffffe")
        self.Labelframe1.place(relx=0.081, rely=0.081, relheight=0.415, relwidth=0.848)

        self.Button1 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#00254a", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text="Close bank account", command=self.closeAccount)
        self.Button1.place(relx=0.667, rely=0.195, height=34, width=181, bordermode='ignore')

        self.Button2 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#00254a", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text="Create bank account", command=self.createCustaccount)
        self.Button2.place(relx=0.04, rely=0.195, height=34, width=181, bordermode='ignore')

        self.Button3 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#00254a", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text="Exit",
                                 command=self.exit)
        self.Button3.place(relx=0.667, rely=0.683, height=34, width=181, bordermode='ignore')

        self.Button4 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#00254a", foreground="#fffffe", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text="Check account summary", command=self.showAccountSummary)
        self.Button4.place(relx=0.04, rely=0.683, height=34, width=181, bordermode='ignore')

        self.Button5 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#00254a", foreground="#fffffe", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text="Show Transaction Log", command=self.showlog)
        self.Button5.place(relx=0.350, rely=0.450, height=34, width=181, bordermode='ignore')

        global Frame1
        Frame1 = tk.Frame(window, relief='groove', borderwidth="2", background="#fffffe")
        Frame1.place(relx=0.081, rely=0.547, relheight=0.415, relwidth=0.848)

    def showlog(self):
        log_window = Toplevel(self.master)
        log_window.title("Transaction Log")
        log_window.geometry("800x600")

        global tree
        global data

        # Fetch data from database
        data = fetch_data()

        # Creating a frame for the search bar and the treeview
        frame = Frame(log_window)
        frame.pack(pady=20)

        # Adding a search bar
        search_label = Label(frame, text="Search:")
        search_label.pack(side=tk.LEFT, padx=5)

        search_entry = Entry(frame)
        search_entry.pack(side=tk.LEFT, padx=5)

        search_label_from = Label(frame, text="From Date (YYYY-MM-DD):")
        search_label_from.pack(side=tk.LEFT, padx=5)

        search_entry_from = Entry(frame)
        search_entry_from.pack(side=tk.LEFT, padx=5)

        search_label_to = Label(frame, text="To Date (YYYY-MM-DD):")
        search_label_to.pack(side=tk.LEFT, padx=5)

        search_entry_to = Entry(frame)
        search_entry_to.pack(side=tk.LEFT, padx=5)

        search_button = Button(frame, text="Search", command=lambda: search_table(
            search_entry.get(),
            search_entry_from.get() if search_entry_from.get() else None,
            search_entry_to.get() if search_entry_to.get() else None
        ))
        search_button.pack(side=tk.LEFT, padx=5)

        # Creating the Treeview to display the table
        columns = ("LogID", "Account Number", "Change Date", "Old Balance", "New Balance", "Transaction Type")
        tree = ttk.Treeview(log_window, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        tree.pack(fill=tk.BOTH, expand=True)

        # Populating the Treeview with initial data
        search_table("")  # Show all data initially
    def closeAccount(self):
        CloseAccountByAdmin(Toplevel(self.master))

    def createCustaccount(self):
        createCustomerAccount(Toplevel(self.master))

    def showAccountSummary(self):
        checkAccountSummary(Toplevel(self.master))

    def printAccountSummary(self, identity):
        # clearing the frame
        for widget in Frame1.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output = display_account_summary(identity, 1)
        output_message = tk.Label(Frame1, text=output, background="#fffffe")
        output_message.pack(pady=20)

    def printMessage_outside(self, output):
        # clearing the frame
        for widget in Frame1.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output_message = tk.Label(Frame1, text=output, background="#fffffe")
        output_message.pack(pady=40)

    def exit(self):
        self.master.withdraw()
        adminLogin(Toplevel(self.master))
def search_table(search_term):
    for item in tree.get_children():
        tree.delete(item)
    for row in data:
        if any(search_term.lower() in str(cell).lower() for cell in row):
            tree.insert('', 'end', values=row)
def fetch_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='hamed356',
            database='bank'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BalanceChangeLog")
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

class CloseAccountByAdmin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+498+261")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Close customer account")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3",
                               text='''Enter account number:''')
        self.Label1.place(relx=0.232, rely=0.220, height=20, width=120)

        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.536, rely=0.220, height=20, relwidth=0.232)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", borderwidth="0",
                                 background="#004080", disabledforeground="#a3a3a3", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text="Back",
                                 command=self.back)
        self.Button1.place(relx=0.230, rely=0.598, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 borderwidth="0", disabledforeground="#a3a3a3", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text="Proceed",
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button2.place(relx=0.598, rely=0.598, height=24, width=67)

    def back(self):
        self.master.withdraw()

    def submit(self, identity):
        if not identity or not identity.isnumeric():
            self.show_error("Invalid account number!")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='hamed356',
                database='bank'
            )
            cursor = conn.cursor()

            # Check if account exists
            query = "SELECT * FROM CustomerTable WHERE Account_Number = %s"
            cursor.execute(query, (identity,))
            account = cursor.fetchone()

            if account is None:
                self.show_error("Account doesn't exist!")
                return

            # If the account exists, delete it
            self.delete_customer_account(identity)

        except mysql.connector.Error as err:
            self.show_error(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        self.master.withdraw()

    def delete_customer_account(self, identity):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='hamed356',
                database='bank'
            )
            cursor = conn.cursor()

            delete_query = "DELETE FROM CustomerTable WHERE Account_Number = %s"
            cursor.execute(delete_query, (identity,))
            conn.commit()

            self.show_message("Account deleted successfully!")

        except mysql.connector.Error as err:
            self.show_error(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_message(self, message):
        self.showinfo("Success", message)

    def show_error(self, message):
        self.showerror("Error", message)
    def show_error(self, message):
        error_window = Toplevel(self.master)
        Error(error_window)
        Error.setMessage(self, message_shown=message)


class createCustomerAccount:
    def __init__(self, window):
        self.master = window
        self.master.geometry("800x600")
        self.master.configure(background="#f2f3f4")
        self.master.title("Create Customer Account")

        self.acc_type = tk.StringVar()
        self.gender = tk.StringVar()

        self.Label1 = tk.Label(window, background="#f2f3f4", foreground="#000000", text='''Account Number:''')
        self.Label1.place(relx=0.292, rely=0.18, height=24, width=122)

        self.Entry1 = tk.Entry(window, background="#cae4ff", foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.511, rely=0.18, height=20, relwidth=0.302)
        self.Entry1.configure(validate="key", validatecommand=(window.register(self.validate_numbers), "%P"))

        self.Label2 = tk.Label(window, background="#f2f3f4", foreground="#000000", text='''Name:''')
        self.Label2.place(relx=0.292, rely=0.24, height=24, width=122)

        self.Entry2 = tk.Entry(window, background="#cae4ff", foreground="#000000", insertbackground="black")
        self.Entry2.place(relx=0.511, rely=0.24, height=20, relwidth=0.302)
        self.Entry2.configure(validate="key", validatecommand=(window.register(self.validate_letters), "%P"))

        self.Label3 = tk.Label(window, background="#f2f3f4", foreground="#000000", text='''Account Type:''')
        self.Label3.place(relx=0.292, rely=0.3, height=24, width=122)

        self.OptionMenu1 = tk.OptionMenu(window, self.acc_type, "Savings", "Checking")
        self.OptionMenu1.place(relx=0.511, rely=0.3, height=20, relwidth=0.302)

        self.Label4 = tk.Label(window, background="#f2f3f4", foreground="#000000",
                               text='''Date of Birth (DD/MM/YYYY):''')
        self.Label4.place(relx=0.292, rely=0.36, height=24, width=130)

        self.Entry4 = tk.Entry(window, background="#cae4ff", foreground="#000000", insertbackground="black")
        self.Entry4.place(relx=0.511, rely=0.36, height=20, relwidth=0.302)
        self.Entry4.configure(validate="key", validatecommand=(window.register(self.validate_date), "%P"))

        self.Label5 = tk.Label(window, background="#f2f3f4", foreground="#000000", text='''Card Number:''')
        self.Label5.place(relx=0.292, rely=0.42, height=24, width=122)

        self.Entry5 = tk.Entry(window, background="#cae4ff", foreground="#000000", insertbackground="black")
        self.Entry5.place(relx=0.511, rely=0.42, height=20, relwidth=0.302)
        self.Entry5.configure(validate="key", validatecommand=(window.register(self.validate_numbers), "%P"))

        self.Label6 = tk.Label(window, background="#f2f3f4", foreground="#000000", text='''Gender:''')
        self.Label6.place(relx=0.292, rely=0.48, height=24, width=122)

        self.OptionMenu2 = tk.OptionMenu(window, self.gender, "Male", "Female")
        self.OptionMenu2.place(relx=0.511, rely=0.48, height=20, relwidth=0.302)

        self.Label7 = tk.Label(window, background="#f2f3f4", foreground="#000000", text='''Address:''')
        self.Label7.place(relx=0.292, rely=0.546, height=24, width=122)

        self.Entry7 = tk.Entry(window, background="#cae4ff", foreground="#000000", insertbackground="black")
        self.Entry7.place(relx=0.511, rely=0.546, height=20, relwidth=0.302)

        self.Label8 = tk.Label(window, background="#f2f3f4", foreground="#000000", text='''PIN:''')
        self.Label8.place(relx=0.292, rely=0.62, height=24, width=122)

        self.Entry8 = tk.Entry(window, background="#cae4ff", foreground="#000000", insertbackground="black", show="*")
        self.Entry8.place(relx=0.511, rely=0.62, height=20, relwidth=0.302)
        self.Entry8.configure(validate="key", validatecommand=(window.register(self.validate_numbers), "%P"))

        self.Label9 = tk.Label(window, background="#f2f3f4", foreground="#000000", text='''Re-enter PIN:''')
        self.Label9.place(relx=0.292, rely=0.695, height=24, width=122)

        self.Entry9 = tk.Entry(window, background="#cae4ff", foreground="#000000", insertbackground="black", show="*")
        self.Entry9.place(relx=0.511, rely=0.695, height=20, relwidth=0.302)
        self.Entry9.configure(validate="key", validatecommand=(window.register(self.validate_numbers), "%P"))

        self.Label10 = tk.Label(window, background="#f2f3f4", foreground="#000000", text='''Initial Balance:''')
        self.Label10.place(relx=0.292, rely=0.779, height=24, width=122)

        self.Entry10 = tk.Entry(window, background="#cae4ff", foreground="#000000", insertbackground="black")
        self.Entry10.place(relx=0.511, rely=0.779, height=20, relwidth=0.302)
        self.Entry10.configure(validate="key", validatecommand=(window.register(self.validate_numbers), "%P"))

        self.Button1 = tk.Button(window, background="#004080", foreground="#ffffff", text='''Back''', command=self.back)
        self.Button1.place(relx=0.243, rely=0.893, height=24, width=67)

        self.Button2 = tk.Button(window, background="#004080", foreground="#ffffff", text='''Proceed''',
                                 command=self.generate_account_details)
        self.Button2.place(relx=0.633, rely=0.893, height=24, width=67)

        self.Button3 = tk.Button(window, background="#004080", foreground="#ffffff", text='''Generate Random Number''',
                                 command=self.generate_random_numbers)
        self.Button3.place(relx=0.511, rely=0.10, height=24, width=180)

    def back(self):
        self.master.withdraw()

    def generate_account_details(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='hamed356',
                database='bank'
            )
            cursor = conn.cursor()

            cursor.execute("SELECT Account_Number FROM CustomerTable ORDER BY Account_Number DESC LIMIT 1")
            last_account_number = cursor.fetchone()
            if last_account_number:
                next_account_number = str(int(last_account_number[0]) + 1).zfill(5)
            else:
                next_account_number = '00001'

            card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])

            self.Entry1.delete(0, tk.END)
            self.Entry1.insert(0, next_account_number)
            self.Entry5.delete(0, tk.END)
            self.Entry5.insert(0, card_number)

            # Convert DOB to 'YYYY-MM-DD' format
            dob = datetime.strptime(self.Entry4.get(), '%d/%m/%Y').strftime('%Y-%m-%d')

            self.create_acc(next_account_number, self.Entry2.get(), self.acc_type.get(),
                            dob, card_number, self.gender.get(), self.Entry7.get(), self.Entry8.get(),
                            self.Entry9.get(), self.Entry10.get())

            conn.close()

        except Exception as e:
            self.show_error(f"Error: {e}")

    def create_acc(self, account_number, name, acc_type, dob, card_number, gender, address, pin, re_pin, balance):
        if pin != re_pin:
            self.show_error("PINs do not match!")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='hamed356',
                database='bank'
            )
            cursor = conn.cursor()

            insert_query = """
            INSERT INTO CustomerTable (Account_Number, Card_Number, Account_Type, PIN, Name, Gender, DOB, Address, Balance, Date_Of_Creation) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            current_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(insert_query, (
                account_number, card_number, acc_type, pin, name, gender, dob, address, balance, current_date
            ))

            conn.commit()
            cursor.close()
            conn.close()

            self.show_message("Account created successfully!")

        except mysql.connector.Error as err:
            self.show_error(f"Error: {err}")

    def generate_random_numbers(self):
        random_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        self.Entry5.delete(0, tk.END)
        self.Entry5.insert(0, random_number)

    def show_message(self, message):
        message.showinfo("Success", message)

    def show_error(self, message):
        message.showerror("Error", message)

    def validate_numbers(self, new_value):
        return re.match("^\d*$", new_value) is not None

    def validate_letters(self, new_value):
        return re.match("^[A-Za-z ]*$", new_value) is not None

    def validate_date(self, new_value):
        return re.match("^\d{0,2}/?\d{0,2}/?\d{0,4}$", new_value) is not None


class customerMenu:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Customer Section")
        window.configure(background="#00254a")

        self.Labelframe1 = tk.LabelFrame(window, relief='groove', font="-family {Segoe UI} -size 13 -weight bold",
                                         foreground="#000000", text='''Select your option''', background="#fffffe")
        self.Labelframe1.place(relx=0.081, rely=0.081, relheight=0.415, relwidth=0.848)

        self.Button1 = tk.Button(self.Labelframe1, command=self.selectWithdraw, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Withdraw''')
        self.Button1.place(relx=0.667, rely=0.195, height=34, width=181, bordermode='ignore')

        self.Button2 = tk.Button(self.Labelframe1, command=self.selectDeposit, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Deposit''')
        self.Button2.place(relx=0.04, rely=0.195, height=34, width=181, bordermode='ignore')

        self.Button3 = tk.Button(self.Labelframe1, command=self.exit, activebackground="#ececec",
                                 activeforeground="#000000",
                                 background="#39a9fc",
                                 borderwidth="0", disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11",
                                 foreground="#fffffe", highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text='''Exit''')
        self.Button3.place(relx=0.667, rely=0.683, height=34, width=181, bordermode='ignore')

        self.Button4 = tk.Button(self.Labelframe1, command=self.selectChangePIN, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Change PIN''')
        self.Button4.place(relx=0.04, rely=0.439, height=34, width=181, bordermode='ignore')

        self.Button5 = tk.Button(self.Labelframe1, command=self.selectCloseAccount, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text='''Close account''')
        self.Button5.place(relx=0.667, rely=0.439, height=34, width=181, bordermode='ignore')

        self.Button6 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#39a9fc", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text='''Check your balance''', command=self.checkBalance)
        self.Button6.place(relx=0.04, rely=0.683, height=34, width=181, bordermode='ignore')

        global Frame1_1_2
        Frame1_1_2 = tk.Frame(window, relief='groove', borderwidth="2", background="#fffffe")
        Frame1_1_2.place(relx=0.081, rely=0.547, relheight=0.415, relwidth=0.848)

    def selectDeposit(self):
        depositMoney(Toplevel(self.master))

    def selectWithdraw(self):
        withdrawMoney(Toplevel(self.master))

    def selectChangePIN(self):
        changePIN(Toplevel(self.master))

    def selectCloseAccount(self):
        self.master.withdraw()
        closeAccount(Toplevel(self.master))

    def exit(self):
        self.master.withdraw()
        CustomerLogin(Toplevel(self.master))

    def printMessage(self, output):
        # clearing the frame
        for widget in Frame1_1_2.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output_message = Label(Frame1_1_2, text=output, background="#fffffe")
        output_message.pack(pady=20)

    def printMessage_outside(output):
        # clearing the frame
        for widget in Frame1_1_2.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output_message = Label(Frame1_1_2, text=output, background="#fffffe")
        output_message.pack(pady=20)

    def checkBalance(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hamed356",
                database="bank"
            )
            cursor = conn.cursor()
            query = """
            SELECT Balance FROM CustomerTable  WHERE Account_Number = %s """
            cursor.execute(query, (customer_accNO,))
            row = cursor.fetchone()

            if row:
                output = (

                    f"Current balance : {row[0]}\n"

                )
            else:
                output = "Account not found."

            self.printMessage(output)
            print("Check balance function called.")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.printMessage(f"Error: {err}")
        self.printMessage(output)
        print("check balance function called.")



class depositMoney:
    def __init__(self, window=None, identifier=None):
        self.master = window
        self.identifier = identifier  # Card number or Account number
        window.geometry("411x117+519+278")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Deposit money")
        p1 = PhotoImage(file='./images/deposit_icon.png')
        window.iconphoto(True, p1)
        window.configure(borderwidth="2")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3",
                               font="-family {Segoe UI} -size 9", foreground="#000000", borderwidth="0",
                               text='''Enter amount to deposit :''')
        self.Label1.place(relx=0.146, rely=0.171, height=21, width=164)

        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black", selectforeground="#ffffffffffff")
        self.Entry1.place(relx=0.535, rely=0.171, height=20, relwidth=0.253)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", borderwidth="0", foreground="#ffffff",
                                 highlightbackground="#000000",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.56, rely=0.598, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 9", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", borderwidth="0", highlightcolor="black", pady="0",
                                 text='''Back''',
                                 command=self.back)
        self.Button2.place(relx=0.268, rely=0.598, height=24, width=67)

    def printMessage(self, output):
        output.showinfo("Message", output)

    def showError(self, message):
        error_window = tk.Toplevel(self.master)
        error = Error(error_window)
        error.setMessage(message)

    def submit(self, amount):
        if self.identifier is None:
            self.showError("Identifier is not set.")
            return

        if amount.isnumeric():
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="hamed356",
                    database="bank"
                )
                cursor = conn.cursor()

                identifier = self.identifier

                if identifier.isdigit() and len(identifier) == 16:  # Assuming card numbers are 16 digits
                    query = "SELECT Balance FROM CustomerTable WHERE Card_Number = %s"
                else:
                    query = "SELECT Balance FROM CustomerTable WHERE Account_Number = %s"

                cursor.execute(query, (identifier,))
                result = cursor.fetchone()

                if result:
                    current_balance = result[0]
                    new_balance = current_balance + int(amount)

                    if identifier.isdigit() and len(identifier) == 16:
                        update_query = "UPDATE CustomerTable SET Balance = %s WHERE Card_Number = %s"
                    else:
                        update_query = "UPDATE CustomerTable SET Balance = %s WHERE Account_Number = %s"

                    cursor.execute(update_query, (new_balance, identifier))
                    conn.commit()

                    output = f"Amount {amount} deposited successfully.\nUpdated balance: {new_balance}"
                    self.printMessage(output)
                    print("Deposit successful.")
                else:
                    self.showError("Account not found.")

                cursor.close()
                conn.close()

            except mysql.connector.Error as err:
                self.showError(f"Transaction failed! Error: {err}")
        else:
            self.showError("Invalid amount!")

    def back(self):
        self.master.withdraw()
class withdrawMoney:
    def __init__(self, window=None, identifier=None):
        self.master = window
        self.identifier = identifier  # Card number or Account number
        window.geometry("411x117+519+278")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Withdraw money")
        p1 = PhotoImage(file='./images/withdraw_icon.png')
        window.iconphoto(True, p1)
        window.configure(borderwidth="2")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3",
                               font="-family {Segoe UI} -size 9", foreground="#000000",
                               text='''Enter amount to withdraw :''')
        self.Label1.place(relx=0.146, rely=0.171, height=21, width=164)

        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black", selectforeground="#ffffffffffff")
        self.Entry1.place(relx=0.535, rely=0.171, height=20, relwidth=0.253)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", borderwidth="0", foreground="#ffffff",
                                 highlightbackground="#000000",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.56, rely=0.598, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", borderwidth="0", font="-family {Segoe UI} -size 9",
                                 foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Back''',
                                 command=self.back)
        self.Button2.place(relx=0.268, rely=0.598, height=24, width=67)

    def printMessage(self, output):
        output.showinfo("Message", output)

    def showError(self, message):
        error_window = tk.Toplevel(self.master)
        error = Error(error_window)
        error.setMessage(message)

    def submit(self, amount):
        if self.identifier is None:
            self.showError("Identifier is not set.")
            return

        if amount.isnumeric():
            if 25000 >= float(amount) > 0:
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="hamed356",
                        database="bank"
                    )
                    cursor = conn.cursor()

                    identifier = self.identifier

                    if identifier.isdigit() and len(identifier) == 16:  # Assuming card numbers are 16 digits
                        query = "SELECT Balance FROM CustomerTable WHERE Card_Number = %s"
                    else:
                        query = "SELECT Balance FROM CustomerTable WHERE Account_Number = %s"

                    cursor.execute(query, (identifier,))
                    result = cursor.fetchone()

                    if result:
                        current_balance = result[0]

                        if current_balance >= float(amount):
                            new_balance = current_balance - float(amount)

                            if identifier.isdigit() and len(identifier) == 16:
                                update_query = "UPDATE CustomerTable SET Balance = %s WHERE Card_Number = %s"
                            else:
                                update_query = "UPDATE CustomerTable SET Balance = %s WHERE Account_Number = %s"

                            cursor.execute(update_query, (new_balance, identifier))
                            conn.commit()

                            output = f"Amount {amount} withdrawn successfully.\nUpdated balance: {new_balance}"
                            self.printMessage(output)
                            print("Withdraw successful.")
                        else:
                            self.showError("Insufficient balance.")
                    else:
                        self.showError("Account not found.")

                    cursor.close()
                    conn.close()

                except mysql.connector.Error as err:
                    self.showError(f"Transaction failed! Error: {err}")

            else:
                self.showError("Limit exceeded!" if float(amount) > 25000 else "Positive value expected!")

        else:
            self.showError("Invalid amount!")

    def back(self):
        self.master.withdraw()


class changePIN:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x111+505+223")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Change PIN")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter new PIN:''')
        self.Label1.place(relx=0.243, rely=0.144, height=21, width=93)

        self.Label2 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Confirm PIN:''')
        self.Label2.place(relx=0.268, rely=0.414, height=21, width=82)

        self.Entry1 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.528, rely=0.144, height=20, relwidth=0.229)

        self.Entry2 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry2.place(relx=0.528, rely=0.414, height=20, relwidth=0.229)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get(), self.Entry2.get()))
        self.Button1.place(relx=0.614, rely=0.721, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text="Back", command=self.back)
        self.Button2.place(relx=0.214, rely=0.721, height=24, width=67)
    def submit(self, customer_accNO, new_PIN, confirm_new_PIN):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hamed356",
                database="bank"
            )
            cursor = conn.cursor()

            # Fetch the current PIN
            query = "SELECT PIN FROM CustomerTable WHERE Account_Number = %s"
            cursor.execute(query, (customer_accNO,))
            row = cursor.fetchone()

            if row is None:
                Error(Toplevel(self.master))
                Error.setMessage(self, message_shown="Account not found!")
                return

            current_PIN = row[0]

            if new_PIN == confirm_new_PIN and len(new_PIN) == 4 and new_PIN.isnumeric():
                if new_PIN == current_PIN:
                    Error(Toplevel(self.master))
                    Error.setMessage(self, message_shown="New PIN cannot be the same as the old PIN!")
                else:
                    # Update the PIN in the database
                    update_query = "UPDATE CustomerTable SET PIN = %s WHERE Account_Number = %s"
                    cursor.execute(update_query, (new_PIN, customer_accNO))
                    conn.commit()
                    self.master.withdraw()
            else:
                Error(Toplevel(self.master))
                if new_PIN != confirm_new_PIN:
                    Error.setMessage(self, message_shown="PIN mismatch!")
                elif len(new_PIN) != 4:
                    Error.setMessage(self, message_shown="PIN length must be 4!")
                else:
                    Error.setMessage(self, message_shown="Invalid PIN!")
                return

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown=f"Error: {err}")


class closeAccount:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+498+261")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Close Account")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter your PIN:''')
        self.Label1.place(relx=0.268, rely=0.256, height=21, width=94)

        self.Entry1 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.511, rely=0.256, height=20, relwidth=0.229)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.614, rely=0.712, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text="Back", command=self.back)
        self.Button2.place(relx=0.214, rely=0.712, height=24, width=67)

    def submit(self, customer_accNO, PIN):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hamed356",
                database="bank"
            )
            cursor = conn.cursor()

            # Check credentials
            query = "SELECT * FROM CustomerTable WHERE Account_Number = %s AND PIN = %s"
            cursor.execute(query, (customer_accNO, PIN))
            row = cursor.fetchone()

            if row:
                # Correct credentials, delete customer account
                delete_query = "DELETE FROM CustomerTable WHERE Account_Number = %s"
                cursor.execute(delete_query, (customer_accNO,))
                conn.commit()
                self.master.withdraw()
                CustomerLogin(Toplevel(self.master))
            else:
                Error(Toplevel(self.master))
                Error.setMessage(self, message_shown="Invalid PIN!")

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown=f"Error: {err}")

    def back(self):
        self.master.withdraw()
        customerMenu(Toplevel(self.master))


class checkAccountSummary:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+498+261")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Check Account Summary")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter ID :''')
        self.Label1.place(relx=0.268, rely=0.256, height=21, width=94)

        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.511, rely=0.256, height=20, relwidth=0.229)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.614, rely=0.712, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text="Back", command=self.back)
        self.Button2.place(relx=0.214, rely=0.712, height=24, width=67)

    def back(self):
        self.master.withdraw()

    def submit(self, identity):
        if not is_valid(identity):
            adminMenu.printAccountSummary(identity)
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Id doesn't exist!")
            return
        self.master.withdraw()


root = tk.Tk()
top = welcomeScreen(root)
root.mainloop()
