import requests
from bs4 import BeautifulSoup
import csv
import datetime
import sys 

# Command line arguments 
# Running the script with the -tenyr flag will fetch data for the past 10 years, using some UNIX epoch manipulations 
args = sys.argv

# If the file is ran with the -tenyr flag, fetch data from the past 10 years, starting from now 
# It should be the last argument
if args[-1] == '-tenyr':
    # Current date and time. To prevent possible issues with a date where there is no data, consider a day before.
    current = datetime.datetime.now(datetime.timezone.utc)
    current = current - datetime.timedelta(days = 1)

    # Set the time to 12:00 AM 
    current = current.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    # Get the date 10 years before. 
    ten_yrs_ago = datetime.datetime(year = current.year - 10, day = current.day, month = current.month) 

    # UNIX epoch for current date 
    current_timestamp = int(current.timestamp())
    ten_yrs_timestamp = int(ten_yrs_ago.timestamp())

    url = f"https://finance.yahoo.com/quote/%5ESPX/history/?period1={ten_yrs_timestamp}&period2={current_timestamp}"

    # Name the file differently, depending on what flag was passed 
    outfile = "spx_ten_years.csv"
else:
    url = r"https://finance.yahoo.com/quote/%5ESPX/history"
    outfile = "spx.csv"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36', 'DNT' : '1'}
req = requests.get(url, headers = headers)

# Make the content readable 
html_src = BeautifulSoup(req.text, "html.parser")
table = html_src.find('table')
table_body = table.contents[2]
table_rows = table_body.contents 

# A dictionary mapping months to their corresponding numbers 
month_abbrevs = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_nums = {month : "{index}".format(index = i + 1) for i, month in enumerate(month_abbrevs)}

# This list maps numbers 0-6 to days of the week.
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Loop over all rows 
row_count = 0
with open(outfile, 'w') as f:
    # Write the file header 
    spx_writer = csv.writer(f, delimiter=',')
    spx_writer.writerow(["Date", "Open", "High", "Low", "Close"])
    for row in table_rows:
        # Each row has 7 attributes
        # But we only want the first five 
        # Date, Open, High, Low, Close
        attributes = [row.contents[i] for i in range(0, 10, 2)]
        
        # First is the date
        # We'll format it using yyyy-mm-dd format 
        date_members = attributes[0].string.split()
        
        # Format the date 
        year = date_members[-1]
        day = date_members[1][:-1].zfill(2)
        month = month_nums[date_members[0]].zfill(2)
        date_str = "{year}-{month}-{day}".format(year = year, month = month, day = day)

        # Also add the day of the week to the front 
        date_object = datetime.date(int(year), int(month), int(day))

        # Row to write 
        spx_writer.writerow([days_of_week[date_object.weekday()], date_str] + [float(item.string.replace(',', '')) for item in attributes[1:]])
        row_count += 1

print(f"Finished creating file {outfile}. Wrote {row_count} rows.")
