import pandas as pd
import csv

text_file = "lables.txt"
csv_file = "labels.csv"

with open(text_file, 'r') as infile, open(csvfile, 'w') as outfile:
     stripped = (line.strip() for line in infile)
     lines = (line.split(",") for line in stripped if line)
     writer = csv.writer(outfile)
     writer.writerows(lines)
