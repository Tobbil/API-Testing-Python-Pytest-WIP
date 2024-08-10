# API Testing with Python and Pytest

This repository is a work-in-progress (WIP) project focused on testing APIs using Python and Pytest. It contains examples of automated tests for RESTful APIs.

## Project Structure

```plaintext
api-testing-python-pytest/
│
├── config/                       # Configuration files
├── helpers/                      # Utility functions for making API requests, assertions, etc.
├── tests/                        # Example test cases
│   └── test_general_api.py       # General API tests
│   └── test_objects_endpoints.py # Test cases for the /objects endpoint
├── conftest.py                   # Global test fixtures and configurations
├── pytest.ini                    # Pytest configuration
├── README.md                     # Project documentation
├── requirements.txt              # List of project requirements
└── test_results.log              # Example of custom logging
