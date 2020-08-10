import datetime
import time
import json
import pandas as pd


def prepare_detail(meter_data_list):
    range_set = [list((m.value, m.date.strftime('%Y-%m-%d'))) for m in meter_data_list]
    dump = json.dumps(range_set)
    df = pd.DataFrame(range_set, columns=['ABSOLUTE VALUE', 'DATE'])
    y_range_set = [time.mktime(y.date.timetuple()) * 1000 for y in meter_data_list]
    x_range_set = [x.value for x in meter_data_list]
    x_values = []
    if len(x_range_set) > 0:
        x_values.append(x_range_set[0])
        for v in range(1, len(x_range_set)):
            x_values.append(abs(x_range_set[v] - x_range_set[v - 1]))
    df['RELATIVE VALUE'] = x_values
    ready_data = {'meterDataList': meter_data_list,
                  'dump': dump,
                  'xRangeSet': x_range_set,
                  'yRangeSet': y_range_set[1:],
                  'xValues': x_values[1:],
                  'dataTable': df}
    return ready_data


def validation(csv_file):
    try:
        df = pd.DataFrame(csv_file)
        df = df.sort_values(by='DATE')
        for index, row in df.iterrows():
            e = validate_date(row['DATE'])
            if e:
                return 'Row of the csv - %d - Failure : %s Please, check the date format and try to upload again!' % (
                index + 2, e)
        s = pd.Series(df['VALUE'])
        s = s.diff().to_list()
        s = s[1:]
        for dif in s:
            if dif < 0:
                return 'Row of the csv - %d - Failure : File contains values with negative difference!' % (
                            s.index(dif) + 3)
    except Exception as e:
        return 'Failure : %s' % e


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return "Incorrect data format, should be YYYY-MM-DD  (%s)" % date_text
