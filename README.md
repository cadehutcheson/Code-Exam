# Code-Exam - Python

This repo is for the python portion of the code exam.

send_data.py - Uses “nba_api” package to get statistics of an NBA player that is inputted by the user. Finds data for the player’s total career points and assists, as well as lists of  point and assist totals for each individual season. Data is concatenated into a string, encoded, and then sent to a given IP address through a given port.

read_and_store_data.py - uses socket module to listen for data through a given port. Two threads are created to simultaneously listen for data and store data to a database(Google Firestore) once data is received. Once data is received and decoded, it is separated so that it is sent to two different collections within the database, and properly sorted so the database receives proper field values.

The database contains 2 collections, one for each chart that will be created in the React App. When data is received, a new document in each collection is created for the individual player data to be displayed on the graphs.
