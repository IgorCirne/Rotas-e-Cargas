import csv

# The program below is made so that we are able to import data from .csv files and insert them in the optimizer
# As there is no true data as of yet, there will need to be adjustments mad in the future to accomodate the real
# .csv file

#csv_path = "cargas.csv" # <-- Uncomment the code to use the .csv file

def load_data_from_csv(csv_path, load):
    weights = []
    volumes = []
    values = []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            weights.append(int(row["Peso"]))
            volumes.append(int(row["Volume"]))
            values.append(int(row["Valor"]))

    num_items = len(weights)
    load["weights"] = weights
    load["volumes"] = volumes
    load["values"] = values
    load["num_items"] = num_items
    load["all_items"] = range(num_items)
