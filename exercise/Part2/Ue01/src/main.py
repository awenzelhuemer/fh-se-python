import os
import shutil
import sqlite3
import sys
from os.path import exists
from shutil import copyfile
import pandas as pd
from pandas import DataFrame

filetypes = ('.csv', '.txt', '.json', '.db')


class FileInput:

    def __init__(self, filename: str, filetype: str, separator: str, table_name: str):
        self.filename = filename
        self.filetype = filetype
        self.separator = separator
        self.table_name = table_name


def validate_input() -> FileInput:

    arg_count = len(sys.argv)

    if arg_count > 4:
        print('<filename> <csv-delimiter> <sqlite-tablename>')
        raise ValueError(f'Invalid arguments {str(sys.argv)}')
    elif arg_count == 1:
        print(f'Allowed file types are {(str(filetypes))}')
        filename = input("Enter filename: ")
    else:
        filename = sys.argv[1]

    if not exists(filename):
        raise IOError(f'File {filename} does not exist')

    filetype = get_filetype(filename)

    if arg_count < 2:
        separator = input("Enter csv separator: ")
    else:
        separator = sys.argv[2]

    if arg_count < 3:
        table_name = input("Enter sqlite table name: ")
    else:
        table_name = sys.argv[3]

    return FileInput(filename, filetype, separator, table_name)


def get_filetype(name: str) -> str:
    for file_type in filetypes:
        if name.lower().endswith(file_type):
            return file_type

    raise ValueError(f'File {name} has invalid type')


def parse_sqlite(filename: str, table_name: str) -> DataFrame:
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c = c.execute(f"SELECT * FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    if c.fetchone() is None:
        conn.close()
        raise ValueError(f'{filename} has no table {table_name}')

    conn = sqlite3.connect(filename)
    df = pd.read_sql(f'select * from {table_name}', con=conn)
    conn.close()
    return df


def parse_csv(filename: str, separator: str) -> DataFrame:
    return pd.read_csv(filename, delimiter=separator)


def parse_json(filename) -> DataFrame:
    return pd.read_json(filename, orient='records')


def main():
    try:
        # Get filename
        file_input = validate_input()
        filename = file_input.filename
        filetype = file_input.filetype
        name = filename.removesuffix(filetype)

        if os.path.isdir(name):
            shutil.rmtree(name)

        print(f'Info: Creating dir {name}')
        os.makedirs(name)
        print(f'Info: Copy file {filename}')
        copyfile(filename, f'{name}/{filename}')
        os.chdir(name)

        # Check and read Input
        print(f'Info: Reading {filename}')
        if filetype == '.csv' or filetype == '.txt':
            df = parse_csv(filename, separator=file_input.separator)
        elif filetype == '.db':
            df = parse_sqlite(filename, table_name=file_input.table_name)
        else:
            df = parse_json(filename)

        # Write to output
        print('Info: Creating out dir')
        os.makedirs("out")
        output_filetypes = [x for x in filetypes if x != filetype]
        for filetype in output_filetypes:
            out_filename = f'out/{name}{filetype}'
            print(f'Info: Creating file {out_filename}')
            if filetype == '.csv' or filetype == '.txt':
                df.to_csv(out_filename, file_input.separator, index=False)
            elif filetype == '.db':
                conn = sqlite3.connect(f'out/{name}.db')
                df.to_sql(name=file_input.table_name, con=conn)
            else:
                df.to_json(out_filename, orient='records')

        print(f'Info: Creating information.txt')
        with open('information.txt', 'w') as f:
            f.write(f'Input file type: {filetype}\n')
            f.write(f'Total row count: {len(df)}\n')
            f.write(f'Total column count: {len(df.columns)}\n')
            f.write(f'Columns: {list(df.columns)}\n')
            f.write(f'Output file types: {output_filetypes}')

    except (IOError, ValueError) as e:
        print(f'Error: {e}')
    except BaseException as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()

