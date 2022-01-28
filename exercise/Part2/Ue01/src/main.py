import os
import shutil
import sqlite3
import sys
from os import listdir
from os.path import exists, isfile, join
from shutil import copyfile
import pandas as pd
from pandas import DataFrame

filetypes = (".csv", ".txt", ".json", ".db")


class FileInput:

    def __init__(self, filename: str, filetype: str, separator: str):
        self.filename = filename
        self.filetype = filetype
        self.separator = separator


def validate_input() -> FileInput:

    arg_count = len(sys.argv)

    if arg_count > 4:
        print("<filename> <csv-delimiter>")
        raise ValueError(f"Invalid arguments {str(sys.argv)}")
    elif arg_count == 1:
        print(f"Allowed file types are {(str(filetypes))}")
        filename = input("Enter filename: ")
    else:
        filename = sys.argv[1]

    if not exists(filename):
        raise IOError(f"File {filename} does not exist")

    filetype = get_filetype(filename)

    if arg_count < 2:
        separator = input("Enter csv separator: ")
    else:
        separator = sys.argv[2]

    return FileInput(filename, filetype, separator)


def get_filetype(name: str) -> str:
    for file_type in filetypes:
        if name.lower().endswith(file_type):
            return file_type

    raise ValueError(f"File {name} has invalid type")


def parse_sqlite(filename: str) -> DataFrame:
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c = c.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
    results = c.fetchall()
    if len(results) == 0:
        conn.close()
        raise ValueError(f"{filename} has no table")
    elif len(results) == 2:
        conn.close()
        raise ValueError(f"{filename} has more than one table")

    # Get first column in first row
    table_name = results[0][0]
    conn = sqlite3.connect(filename)
    df = pd.read_sql(f"select * from {table_name}", con=conn)
    conn.close()
    return df


def parse_csv(filename: str, separator: str) -> DataFrame:
    return pd.read_csv(filename, delimiter=separator)


def parse_json(filename) -> DataFrame:
    return pd.read_json(filename, orient="records")


def main(test_files: bool = False):
    if test_files:
        os.chdir("exercise_test_cases")
        files = [FileInput(f, get_filetype(f), ",") for f in listdir() if isfile(f)]
    else:
        files = [validate_input()]

    for file in files:
        print(f"-------------- {file.filename} --------------")
        try:
            filename = file.filename
            filetype = file.filetype
            name = filename.removesuffix(filetype)

            target_folder = name
            if os.path.isdir(target_folder):
                shutil.rmtree(target_folder)

            print(f"Info: Creating dir {target_folder}")
            os.makedirs(f"{target_folder}")
            print(f"Info: Copy file {filename}")
            copyfile(filename, join(target_folder, filename))

            # Check and read Input
            print(f"Info: Reading {join(target_folder, filename)}")
            if filetype == ".csv" or filetype == ".txt":
                df = parse_csv(join(target_folder, filename), separator=file.separator)
            elif filetype == ".db":
                df = parse_sqlite(join(target_folder, filename))
            else:
                df = parse_json(join(target_folder, filename))

            # Write to output
            print("Info: Creating out directory")
            out_folder = join(target_folder, "out")
            os.makedirs(out_folder)
            output_filetypes = [x for x in filetypes if x != filetype]
            for filetype in output_filetypes:
                out_filename = join(out_folder, f"{name}{filetype}")
                print(f"Info: Creating file {name}{filetype}")
                if filetype == ".csv" or filetype == ".txt":
                    df.to_csv(out_filename, file.separator, index=False)
                elif filetype == ".db":
                    conn = sqlite3.connect(join(out_folder, f"{name}.db"))
                    df.to_sql(name=name, con=conn)
                    conn.close()
                else:
                    df.to_json(out_filename, orient="records")

            print(f"Info: Creating information.txt")
            with open(join(target_folder, "information.txt"), "w") as f:
                f.write(f"Input file type: {filetype}\n")
                f.write(f"Total row count: {len(df)}\n")
                f.write(f"Total column count: {len(df.columns)}\n")
                f.write(f"Columns: {list(df.columns)}\n")
                f.write(f"Output file types: {output_filetypes}")
        except (IOError, ValueError) as e:
            print(f"Error: {e}")
        except BaseException as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main(test_files=True)

