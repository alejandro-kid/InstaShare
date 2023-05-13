upload_file_schema = {
    "type": "object",
    "properties": {
        "file": {
            "type": "string",
            "contentEncoding": "base64"
        },
        "file_name": {
            "type": "string",
            "pattern": r"[A-Za-z0-9]{1,}\.[A-Za-z0-9]{1,4}"
        },
        "user_id": {
            "type": "string",
            "format": "uuid"
        }
    },
    "required": ["file", "file_name", "user_id"]
}
