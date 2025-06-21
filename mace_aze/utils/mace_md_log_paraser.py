import csv
import numpy as np
from mace_aze.utils.io import find_md_log

def parse_md_out_log(filepath):
    table = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Process header
    header_line = lines[0].lstrip('#').replace('"', '').strip()
    headers = header_line.split(',')

    for line in lines[1:]:
        row = next(csv.reader([line.strip()]))
        processed_row = []

        for i, item in enumerate(row):
            item = item.strip()
            col_name = headers[i]

            if item == '--':
                value = None
            elif item.endswith('%'):
                try:
                    value = float(item.strip('%')) / 100
                except ValueError:
                    value = None
            elif col_name == "Time Remaining":
                value = item  # keep as string
            else:
                try:
                    value = float(item)
                except ValueError:
                    value = item  # fallback: keep as-is

            processed_row.append(value)

        table.append(dict(zip(headers, processed_row)))

    return table

def extract_column(table, column_name):
    return np.array(
        [row[column_name] for row in table if row[column_name] is not None],
        dtype=float
    )

def get_temp(traj_path: str):
    md_path = find_md_log(traj_path)
    if md_path is None:
        return np.array([])
    table = parse_md_out_log(md_path)
    return extract_column(table, "Temperature (K)")

# # Example usage
# if __name__ == "__main__":
#     filepath = 'mace_md.log'
#     table = parse_md_out_log(filepath)
#     volume_array = extract_column(table, "Temperature (K)")
#     print(volume_array)
