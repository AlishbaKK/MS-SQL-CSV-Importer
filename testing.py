# Import necessary libraries
import csv
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, filedialog
import pyodbc
from PIL import ImageTk,Image
import customtkinter

# Replace server_name and database_name with your own values
server_name = 'Your server name'
database_name = 'Your database name'

# Create the connection string with Windows Authentication
conn_str ='Driver={SQL Server};Server=' + server_name + ';Database=' + database_name + ';Trusted_Connection=yes;'

# Connect to the SQL Server database
conn=pyodbc.connect(conn_str)

# Create a cursor object
cursor = conn.cursor()

filenames=[]

# create a function to handle the import of CSV files
def import_csv():
    global filenames
    global table_name_filemanager

    # open a file dialog to choose a CSV file to import
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    # if no file was chosen, return without doing anything
    if not file_path:
        return

    # to retrieve the file name
    filename = os.path.basename(file_path)
    filenames.append(filename)

    # show a success message
    messagebox.showinfo("Success", "CSV file imported successfully!")

    # create table names
    table_name_filemanager = f'files{value_acc[0]}'

    # check if table already exists in db
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name_filemanager}'")
    table_exists = cursor.fetchone()[0] > 0

    if not table_exists:
        # command to create new table in db
        create_table_sql = f"CREATE TABLE {table_name_filemanager} (filename VARCHAR(50) PRIMARY KEY);"
        try:
            # execute command to create new table in db
            cursor.execute(create_table_sql)
        except Exception as e:
            # error message
            print(f"Creation error: {e}")
        else:
            print("Table created!")

    # sql command to add file to db table
    insert_statement_sql = f"INSERT INTO {table_name_filemanager} (filename) VALUES (?);"
    cursor = conn.cursor()

    #execute command to file in the db table
    try:
        cursor.execute(insert_statement_sql, (filename))
        cursor.commit()
    except Exception as e:
        # error message
        print(f"Insertion error: {e}")

    #import file into DB
    #open csv file
    with open(file_path, 'r') as f:
        # read the first line of the csv files to determine the number of columns
        reader = csv.reader(f, delimiter = ',')
        #output number of columns
        num_cols = len(next(reader))

        row_values_all = []
        first_row = next(reader)
        row_values_all.append(first_row)

        for row in reader:
            # Within this loop, a new empty list called 'row_values' is created.
            row_values = []
            # Another 'for' loop is used to iterate over each value in the current row, and the 'split(",")' function is used to split the value into multiple values if it contains a comma.
            for value in row:
                # The value is appended to the 'row_values' list without being split.
                row_values.append(value)
            # After the inner loop has finished, the 'row_values' list is appended to the 'row_values_all' list.
            row_values_all.append(row_values)

        global table_name
        #create unique table names based on date and time
        table_name = datetime.now().strftime("importeddata_%Y%m%d_%H%M%S")

        #create table in sql
        create_table_sql = f"CREATE TABLE {table_name} (id INT IDENTITY(1,1) PRIMARY KEY,"
        for i in range(num_cols):
            column_data_type = "NVARCHAR(MAX)"  # assume that all columns nvarchar
            create_table_sql += f"col{i} {column_data_type},"
        create_table_sql = create_table_sql[:-1] + ")"  #remove trailing comma and close parentheses

        #execute create table sql command
        cursor = conn.cursor()
        cursor.execute(create_table_sql)

        #iterate through each line of the csv and insert them into sql server
        num_of_columns = num_cols
        placeholders = ",".join("?" * num_of_columns)
        insert_statement = f"INSERT INTO {table_name} VALUES ({placeholders})"

        for row in row_values_all:
            row_values = row
            cursor = conn.cursor()
            cursor.execute(insert_statement, *row_values)
            cursor.commit()


#function to display all imported files
def File_Manager():
    #file manager window
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    root2 = customtkinter.CTk()
    root2.geometry("500x600")
    root2.title("File Manager")
    root2.resizable(False, False)
    root2.config(bg="#34495E")
    root2.iconbitmap('icon.ico')

    # Sign in frame
    signin3 = customtkinter.CTkFrame(root2)
    signin3.pack(padx=15, pady=15, fill='both', expand=True)

    #label to show imported csv
    Label_of_filemanager = customtkinter.CTkLabel(signin3, text="List of All imported CSV's", text_font=("Inter SemiBold", 26, "bold"))
    Label_of_filemanager.pack(padx=20, pady=15)

    try:
        query = f"SELECT * FROM files{value_acc[0]};"
        cursor.execute(query)
        # Fetch all rows from the result set
        rows = cursor.fetchall()
        values = [row[0] for row in rows]

        # iterate over all csv
        for i in range(len(values)):
            # create a label to display each CSV file name
            label = customtkinter.CTkLabel(signin3, text=f'{i + 1})  {values[i]}',text_font=('Inter SemiBold', 16))
            # add padding to the label
            label.pack(padx=17, pady=10)
    except Exception as e:
        label =customtkinter.CTkLabel(signin3, text="No CSV's imported", text_font=('Inter SemiBold', 16))
        # add padding to the label
        label.pack(padx=20, pady=10)
        print(e)

    root2.mainloop()

