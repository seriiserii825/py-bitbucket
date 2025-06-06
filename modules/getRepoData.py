import csv
def getRepoData(email, ROOT_DIR):
    filename=f"{ROOT_DIR}/accounts.csv"
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["email"] == email:
                # Convert 'is_private' to boolean
                row["is_private"] = row["is_private"].lower() == "true"
                return row
    return {}

