import configparser


conf = configparser.ConfigParser()
conf.read("../config.ini")

url = conf["alphav"]["url"]
api_key = conf["alphav"]["api_key"]
period = conf["fx"]["period"]
csv_path = conf["csv"]["path"]