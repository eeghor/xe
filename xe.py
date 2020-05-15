import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import arrow

class XE:
    
    DATE_FRM = 'YYYY-MM-DD'
    
    def __init__(self):
        pass
    
    def get(self, currency, date=None):
        
        today = arrow.now().format(self.DATE_FRM)
        
        if date:
                
            try:
                date = arrow.get(date).format(self.DATE_FRM)
            except:
                raise ValueError(f'ERROR: don\'t understand your date format')
        else:
            date = today
        
        got_table = False
        
        for i in range(3):
     
            self.URL = f'https://www.xe.com/currencytables/?from={currency.upper()}&date={date}'
            
            r = requests.get(self.URL)
            
            if r.status_code != requests.codes.ok:
                print(f'ERROR: some problem with your request, code {r.status_code}..')
                return self
            
            soup = BeautifulSoup(r.text, 'html.parser')
            
            if soup.find(id='historicalRateTbl'):
                got_table = True
                break
            elif i == 0:
                date = arrow.get(date).shift(days=-1).format(self.DATE_FRM)
                continue
            elif i == 1:
                date = today
                continue
        
        if not got_table:
            print('sorry, tried the day before and today but nothing worked')
            return self
  
        cols = [re.sub('[^\w ]', '',  t.text) for t in soup.select('#historicalRateTbl>thead>tr>th')]
    
        print(f'ok, found you a table for {date}')
        
        return (pd.DataFrame([[s.text if '.' not in s.text else float(s.text) for s in row.find_all('td')] 
                      for row in soup.find(id='historicalRateTbl').tbody.find_all('tr')])
                            .rename(columns=dict(enumerate(cols))))