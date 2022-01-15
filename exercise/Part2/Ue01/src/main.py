import os
import shutil
import sqlite3
import sys
from os.path import exists
from shutil import copyfile
import pandas as pd

filetypes = ('.csv', '.txt', '.json', '.db')


def validate_input() -> (str, str, str, str):

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

    if arg_count < 3:
        separator = input("Enter csv separator: ")
    else:
        separator = sys.argv[2]

    if arg_count < 4:
        table_name = input("Enter sqlite table name: ")
    else:
        table_name = sys.argv[3]

    return filename, filetype, separator, table_name


def get_filetype(name: str) -> str:
    for file_type in filetypes:
        if name.lower().endswith(file_type):
            return file_type

    raise ValueError(f'File {name} has invalid type')


def main():
    try:
        # Get filename
        filename, filetype, separator, table_name = validate_input()
        name = filename.removesuffix(filetype)

        if os.path.isdir(name):
            shutil.rmtree(name)

        print(f'Info: Creating dir {name}')
        os.makedirs(name)
        print(f'Info: Copy file {filename}')
        copyfile(filename, f'{name}/{filename}')
        os.chdir(name)

        # Check Input
        if filetype == '.db':
            conn = sqlite3.connect(filename)
            c = conn.cursor()
            c = c.execute(f"SELECT * FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            if c.fetchone() is None:
                raise ValueError(f'{filename} has no table {table_name}')

        # Read Input
        print(f'Info: Reading {filename}')
        if filetype == '.csv' or filetype == '.txt':
            df = pd.read_csv(filename,  delimiter=separator)
        elif filetype == '.db':
            conn = sqlite3.connect(filename)
            df = pd.read_sql(f'select * from {table_name}', con=conn)
        else:
            df = pd.read_json(filename, orient='records')

        # Write to output
        print('Info: Creating out dir')
        os.makedirs("out")
        output_filetypes = [x for x in filetypes if x != filetype]
        for filetype in output_filetypes:
            out_filename = f'out/{name}{filetype}'
            print(f'Info: Creating file {out_filename}')
            if filetype == '.csv' or filetype == '.txt':
                df.to_csv(out_filename, sep=separator, index=False)
            elif filetype == '.db':
                conn = sqlite3.connect(f'out/{name}.db')
                df.to_sql(name=table_name, con=conn)
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
        print(e)
    except BaseException as e:
        print(f'Exception {e}')


if __name__ == '__main__':
    main()

