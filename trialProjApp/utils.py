import datetime
import pandas as pd


def validation(csv_file):
    try:
        df = pd.DataFrame(csv_file)
        df = df.sort_values(by='DATE')
        for index, row in df.iterrows():
            e = validate_date(row['DATE'])
            if e:
                return 'Row %d - Failure : %s Please, check the data and try to upload again!' % (index, e)
        s = pd.Series(df['VALUE'])
        s = s.diff().to_list()
        s = s[1:]
        for dif in s:
            if dif < 0:
                return 'Failure : File contains values with negative difference!'
    except Exception as e:
        return 'Failure : %s' % e


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return "Incorrect data format, should be YYYY-MM-DD  (%s)" % date_text
