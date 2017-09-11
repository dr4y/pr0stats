from datetime import datetime
import json
import requests
import collections

class Processor:
    def __init__(self, config):
        self.config = config
        self.data = False

    def save_score(self, data):
        dat = {"date":datetime.now().strftime('%d.%m.%Y - %H:%M'), "score": data["user"]["score"]}
        f = open(self.config["general"]["data_file"],"a")
        f.write(json.dumps(dat, sort_keys=True)+"\n")
        f.close()
        self.__refresh()

    def __refresh(self):
        f = open(self.config["general"]["data_file"],"r")
        self.data = f.readlines()
        f.close()


    def read_data(self):
        if not self.data:
            self.__refresh()
        return self.data

    def read_last_score_entry(self):
        if not self.data:
            self.__refresh()
        return self.data[-1]

    def read_score_of_last_day(self):
        if not self.data:
            self.__refresh()

        ret = collections.OrderedDict()
        for l in self.data:
            if ":00" in l:
                d = json.loads(l.strip())
                ret[d["date"].replace("2017","")] = d["score"]

        last_entry = json.loads(self.data[-1])
        ret[last_entry["date"].replace("2017","")] = last_entry["score"]
        return ret

    def read_score_of_last_hour(self):
        if not self.data:
            self.__refresh()

        ret = collections.OrderedDict()
        for l in self.data[-60:]:
            d = json.loads(l.strip())
            ret[d["date"].replace("2017","")] = d["score"]

        return ret
