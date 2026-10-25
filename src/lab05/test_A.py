from src.lab05.json_csv import json_to_csv, csv_to_json
import csv
import json

json_to_csv("data/lab05/samples/people.json", "data/lab05/out/people_from_json.csv")
csv_to_json("data/lab05/samples/people.csv", "data/lab05/out/people_from_csv.json")

with open("data/lab05/out/people_from_json.csv", newline="", encoding="utf-8") as f:
    print("CSV строк с данными:", len(list(csv.DictReader(f))))

with open("data/lab05/out/people_from_csv.json", encoding="utf-8") as f:
    print("JSON объектов:", len(json.load(f)))