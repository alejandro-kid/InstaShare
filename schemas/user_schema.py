register_user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minimum": 8,
        },
        "email": {
            "type": "string",
            "format": "email"
            },
        "password": {
            "type": "string",
            "minimum": 8,
            },
    },
    "requiered": ["name", "email", "password"]
}

login_user_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
            },
        "password": {
            "type": "string"
            },
    },
    "requiered": ["email", "password"]
}