#function for search bar
def search_csv():
    #result of the search with get
    searched_value = search_bar.get()

    #initialize empty list to add files
    matching_files = []
    files=[]

    #check whether the value in search field is not empty
    if searched_value != "":
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        #new window for search results
        root3 = customtkinter.CTk()
        root3.geometry("500x600")
        root3.title("Search Results")
        root3.config(bg="#34495E")
        root3.resizable(False, False)
        root3.iconbitmap('icon.ico')

        # Sign in frame
        signin4 = customtkinter.CTkFrame(root3)
        signin4.pack(padx=15, pady=15, fill='both', expand=True)

        query = f"SELECT * FROM files{value_acc[0]};"
        cursor.execute(query)
        # Fetch all rows from the result set
        rows = cursor.fetchall()
        values = [row[0] for row in rows]
        for i in values:
            files.append(i)

        #iterate over all csv files
        for results in files:
            result = results.upper()
            value_searched_upper = searched_value.upper()
            if value_searched_upper in result:
                matching_files.append(results)
        #check if there are any matching files
        if matching_files != []:
            # create a label to show that the search results will be displayed below
            search_label = customtkinter.CTkLabel(signin4, text="Search results will be shown here.",text_font=("Inter SemiBold",20, "bold"))
            # add padding to the label
            search_label.pack(padx=20, pady=15)

            #iterate over all the matching files
            for i in range(len(matching_files)):
                # create a label to display each matching file name
                label1 = customtkinter.CTkLabel(signin4, text=f'{i + 1})  {matching_files[i]}',text_font=('Inter SemiBold', 16))
                # add padding to the label
                label1.pack(padx=20, pady=10)
                # run the window
            root3.mainloop()

        else:
            # create a label to show that the search results will be displayed below
            search_label = customtkinter.CTkLabel(signin4, text="Search results will be shown here.",text_font=("Inter SemiBold", 26, "bold"))
            # add padding to the label
            search_label.pack(padx=20, pady=15)

            # create a label to show that there are no matching files
            search_label_1 = customtkinter.CTkLabel(signin4, text="No such file.",text_font=('Inter SemiBold', 16))
            # add padding to the label
            search_label_1.pack(padx=20, pady=15)
    else:
        # show an error message if the searched value is empty
        messagebox.showerror("ERROR!!", "Please enter a file name.")

# This function creates a new account in a database table.
def account_creation():
    # Get user input values for email and password
    email_signup = email_value_signup.get()
    password_signup = password_value_signup.get()
    first_name=firstname.get()
    surname_value=surname.get()
    date_value=date.get()
    month_value=month.get()
    year_value=year.get()
    gender_value=gender.get()
    dob_value=date_value+"-"+month_value+"-"+year_value


    # Check if email and password fields are filled
    if email_signup == "" or password_signup == "" or first_name== "" or surname_value=="" or dob_value=="" or gender_value=="":
        # Show an error message box if any of the fields are empty
        messagebox.showerror("ERROR!!!", "All fields must be filled.")

    else:
        # Generate table name
        table_name_signup = "Accountsinfo"
        # Check if the table already exists in the database
        cursor = conn.cursor()
        # The line then checks whether a table with the same name already exists in the database by executing a SQL query using the cursor object. The query selects the count of tables in the database where the table name matches table_name_signup. If the count is greater than zero, that means the table already exists.
        cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name_signup}'")
        # cursor.fetchone()[0] accesses the first (and only) element of the row returned by cursor.fetchone(), which is the count value.
        table_exists = cursor.fetchone()[0] > 0

        if not table_exists:
            # Construct SQL statement to create a new table in the database
            create_table_sql = f"CREATE TABLE {table_name_signup} (email VARCHAR(50) PRIMARY KEY,password VARCHAR(50),firstname VARCHAR(50),surname VARCHAR(50),dob VARCHAR(50),gender VARCHAR(50));"
            try:
                # Execute the SQL statement to create a new table in the database
                cursor.execute(create_table_sql)

            except Exception as e:
                # Print an error message if the table creation fails
                print(f"Error creating table: {e}")
            else:
                # Print a success message if the table creation is successful
                print("Table created successfully!")
        # Construct SQL statement to insert data into the database table
        insert_statement_sql = f"INSERT INTO {table_name_signup} (email, password, firstname, surname, dob, gender) VALUES (?, ?, ?, ?, ?, ?);"
        cursor = conn.cursor()
        # Execute the SQL statement to insert the user data into the table
        try:
            cursor.execute(insert_statement_sql, (email_signup, password_signup,first_name,surname_value,dob_value,gender_value))
            cursor.commit()
            # Show a success message box after the account creation is successful
            messagebox.showinfo("Success", "Account has been created successfully!")
        except Exception as e:
            # Print an error message if the table creation fails
            print(f"Error inserting in table: {e}")
        # Close the account creation window
        root4.destroy()


