import json
import collections

class ChartJsGenerator():
	def __init__(self,config,processor):
		self.www_root = config["chartjs"]["www_root"]
		self.data_file = config["general"]["data_file"]
		self.processor = processor
		self.config = config

	def generate(self):
		self.__create_stats_js()


	def __create_stats_js(self):
		js  = "var labels={}; var data = {};\n"
		js += self.__stats_last_hour()
		js += self.__stats_last_day()

		f = open(self.www_root+"/data.js","w")
		f.write(js)
		f.close()

	def __stats_last_hour(self):
		stats = self.processor.read_score_of_last_hour()
		return self.__create_javascript("LastHour",stats)


	def __stats_last_day(self):
		stats = self.processor.read_score_of_last_day()
		return self.__create_javascript("LastDay",stats)

	def __create_javascript(self, name, data):
		outlabels=""
		outdata=""
		for k,v in data.items():
			outlabels += "\"{0}\",".format(k)
			outdata   += "{0},".format(v)

		ret ="labels[\"{0}\"] = [{1}];\n".format(name,outlabels[:-1])
		ret += "data[\"{0}\"] = [{1}];\n".format(name,outdata[:-1])
		return ret
