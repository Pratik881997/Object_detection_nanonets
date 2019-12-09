import csv
import pandas as pd
import os

final_list = []
flag = True
with open('GH010034_HERO8 Black-GPS5.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

    for row in rows:
        if(flag):
            final_row = [row[1], row[2], row[3]]
            flag=False
        else:
            final_row = [str(row[1])[:-5], row[2], row[3]]

        final_list.append(final_row)


with open('Temp.csv', mode='w', newline='') as final_csv:
    writer = csv.writer(final_csv)
    for final_row in final_list:
        writer.writerow(final_row)

# read csv file
df = pd.read_csv('Temp.csv')

# perform groupby
res = df.groupby('date')[['GPS (Lat.) [deg]', 'GPS (Long.) [deg]']].mean().reset_index()
res.to_csv('Extracted_details.csv', index=False)

os.remove("Temp.csv")