# This code creates a GUI window for the user to sign up for a new account.
def sign_up_screen():
    # Access the global variable root4 to create the GUI window
    global root4
    global email_value_signup
    global password_value_signup
    global firstname
    global surname
    global date
    global month
    global year
    global gender
    # Themes: "blue" (standard), "green", "dark-blue"
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    root4 = customtkinter.CTk()
    # Set the size and title of the GUI window
    root4.geometry("500x600")
    root4.title("Sign Up")
    root4.resizable(False, False)
    root4.config(bg="#34495E")
    root4.iconbitmap('icon.ico')

    # Sign in frame
    signin2 = customtkinter.CTkFrame(root4)
    signin2.pack(padx=15, pady=15, fill='both', expand=True)

    # Create a header label for the sign up form
    Label_header = customtkinter.CTkLabel(signin2, text="SIGN UP FORM", text_font=("Inter SemiBold", 26, "bold"))
    Label_header.place(x=30, y=30)

    Label_subheader = customtkinter.CTkLabel(signin2, text="It's quick and easy.", text_font=("Inter SemiBold", 16))
    Label_subheader.place(x=30, y=70)

    # Create a label and entry field for the user's email
    firstname = customtkinter.CTkEntry(signin2, placeholder_text="First Name", text_font=('Inter SemiBold', 16),
                                       width=180)
    firstname.place(x=30, y=130)

    surname = customtkinter.CTkEntry(signin2, placeholder_text="Surname", text_font=('Inter SemiBold', 16), width=180)
    surname.place(x=260, y=130)

    email_value_signup = customtkinter.CTkEntry(signin2, placeholder_text="email address", width=410,
                                                text_font=('Inter SemiBold', 16))
    email_value_signup.place(x=28, y=200)

    # Create a label and entry field for the user's password
    password_value_signup = customtkinter.CTkEntry(signin2, placeholder_text="Password",
                                                   text_font=('Inter SemiBold', 16), width=410,show="*")
    password_value_signup.place(x=28, y=270)

    dob_label = customtkinter.CTkLabel(signin2, text="Enter your date of birth", text_font=('Inter SemiBold', 13))
    dob_label.place(x=28, y=320)

    date = customtkinter.CTkComboBox(signin2,
                                     values=['1', "2", "3", "4", "5", "6", '7', "8", "9", "10", "11", "12", '13', "14",
                                             "15", "16", "17", "18", '19', "20", "21", "22", "23", "24", "25", "26",
                                             "27", "28", "29", "30", "31"], width=120)
    date.set("1")
    date.place(x=28, y=370)

    month = customtkinter.CTkComboBox(signin2,
                                      values=['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep',
                                              'Oct', 'Nov', 'Dec'], width=120)
    month.set('Jan')
    month.place(x=178, y=370)

    year = customtkinter.CTkComboBox(signin2,
                                     values=['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015',
                                             '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006',
                                             '2005', '2004', '2003', '2002', '2001', '2000'], width=120)
    year.set('2023')
    year.place(x=320, y=370)

    gender_label = customtkinter.CTkLabel(signin2, text="Gender", text_font=('Inter SemiBold', 13))
    gender_label.place(x=-15, y=420)

    gender = customtkinter.CTkComboBox(signin2, values=['Female', 'Male', 'Other'])
    gender.set('Female')
    gender.place(x=28, y=470)

    # Create a button to submit the sign up form and execute the account_creation() function
    sign_button = customtkinter.CTkButton(signin2, text="Create Account", command=account_creation,
                                          text_font=('Inter SemiBold', 16), padx=10, pady=5, bd=1, width=150)
    sign_button.place(x=140, y=515)

    # Start the main event loop to display the GUI window
    root4.mainloop()

