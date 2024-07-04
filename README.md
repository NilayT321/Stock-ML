# Stock-ML
Some machine learning and data curation tasks based on stock market data on the S&amp;P index using Yahoo Finance data. 

## Running The Finance Scraper 

The file `finance_scraper.py` is a web-scraping script which retrieves data for the S&amp;P index from Yahoo Finance. The script is a standard Python script and should be invoked as follows 
```bash
$ python3 finance_scraper.py [-tenyr]
```
The script takes an optional command-line argument `-tenyr` (should be passed as the last argument). If this argument is passed, the script will retrieve data from the last 10 years. To prevent issues with a date possibly not existing, the script will retrieve data using yesterday's date and the date 10 years prior to yesterday's date. If the script is ran without the `-tenyr` argument, the script will retrieve data for the past year. 
