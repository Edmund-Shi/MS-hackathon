import csv


def get_dataset():
    filename = "export.csv"
    dataset = {}
    header = []
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            uid, command, params, os_type, source, begin, end = row
            if reader.line_num == 1:
                header = row
                continue
            if uid not in dataset:
                dataset[uid] = [row[1:]]
            else:
                last_cmd, last_params, *_ = dataset[uid][-1]
                if last_cmd == command and last_params == params:
                    continue  # duplicate
                dataset[uid].append(row[1:])
    return dataset


if __name__ == "__main__":
    get_dataset()
