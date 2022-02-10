import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import arrow
import warnings


class XE:

    DATE_FRM = "YYYY-MM-DD"

    def get(self, currency: str = None, date: str = None, save_to_csv: bool = False):

        today = arrow.now().format(self.DATE_FRM)

        if date is not None:

            try:
                date = arrow.get(date).format(self.DATE_FRM)
            except:
                raise ValueError("ERROR: don't understand your date format")
        else:
            date = today

        got_table = False

        for i in range(3):

            self.URL = f"https://www.xe.com/currencytables/?from={currency.upper()}&date={date}#table-section"

            r = requests.get(self.URL)

            if r.status_code != requests.codes.ok:
                print(f"ERROR: some problem with your request, code {r.status_code}..")
                return self

            soup = BeautifulSoup(r.text, "html.parser")

            _table_selector = "#table-section > section > div.currencytables__TablePadder-xlq26m-0.bqoUf > div > table"

            if soup.select(_table_selector):
                got_table = True
                break
            elif i == 0:
                date = arrow.get(date).shift(days=-1).format(self.DATE_FRM)
                continue
            elif i == 1:
                date = today
                continue

        if not got_table:
            warnings.warn("sorry, tried the day before and today but nothing worked")
            return self

        cols = [
            re.sub("[^\w ]", "", t.text)
            for t in soup.select(f"{_table_selector} > thead > tr > th")
        ]

        print(f"ok, found you a table for {date}")

        currency_abbreviations = [
            _.text for _ in soup.select(f"{_table_selector} > tbody > tr > th")
        ]

        fx_df = pd.concat(
            [
                pd.DataFrame(currency_abbreviations),
                pd.DataFrame(
                    [
                        [
                            s.text.replace(",", "")
                            if "." not in s.text
                            else float(s.text.replace(",", ""))
                            for s in row.find_all("td")
                        ]
                        for row in soup.select(f"{_table_selector} > tbody > tr")
                    ]
                ),
            ],
            axis=1,
            ignore_index=True,
        ).rename(columns=dict(enumerate(cols)))

        if save_to_csv:

            save_to = f"fx_rates_{currency}_{date}.csv"

            try:
                fx_df.to_csv(save_to, index=False)
            except:
                print(f"failed to save results to {save_to}")

        return fx_df
