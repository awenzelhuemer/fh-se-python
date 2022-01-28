import os
import pathlib
import sqlite3
from flask import Flask, render_template, request, redirect, send_from_directory
import pandas as pd
from pandas import DataFrame

app = Flask(__name__)

output_directory = "files"
filetypes = ('.csv', '.txt', '.json', '.db')


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


def parse_file(name: str, file_type) -> DataFrame:
    if file_type == '.csv' or file_type == '.txt':
        return parse_csv(name, separator=',')
    elif file_type == '.json':
        return parse_json(name)
    else:
        return parse_sqlite(name, name.removesuffix(file_type))


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
    source_file_name = os.path.join(output_directory, filename)
    file_path = pathlib.Path(source_file_name)
    source_file_type = file_path.suffix
    df = parse_file(source_file_name, source_file_type)
    if not os.path.exists('temp'):
        os.mkdir('temp')
    target_file_type = request.form['file_type']
    target_file_name = f"{file_path.stem}{target_file_type}"
    save_file(df, 'temp', target_file_name, target_file_type)
    return send_from_directory('temp', target_file_name)


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


def save_file(df: DataFrame, output_dir: str, filename: str, file_type: str):
    if file_type == '.csv' or file_type == '.txt':
        df.to_csv(f"{output_dir}/{filename}")
    elif file_type == '.json':
        df.to_json(f"{output_dir}/{filename}")
    else:
        conn = sqlite3.connect(f'{output_dir}/{filename}')
        df.to_sql(filename.removesuffix(file_type), con=conn)


if __name__ == '__main__':
    app.run()
