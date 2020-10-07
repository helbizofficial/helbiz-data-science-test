import os
import sqlite3
import pandas as pd


def get_csv_records(records:list, destination_path):

    # stating the destination path as the 'output' folder
    database_path = os.path.join(destination_path, 'records.db')
    csv_path = os.path.join(destination_path, 'crowdedness.csv')
    
    # checking if database exists
    database_exist = False
    if os.path.isfile(database_path):
        database_exist = True

    # sqlite connection
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # if database doesnot exit, create the table and append the records
    if not database_exist:
        c.execute('''CREATE TABLE data
                (date_and_time, hexagon_center, num_bikes)''')

    # if database exist, only append the records
    for i in records:
        c.execute('insert into data values (?,?,?)', [i['date_and_time'], i['hexagon_center'], i['num_bikes']])
    conn.commit()

    # creating the dataframe from databse and sorting it based on num of bikes in descending order
    df = pd.read_sql('SELECT * from data', conn)
    df = df.sort_values(by='num_bikes', ascending=False)

    # checking if csv already exists
    if os.path.isfile(csv_path):
        # if csv file exists for the current iterateion then delete the old csv file as we have complete dataframe from database
        os.remove(csv_path)

        # grouping it based on hexagon_center and taking the mean of 'num_bikes' of this iteration and previous iteration
        group_df = df.groupby('hexagon_center')['num_bikes'].mean()

        # addind the average num of bikes of both iteration as 'num_bikes_avg' column and dropping the old 'num_bikes' column
        # also checking if there's a duplicate hexagon_center and dropping if it exists since we already have 'avg_num_bikes'
        grouped_df = df.join(group_df, on='hexagon_center', rsuffix="_avg").drop(['num_bikes'], axis = 1).drop_duplicates(subset=['hexagon_center'])
        grouped_df.to_csv(csv_path, index=False)
    else:
        # if csv doesnot exist, then create a new file
        df.to_csv(csv_path, index=False)