**Database Migration and Rollback**

_Overview_
<br />
The project is developed using SQL, python, and PostgreSQL database. The project contains 3 different source files: The initialization.sql file sets up the initial state of the database. The migration script updates the schema of existing tables, while the rollback script reverts the changes made by the migration.<br />
<br />
_Requirements:_
<br />
•	PostgreSQL database server (should run on port 5433)
<br />
•	pg8000 Python library ("pip install pg8000" command for installing)

_How to run?_
<br />
* First download the zip file from repository (alternatively, clone repository to your machine) 
* open directory through IDE or any other tool. (Pycharm recommended for compiling python scripts and database extension flexibility)
* Run initialization.sql file in order to create tables and inserting data. (Make sure is postgreSQL server is running on your local machine; port 5433)
* Then you should run migration.py file to migrate databases to updated versions of them. (If you are using terminal, on project directory, command "python migration.py" will be enough to run script successfully)
* In order to rollback to previous version of database then run rollback.py file.
<br />

_Additional Notes:_
* During the migration process, the tables might be populated with new data. The migration script handles this scenario by migrating the existing data to the new schema.
* Error Handling: If any errors occur during the migration or rollback process, the scripts will handle them gracefully and roll back the changes to maintain data integrity with the power of pg8000 library.
