
SCHEMA = {

    "root": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {
                    "required": False,
                    "type": "string"
                },
                "target": {
                    "required": False,
                    "type": "string"
                },
                "start": {
                    "required": False,
                    "type": "string"
                },
                "steps": {
                    "type": "list",
                    "anyof_schema": [
                        {
                            "type": "dict",
                            "keyschema": {
                                "type": "string", "allowed": ['north', 'south', 'east', 'west', 'forward', 'right']
                            },
                            "valueschema": {"type": "integer", "nullable": True}
                        },
                        {
                            "type": "dict",
                            "schema": {
                                "reach": {
                                    "type": "string"
                                }
                            }
                        },
                    ]
                }

            }

        }
    }

}
