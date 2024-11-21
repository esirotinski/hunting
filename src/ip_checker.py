import pathlib
import sqlite3
import requests

from datetime import datetime
from contextlib import closing
from utils.smtplib_send_message import smtp_send_text

# def adapt_datetime_iso(val):
#     """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
#     return val.isoformat()
# sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)
#
# def convert_datetime(val):
#     """Convert ISO 8601 datetime to datetime.datetime object."""
#     return datetime.datetime.fromisoformat(val.decode())
# sqlite3.register_converter("datetime", convert_datetime)

def get_current_ip_address():
    try:
        response = requests.get('https://showip.net')
        response.raise_for_status()
    except Exception as e:
        smtp_send_text('Matei failed to fetch from showip.net', str(e))
        raise Exception(e)
    else:
        return response.text

def main():
    db = 'ip_history.db'

    if pathlib.Path(db).is_file():

        with closing(sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)) as connection:
            with closing(connection.cursor()) as cursor:
                row = cursor.execute('SELECT * FROM allocation_history ORDER BY created_at DESC').fetchone()

        last_ip_address = row[0]
        current_ip_address = get_current_ip_address()

        if last_ip_address != current_ip_address:
            smtp_send_text('Matei has new IP address.', str(current_ip_address))
            with closing(
                    sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)) as connection:
                with closing(connection.cursor()) as cursor:
                    insert_query = 'INSERT INTO allocation_history VALUES(?, ?)'
                    cursor.execute(insert_query, (str(current_ip_address), datetime.now()))
                    connection.commit()

    else:
        connection = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE allocation_history (ip TEXT, created_at TIMESTAMP)')
        insert_query = 'INSERT INTO allocation_history VALUES(?, ?)'
        cursor.execute(insert_query, ('127.0.0.1', datetime.now()))
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == '__main__':
    main()