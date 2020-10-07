**Steps performed:**

- Read the data of Los Angeles Region from 'https://raw.githubusercontent.com/black-tea/swarm-of-scooters/master/data/systems.csv'

- Grabbed all the coordinates from the url where the bikes are located. Defined with 'get_coordinates' function in script 'src/get_hexbins.py' where we will pass the list of urls in the functuion.

- The numpy array of coordinates collected from 'get_coordinates' function is then passed through 'get_hexagon_bins' function in script 'src/get_hexbins.py' where we will also pass the list consisting [min_lat, max_lat, min_lon, max_long] of Los Angeles Region to divide the area into equal hexagon bins and get bikes_count for each hexagon_center.

- These records are then added into database with sqlite3 with function 'get_csv_records' in script 'src/database.py' where we will pass the list of records (hexagonal_centers, bike_counts and date_and_time). The function will produce the database and csv report. 

It is created in such a way that with every iteration the records will be appended inside database while csv report will give us the average bike counts in each hexagonal_centers.

- Then cron job is setted up in AWS EC2 instance. Using scp, all required script was uploaded to my AWS EC2 instance and a virtual environment was setted up inside the instance to install requried libraries. Then opening the 'crontab -e' and adding this command '*/7 * * * * source /home/ec2-user/.bash_profile; /home/ec2-user/.venv/bin/python3 /home/ec2-user/src/main.py' (crontab.txt), ran my script in every 7 minutes. The cron job was then stopped after around 2.5 hours.

- Frequency: every 7 minutes
- Run time: For around 2.5 hours

- Total number of records collected in database 'records.db' is '254,276' which we can verify running the script 'read_database_records.py'.
- So, we ran our script  22 times and generated the csv report named 'crowdedness.csv' (can be viewed in 'output' folder) where we can see the average number of bikes in each hexagon center.


**Entire flow can be viewed in 'src/main.py'**

**Required Result:**
- CSV Report - 'output' folder (with avg_num_bikes in each hexagon center) 
- Records database - 'output' folder (with all the records for all runs)


**Tools Used:**

- For scripts: Python, Pandas, NumPy, Matplotlib
- For database: Sqlite3
- For cloud: AWS EC2
