import json
from datetime import datetime, date


class FileInfo:
    def __init__(self, name, size, upload_date):
        self.name = name
        self.size = size
        self.upload_date = upload_date


class FileEncoder(json.JSONEncoder):
    def default(self, file_info):
        if isinstance(file_info, FileInfo):
            return {"__class__": "FileInfo", "name": file_info.name, "size": file_info.size,
                    "upload_date": file_info.upload_date}
        elif isinstance(file_info, (datetime, date)):
            return file_info.isoformat()
        else:
            return super().default(file_info)


def decode_file_info(json_file):
    if json_file["__class__"] == "FileInfo":
        return FileInfo(json_file["name"], json_file["size"], json_file["upload_date"])
    return json_file
