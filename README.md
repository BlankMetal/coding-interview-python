# Coding Interview Python - API-Driven Test Framework

API-driven test framework for coding interview challenges. This framework fetches test cases from an API, runs your solution, and validates results automatically.

## Overview

This framework is designed for coding interviews where:
- Test cases are served dynamically via API
- Solutions are validated against backend-computed expected results
- Candidates focus on implementing logic without managing test data

## Requirements

- Python 3.12 or higher
- Backend API running (default: `http://localhost:3001`)

## Setup

### Using uv (recommended)

```bash
uv sync
```

### Using pip

```bash
pip install -e .
```

## Usage

### 1. Configure Your Challenge

Edit [solution.py](solution.py) to set your challenge level and scenario:

```python
CHALLENGE_LEVEL = 1
SCENARIO_NAME = "ticket_pricing"
```

### 2. Implement Your Solution

Write your solution in the `solve()` function in [solution.py](solution.py):

```python
def solve(*params):
    # Your implementation here
    # params is a list of test case parameters
    return result
```

### 3. Run Tests

```bash
# With uv
uv run python run_tests_api.py

# With Python directly
python run_tests_api.py
```

### Health Check

When you run the test framework, it will automatically perform a health check to verify connectivity to the Vercel backend servers. You should see:

```
✓ Health check successful
```

If you see an error message instead, please debug any connectivity issues with `.vercel.app` domains. If you're certain it's not your machine, reach out to your recruiter.

## Configuration

### API Base URL

Set via environment variable:

```bash
export API_BASE_URL=http://localhost:3001
python run_tests_api.py
```

Or edit [config.py](config.py) directly.

## API Requirements

The framework expects the following API endpoints:

### GET /test-cases

Fetch test cases for a specific challenge level and scenario.

**Query Parameters:**
- `challenge_level` (int): The challenge difficulty level
- `scenario_name` (str): The name of the scenario

**Response:**
```json
[
  [5, 3, 2, "2025-01-01", "2024-12-01", "[]", ""],
  [10, -5, 0, "", "", "", ""],
  ...
]
```

Each test case is an array of parameters (integers, strings, etc.).

### POST /check-results

Submit results for validation.

**Request Body:**
```json
{
  "results": [8, 5, 0, 10, ...],
  "challenge_level": 1,
  "scenario_name": "ticket_pricing"
}
```

**Response:**
```json
{
  "results": [
    {
      "testCase": 1,
      "level": 1,
      "passed": true,
      "expected": 8,
      "received": 8
    },
    ...
  ],
  "summary": {
    "total": 10,
    "passed": 9,
    "failed": 1
  }
}
```

## Output Example

```
=== Coding Interview Challenge ===
Current Level: 1
Scenario: ticket_pricing

✓ Health check successful

Running 10 test(s)...

Test #1: PASS
  Level: 1
  Expected: 8
  Received: 8

Test #2: FAIL
  Level: 1
  Expected: 5
  Received: 6

==================================================
Results: 9 passed, 1 failed out of 10 total
==================================================

✗ 1 test(s) failed. Please fix and try again.
```

## Project Structure

- [solution.py](solution.py) - Your solution implementation
- [run_tests_api.py](run_tests_api.py) - Test runner (do not modify)
- [config.py](config.py) - API configuration
- [pyproject.toml](pyproject.toml) - Python project configuration

## License

MIT
