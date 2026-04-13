
cvs-sql is a Python script that loads CSV files downloaded from
British banks into a sqlite3 database.

This project is now terminated as it only works on CSVs from one UK bank. 

Please read the license for disclaimer of responsibility
for any data loss.

For more details about the project, please visit
https://voleproject.org.uk/project.html

The script will load a database with each transaction
given an unique id (a "tid").

No transaction will be duplicated in the database.

Transactions will be verified to see if the balance
of the previous transaction plus the value of the current
transaction is equal to the balance
of the current transaction

The script will give a list of date ranges where
transactions are missing.


