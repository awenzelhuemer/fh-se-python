import os
import pathlib
import sqlite3
from flask import Flask, render_template, request, redirect, send_from_directory
import pandas as pd
from pandas import DataFrame

app = Flask(__name__)

output_directory = "files"
filetypes = ('.csv', '.txt', '.json', '.db')


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
    return pd.read_csv(filename, delimiter=separator)


def parse_json(filename) -> DataFrame:
    return pd.read_json(filename, orient='records')


def parse_file(name: str, file_type: str) -> DataFrame:
    if file_type == '.csv' or file_type == '.txt':
        return parse_csv(name, separator=',')
    elif file_type == '.json':
        return parse_json(name)
    else:
        return parse_sqlite(name)


@app.route('/', methods=['GET'])
def get_files():
    files = [f for f in os.listdir(output_directory)]
    return render_template('index.html', files=files)


@app.route('/delete/<filename>', methods=['GET'])
def delete_file(filename: str):
    if os.path.exists(f"{output_directory}/{filename}"):
        os.remove(f"{output_directory}/{filename}")
    return redirect('/')


@app.route('/export/<filename>', methods=['POST'])
def export_file(filename: str):
    filename = os.path.join(output_directory, filename)
    filepath = pathlib.Path(filename)
    source_filetype = filepath.suffix
    df = parse_file(filename, source_filetype)
    if not os.path.exists('temp'):
        os.mkdir('temp')
    target_file_type = request.form['file_type']
    target_file_name = f"{filepath.stem}{target_file_type}"
    save_file(df, 'temp', target_file_name, target_file_type)
    return send_from_directory('temp', target_file_name)


@app.route('/details/<filename>', methods=['GET'])
def details(filename: str):
    full_filename = os.path.join(output_directory, filename)
    file_path = pathlib.Path(full_filename)
    df = parse_file(full_filename, file_path.suffix)
    return render_template('details.html', filename=filename, data_frame=df)


@app.route('/delete-col/<filename>/<index>', methods=['GET'])
def delete_col(filename: str, index: str):
    df = delete_col_or_row(filename, int(index), is_row=False)

    if df.empty:
        delete_file(filename)
        return redirect("/")

    return redirect(f'/details/{filename}')


@app.route('/delete-row/<filename>/<index>', methods=['GET'])
def delete_row(filename: str, index: str):
    df = delete_col_or_row(filename, int(index), is_row=True)

    if df.empty:
        delete_file(filename)
        return redirect("/")

    return redirect(f'/details/{filename}')


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

    save_file(df, output_directory, filename, file_type, table_name)

    return df


@app.route('/', methods=['POST'])
def add_file():
    file = request.files['file']
    filename = file.filename
    try:
        if filename == '':
            raise ValueError('No file specified')
        else:
            file_type = os.path.splitext(filename)[1]
            if file_type not in filetypes:
                raise ValueError(f'File {file.filename} has invalid type')
            file.save(file.filename)
        df = parse_file(filename, file_type)
        save_file(df, output_directory, filename, file_type)
    except ValueError as e:
        print(f'Error: {e}')
    except BaseException as e:
        print(f'Exception details: {e}')
    finally:
        # Cleanup uploaded file
        if os.path.exists(filename):
            os.remove(filename)

    return redirect('/')


def save_file(df: DataFrame, output_dir: str, filename: str, file_type: str, table_name: str = None):
    if file_type == '.csv' or file_type == '.txt':
        df.to_csv(os.path.join(output_dir, filename), index=False)
    elif file_type == '.json':
        df.to_json(os.path.join(output_dir, filename), orient="records")
    else:
        conn = sqlite3.connect(os.path.join(output_dir, filename))

        # Generate table name
        if table_name is None:
            table_name = filename.removesuffix(file_type)

        df.to_sql(table_name, con=conn, index=False, if_exists='replace')
        conn.close()


@app.route('/edit/<filename>/<row_index>/<column_index>', methods=['GET'])
def edit_entry(filename: str, row_index: str, column_index: str):
    full_filename = os.path.join(output_directory, filename)
    file_path = pathlib.Path(full_filename)
    df = parse_file(full_filename, file_path.suffix)

    value = df.iloc[int(row_index), int(column_index)]

    return render_template("edit.html", row_index=row_index, column_index=column_index, filename=filename, value=value)


@app.route('/edit/<filename>/<row_index>/<column_index>', methods=['POST'])
def update_entry(filename: str, row_index: str, column_index: str):
    update_entry(filename, row_index, column_index, request.form["value"])
    return redirect(f'/details/{filename}')


@app.route('/delete-value/<filename>/<row_index>/<column_index>', methods=['GET'])
def delete_entry(filename: str, row_index: str, column_index: str):
    set_entry(filename, row_index, column_index, "null")
    return redirect(f'/details/{filename}')


def set_entry(filename: str, row_index: str, column_index: str, value: str):
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

    save_file(df, output_directory, filename, file_type, table_name)


if __name__ == '__main__':
    app.run()
