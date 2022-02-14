import os
import pathlib

from flask import Flask, render_template, request, redirect, send_from_directory
import pandas as pd

import file_helper
import github_helper

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_files():
    files = file_helper.get_fileinfos()
    return render_template('index.html', files=files)


@app.route('/delete/<filename>', methods=['GET'])
def delete_file(filename: str):
    file_helper.remove_file(filename)
    return redirect('/')


@app.route('/export/<filename>', methods=['POST'])
def export_file(filename: str):
    filename = os.path.join(file_helper.output_directory, filename)
    filepath = pathlib.Path(filename)
    source_filetype = filepath.suffix
    df = file_helper.parse_file(filename, source_filetype)
    target_file_type = request.form['file_type']
    target_file_name = f"{filepath.stem}{target_file_type}"
    file_helper.save_file(df, target_file_name, target_file_type, target_directory='temp')
    return send_from_directory('temp', target_file_name)


@app.route('/github-url', methods=['POST'])
def add_url():
    try:
        url = request.form['url']
        # Validate url
        if github_helper.is_valid_github_url(url):
            # Extract data
            data = github_helper.extract_github_data(url)
            title = data["title"]
            members = data["member_count"]
            languages = data["languages"]
            repositories = data["repositories"]

            # Create file
            df = pd.DataFrame(repositories)
            file_helper.save_file(df, f"{title}.csv", ".csv", None)
            file_helper.add_fileinfo_entry(f"{title}.csv", url, ', '.join(languages), len(repositories), members)
        else:
            raise ValueError('Url is invalid')
    except BaseException as e:
        print("Error: ", e)

    return redirect('/')


@app.route('/details/<filename>', methods=['GET'])
def get_file(filename: str):
    try:
        return render_template('details.html', filename=filename, data_frame=file_helper.get_dataframe(filename))
    except BaseException as e:
        print("Error: ", e)
        return redirect("/")


@app.route('/delete-col/<filename>/<index>', methods=['GET'])
def delete_col(filename: str, index: str):
    df = file_helper.delete_col_or_row(filename, int(index), is_row=False)

    if df.empty:
        delete_file(filename)
        return redirect("/")

    return redirect(f'/details/{filename}')


@app.route('/delete-row/<filename>/<index>', methods=['GET'])
def delete_row(filename: str, index: str):
    df = file_helper.delete_col_or_row(filename, int(index), is_row=True)

    if df.empty:
        delete_file(filename)
        return redirect("/")

    return redirect(f'/details/{filename}')


@app.route('/', methods=['POST'])
def add_file():
    file = request.files['file']
    filename = file.filename
    try:
        if filename == '':
            raise ValueError('No file specified')
        else:
            file_type = os.path.splitext(filename)[1]
            if file_type not in file_helper.filetypes:
                raise ValueError(f'File {file.filename} has invalid type')
            file.save(file.filename)
        df = file_helper.parse_file(filename, file_type)
        file_helper.save_file(df, filename, file_type)
        file_helper.add_fileinfo_entry(filename)
    except ValueError as e:
        print(f'Error: {e}')
    except BaseException as e:
        print(f'Exception details: {e}')
    finally:
        # Cleanup uploaded file
        if os.path.exists(filename):
            os.remove(filename)
    return redirect('/')


@app.route('/edit/<filename>/<row_index>/<column_index>', methods=['GET'])
def edit_entry(filename: str, row_index: str, column_index: str):
    value = file_helper.get_cell_value(filename, int(row_index), int(column_index))
    return render_template("edit.html", row_index=row_index, column_index=column_index, filename=filename, value=value)


@app.route('/edit/<filename>/<row_index>/<column_index>', methods=['POST'])
def update_entry(filename: str, row_index: str, column_index: str):
    file_helper.update_cell_value(filename, int(row_index), int(column_index), request.form["value"])
    return redirect(f'/details/{filename}')


@app.route('/delete/<filename>/<row_index>/<column_index>', methods=['GET'])
def delete_entry(filename: str, row_index: str, column_index: str):
    file_helper.update_cell_value(filename, int(row_index), int(column_index), None)
    return redirect(f'/details/{filename}')


if __name__ == '__main__':
    app.run()