#Log in function
def Login():
    global search_bar
    global email
    global value_acc

    # get the email and password values from the entry widgets
    email = email_value.get()
    value_acc = email.split(sep="@")
    password = password_value.get()

    table_name_signup = "Accountsinfo"

    # Construct the SQL query to check if the email and password match
    select_sql = f"SELECT email FROM {table_name_signup} WHERE email = ? AND password = ?"

    # Execute the query and fetch the result
    cursor = conn.cursor()
    cursor.execute(select_sql, (email, password))
    result = cursor.fetchone()

    # Check if a row was returned
    if result:
        # If a row was returned, the email and password match
        messagebox.showinfo("Success!!", "Log in Successful!!")
        # close the main window
        root.destroy()
        # create a new window for the dashboard
        root1 = customtkinter.CTk()
        root1.iconbitmap('icon.ico')
        root1.geometry("500x600")
        root1.resizable(False, False)
        root1.title("CSV Importer")
        root1.config(bg="#34495E")

        # Sign in frame
        signin1 = customtkinter.CTkFrame(root1)
        signin1.pack(padx=15, pady=15, fill='both', expand=True)


        logo = ImageTk.PhotoImage(Image.open('CSV IMPORTER.png').resize((710, 240), Image.ANTIALIAS))

        # Create a Tkinter label and set the image as its content:
        img_label_csv = customtkinter.CTkLabel(signin1, image=logo)
        img_label_csv.place(x=0,y=0)

        # create the file manager button
        file_manager_button = customtkinter.CTkButton(signin1, text="File Manager", command=File_Manager, text_font=("Arial", 12), padx=10, pady=5, bd=1, width=200)
        file_manager_button.place(x=130,y=220)

        # create the import button
        import_button =customtkinter.CTkButton(signin1, text="Import", command=import_csv, text_font=("Arial", 12),padx=10, pady=5, bd=1, width=200)
        import_button.place(x=130,y=290)

        # Create the log out button
        logout_button = customtkinter.CTkButton(signin1, text="Log out", command=root1.destroy, text_font=("Arial", 12), padx=10, pady=5, bd=1, width=200)
        logout_button.place(x=130,y=360)

        # create the search bar and button
        search_var = tk.StringVar()
        search_bar = customtkinter.CTkEntry(signin1, textvariable=search_var, text_font=("Arial", 12),width=280)
        search_bar.place(x=50,y=440)
        search_button = customtkinter.CTkButton(signin1, text="Search", command=search_csv, text_font=("Arial", 12), padx=10, pady=5, bd=1, width=10)
        search_button.place(x=340,y=435)

        # start the event loop for the dashboard window
        root1.mainloop()
    else:
        # If no row was returned, the email and password do not match
        # show error message if email and/or password is incorrect
        messagebox.showerror("ERROR!!!", "Please enter the correct email and password.")

# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# create the main window
root = customtkinter.CTk()
root.geometry("430x600")
root.resizable(False, False)
root.iconbitmap('icon.ico')
root.title("CSV Importer")
root.config(bg="#34495E")

# Sign in frame
signin = customtkinter.CTkFrame(root)
signin.pack(padx=15, pady=15, fill='both', expand=True)

person = ImageTk.PhotoImage(Image.open('main.png').resize((248, 248), Image.ANTIALIAS))


# Create a Tkinter label and set the image as its content:
img_label = customtkinter.CTkLabel(signin, image=person)
img_label.place(x=120,y=45)


# create the email and password widgets
email_label = customtkinter.CTkLabel(signin, text="Email", text_font=('Inter SemiBold', 16))
email_label.place(x=10, y=280)

email_value = customtkinter.CTkEntry(signin, width=230,height=40,border_width=2,corner_radius=10)
email_value.place(x=145, y=275)
email_value.focus()

password =customtkinter.CTkLabel(signin, text="Password", text_font=('Inter SemiBold', 16))
password.place(x=10, y=360)

password_value = customtkinter.CTkEntry(signin, width=230,height=40,border_width=2,corner_radius=10,show="*")
password_value.place(x=145, y=355)

# create the login button
login_button = customtkinter.CTkButton(signin, text="Login", compound='right',command=Login, text_font=('Inter SemiBold', 14),padx=10, pady=5, width=150,height=40,corner_radius=5)
login_button.place(x=125, y=440)

# create the signup button
signup_button = customtkinter.CTkButton(signin, text="Sign Up", compound='right',command=sign_up_screen,  text_font=('Inter SemiBold', 14),padx=10, pady=5, width=150,height=40,corner_radius=5)
signup_button.place(x=125, y=500)

# start the event loop for the main window
root.mainloop()