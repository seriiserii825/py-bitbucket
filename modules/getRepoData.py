import csv
def getRepoData(ROOT_DIR):
    filename=f"{ROOT_DIR}/accounts.csv"
    rows = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["is_private"] = row["is_private"].lower() == "true"
            rows.append(row)
    return rows

