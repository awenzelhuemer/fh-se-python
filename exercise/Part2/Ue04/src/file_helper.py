import os
import pathlib
import sqlite3

import pandas as pd
from pandas import DataFrame

output_directory = "uploaded_files"
filetypes = ('.csv', '.txt', '.json', '.db')


def remove_file(filename):
    full_filename = os.path.join(output_directory, filename)
    remove_fileinfo_entry(filename)
    if os.path.exists(full_filename):
        os.remove(full_filename)


def get_dataframe(filename):
    full_filename = os.path.join(output_directory, filename)
    file_path = pathlib.Path(full_filename)
    return parse_file(full_filename, file_path.suffix)


def save_file(df: DataFrame, filename: str, file_type: str, table_name: str = None, target_directory: str = None):

    if target_directory is None:
        target_directory = output_directory

    if not os.path.exists(target_directory):
        os.mkdir(target_directory)

    if file_type == '.csv' or file_type == '.txt':
        df.to_csv(os.path.join(target_directory, filename), index=False)
    elif file_type == '.json':
        df.to_json(os.path.join(target_directory, filename), orient="records")
    else:
        conn = sqlite3.connect(os.path.join(target_directory, filename))

        # Generate table name
        if table_name is None:
            table_name = filename.removesuffix(file_type)

        df.to_sql(table_name, con=conn, index=False, if_exists='replace')
        conn.close()


def get_sqlite_table_name(filename, conn) -> str:
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
    return results[0][0]


def parse_sqlite(filename: str) -> DataFrame:
    conn = sqlite3.connect(filename)
    table_name = get_sqlite_table_name(filename, conn)

    df = pd.read_sql(f"select * from {table_name}", con=conn)
    conn.close()
    return df


def parse_csv(filename: str, separator: str) -> DataFrame:
    return pd.read_csv(filename, encoding="latin-1", delimiter=separator)


def parse_json(filename) -> DataFrame:
    return pd.read_json(filename, encoding="latin-1", orient='records')


def parse_file(name: str, file_type: str) -> DataFrame:
    if not os.path.isfile(name):
        raise ValueError('File does not exist')

    if file_type == '.csv' or file_type == '.txt':
        return parse_csv(name, separator=',')
    elif file_type == '.json':
        return parse_json(name)
    else:
        return parse_sqlite(name)


def add_fileinfo_entry(name: str, url=None, languages=None, repositories=None, members=None):
    conn = sqlite3.connect('fileinfo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files (
        name text,
        url text,
        languages text,
        repository_count decimal,
        member_count decimal)''')

    c.execute('''INSERT INTO files (name, url, languages, repository_count, member_count)
                            VALUES(?,?,?,?,?)''', [name, url, languages, repositories, members])

    conn.commit()
    c.close()


def get_fileinfos():
    conn = sqlite3.connect('fileinfo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files (
            name text,
            url text,
            languages text,
            repository_count decimal,
            member_count decimal)''')
    c.execute('''SELECT * FROM files''')
    results = c.fetchall()
    c.close()
    return results


def remove_fileinfo_entry(name: str):
    conn = sqlite3.connect('fileinfo.db')
    c = conn.cursor()
    c.execute('''DELETE FROM files WHERE name = ?''', [name])
    conn.commit()
    c.close()


def get_cell_value(filename: str, row_index: int, column_index: int):
    full_filename = os.path.join(output_directory, filename)
    file_path = pathlib.Path(full_filename)
    df = parse_file(full_filename, file_path.suffix)

    return df.iloc[row_index, column_index]


def update_cell_value(filename: str, row_index: int, column_index: int, value: str | None):
    full_filename = os.path.join(output_directory, filename)
    file_path = pathlib.Path(full_filename)
    file_type = file_path.suffix
    df = parse_file(full_filename, file_path.suffix)

    df.iloc[int(row_index), int(column_index)] = value

    if file_type == '.db':
        conn = sqlite3.connect(full_filename)
        table_name = get_sqlite_table_name(full_filename, conn)
        conn.close()
    else:
        table_name = None

    save_file(df, filename, file_type, table_name)


def delete_col_or_row(filename: str, index: int, is_row: bool):
    full_filename = os.path.join(output_directory, filename)
    file_path = pathlib.Path(full_filename)
    file_type = file_path.suffix
    df = parse_file(full_filename, file_path.suffix)

    if is_row:
        df.drop([index], inplace=True)
    else:
        df.drop(df.columns[index], axis=1, inplace=True)

    # Get table name if necessary
    if file_type == '.db':
        conn = sqlite3.connect(full_filename)
        table_name = get_sqlite_table_name(full_filename, conn)
        conn.close()
    else:
        table_name = None

    save_file(df, filename, file_type, table_name)

    return df
