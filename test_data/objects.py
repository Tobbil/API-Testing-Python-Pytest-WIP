class TestObjects:
    OBJECT_VALID = {
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB",
        },
    }
    OBJECT_VALID_PUT = {
        "name": "Lenovo",
        "data": {
            "year": 2024,
            "price": 2500.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB",
        },
    }
    OBJECT_VERY_LARGE_PAYLOAD = {
        "data": "A" * 100000,
    }
