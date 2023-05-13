upload_file_schema = {
    "type": "object",
    "properties": {
        "file": {
            "type": "string",
            "contentEncoding": "base64"
        },
        "filename": {
            "type": "string",
            "pattern": "[A-Za-z0-9]{1,}$+\.[A-Za-z0-9]{1,4}$"
        },
        "user_id": {
            "type": "string",
            "format": "uuid"
        }
    },
    "required": ["file", "filename", "user_id"]
}
