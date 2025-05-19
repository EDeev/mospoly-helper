from csv import reader, writer

def write_log(text):
    with open("../data/database/log.txt", "a") as f:
        f.writelines(text)


def view_csv(filename):
    data = []
    with open(f'../data/database/{filename}', 'r', encoding='utf-8') as csvfile:
        csvreader = reader(csvfile)
        for row in csvreader:
            data.append(row)

    return data
