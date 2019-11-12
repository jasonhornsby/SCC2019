from datetime import datetime
import json

from flask import Flask

from FileUtils import FileEncoder, FileInfo

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


def encode_file_info(files):
    return json.dumps(files, cls=FileEncoder)


# TODO get files from database
def get_files_from_db():
    file_list = [FileInfo("f1", 10, datetime(2014, 4, 21, 12, 24, 32)),
                 FileInfo("f2", 100, datetime(2016, 10, 1, 14, 1)),
                 FileInfo("f3", 114450, datetime(2017, 4, 21, 12, 24, 32))]
    return file_list


@app.route("/files", methods=("GET",))
def get_files():
    # get files from database
    files = get_files_from_db()
    # encode files info
    files_info = encode_file_info(files)
    return files_info


if __name__ == '__main__':
    app.run()
