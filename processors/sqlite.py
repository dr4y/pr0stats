from datetime import datetime
import json
import requests
import sqlite3
import collections


class Processor:
    def __init__(self, config):
        self.config = config
        self.conn = sqlite3.connect(config['sqlite']['sqlite_file'])
        self.conn.cursor().execute("CREATE TABLE IF NOT EXISTS score (timestamp INTEGER, score INTEGER);")
        self.conn.commit()

    def save_score(self, data):
        self.conn.cursor().execute("INSERT INTO score VALUES (datetime('now', 'localtime'),?)",(data["user"]["score"],))
        self.conn.commit()

    def read_score(self, limit):
        sql = "SELECT strftime(\'%d.%m.%Y %H:%M\',timestamp),score FROM score ORDER BY timestamp DESC LIMIT {0};".format(int(limit))
        ret = []
        for row in self.conn.cursor().execute(sql):
            ret.append(row)
        return ret

    def read_last_score_entry(self):
        sql = "SELECT strftime('%d.%m %H:%M',timestamp), score FROM score ORDER BY timestamp DESC LIMIT 1;"
        return self.conn.cursor().execute(sql).fetchone()

    def read_score_of_last_day(self):
        sql = "SELECT strftime('%d.%m %H:%M',timestamp), score FROM score WHERE strftime('%d.%m.%Y %H:%M',timestamp) = strftime('%d.%m.%Y %H:00',timestamp) and strftime('%s','now','localtime')-strftime('%s',timestamp) < 86400 ORDER BY timestamp DESC;"
        return self.__read_result(sql, True)

    def read_score_of_last_hour(self):
        sql = "SELECT strftime('%d.%m %H:%M',timestamp), score FROM score WHERE strftime('%d.%m.%Y %H:%M',timestamp) = strftime('%d.%m.%Y %H:%M',timestamp) and strftime('%s','now','localtime')-strftime('%s',timestamp) < 3600 ORDER BY timestamp DESC;"
        return self.__read_result(sql, False)

    def __read_result(self, sql, last_item):
        data = {}
        for row in self.conn.cursor().execute(sql):
            data[row[0]] = row[1]

        if(last_item):
            last_entry = self.read_last_score_entry()
            data[last_entry[0]] = last_entry[1]

        ret = collections.OrderedDict(sorted(data.items(), key=lambda t: t[0]))
        return ret
