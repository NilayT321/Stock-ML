import requests
from bs4 import BeautifulSoup
import csv
import datetime

url = r"https://finance.yahoo.com/quote/%5ESPX/history"
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
with open('spx.csv', 'w') as f:
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

print("Finished creating file spx.csv. Wrote {row_count} rows.".format(row_count = row_count))
