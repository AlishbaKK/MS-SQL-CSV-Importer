# MS-SQL-CSV-Importer
This Python-based CSV importer is designed to establish a connection with a SQL Server database, leveraging Windows Authentication for secure access. The code facilitates seamless importing of CSV files, enabling users to effortlessly create tables and efficiently insert data into the database. Additionally, the code encompasses robust file management capabilities and an integrated search function. The solution is built with Python and incorporates the Tkinter framework.
# Features
1) **Easy Installation**: The CSV Importer can be quickly installed on your local machine or server using simple installation instructions.
2) **Intuitive Graphical User Interface:** The tool provides a graphical user interface that allows you to seamlessly import CSV files into SQL Server without any complex configurations.
3) **Efficient Bulk Insertion:** Leveraging SQL Server's bulk insert functionality, the CSV Importer efficiently inserts data from CSV files into SQL Server tables, optimizing the import process.
4) **Logging and Error Handling:** Comprehensive logging and error handling mechanisms are in place to provide detailed information about the import process and handle any encountered issues effectively.
5) **Data Validation:** The tool performs data validation during the import process, ensuring the integrity and accuracy of the data being imported.
# Installation
1) Clone the repository to your local machine using the following command:
   git clone https://github.com/AlishbaKK/MS-SQL-CSVImporter.git 
2) Navigate to the project directory:
   cd MS-SQL-CSVImporter
3) Ensure you have Python 3.10 installed on your system. You can download it from the official Python website.
4) Install the MSSQL ODBC Driver on your system. This is necessary for connecting to the MSSQL database. You can download the driver from the official 
   Microsoft website.
5) Download SQL Server Express
6) Go to the Microsoft SQL Server Management Studio download page: https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms
7) Select the latest version of SSMS that is compatible with your system.
8) Choose the language and download the installation file.
9) Run the installation file and follow the installation wizard to install SSMS on your system.
10) Once the installation is complete, you can launch SSMS and connect to your SQL Server instance by providing the server name and authentication credentials.
11) Install the required dependencies by running: pip install -r requirements.txt
12) Run the project using the following command: python testing.py
13) The GUI interface will launch, allowing you to interact with your project.

# Usage
1) Ensure you have followed the installation guide and have the project set up on your system.
2) Launch the project by running the following command in your terminal:
   python main.py
3) The graphical user interface (GUI) will open, presenting you with the login screen.
4) Enter your account credentials (username and password) to log in to your account.
5) If you dont have an account, then click on sign up button and create an account.
6) Upon successful login, the file manager will be displayed, showing all the CSV files imported from your account.
7) To import a new CSV file into your account, click on the "Import CSV" buttonA file dialog will open, allowing you to select the CSV file from your local system. Choose the desired CSV file.
8) The imported CSV file will be added to your account and will now be visible in the file manager.
9) To search the imported CSV's by name, there is a search bar.
10) To log out of your account, click on the "Log Out" button.
# License
This project is licensed under the MIT License.
# Contributing
Contributions to the CSV Importer project are welcome. Please read our Contribution Guidelines for more information on how to contribute.
