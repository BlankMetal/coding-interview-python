#!/usr/bin/env python3
"""
API-driven test runner for coding interview challenges.
Fetches test cases from API, runs solution, and validates results.
"""

import sys
import requests
from solution import solve, CHALLENGE_LEVEL, SCENARIO_NAME
from config import API_BASE_URL

# Health check endpoint (hardcoded)
HEALTH_CHECK_URL = "https://simple-connectivity-check.vercel.app/"


def perform_health_check():
    """Perform health check to verify connectivity to Vercel backend."""
    try:
        response = requests.get(HEALTH_CHECK_URL, timeout=10)
        response.raise_for_status()
        response_text = response.text
        
        if "Healthy" in response_text:
            print("✓ Health check successful\n")
            return True
        else:
            print("✗ Health check failed: Unexpected response from server\n")
            return False
    except requests.exceptions.RequestException as e:
        print("✗ Error connecting to Vercel servers.")
        print("Please debug any reason why .vercel.app domains can't be hit,")
        print("and if you are sure it's not your machine reach out to your recruiter.\n")
        print(f"Technical details: {e}\n")
        return False


def fetch_test_cases(challenge_level, scenario_name):
    """Fetch test cases from API."""
    try:
        url = f"{API_BASE_URL}/test-cases"
        params = {
            "challenge_level": challenge_level,
            "scenario_name": scenario_name
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching test cases: {e}")
        sys.exit(1)


def submit_results(results, challenge_level, scenario_name):
    """Submit results to API for validation."""
    try:
        url = f"{API_BASE_URL}/check-results"
        payload = {
            "results": results,
            "challenge_level": challenge_level,
            "scenario_name": scenario_name
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error submitting results: {e}")
        sys.exit(1)


def main():
    print(f"=== Coding Interview Challenge ===")
    print(f"Current Level: {CHALLENGE_LEVEL}")
    print(f"Scenario: {SCENARIO_NAME}\n")
    
    # Perform health check
    perform_health_check()

    test_cases = fetch_test_cases(CHALLENGE_LEVEL, SCENARIO_NAME)

    if not test_cases or len(test_cases) == 0:
        print("No test cases found.")
        return

    print(f"Running {len(test_cases)} test(s)...\n")

    results = []
    for i, test_case in enumerate(test_cases, 1):
        try:
            result = solve(*test_case)
            results.append(result)
        except Exception as e:
            print(f"Error running test {i}: {e}")
            results.append(None)

    validation = submit_results(results, CHALLENGE_LEVEL, SCENARIO_NAME)

    if 'results' in validation:
        for test_result in validation['results']:
            test_num = test_result.get('testCase', test_result.get('test_id', '?'))
            passed = test_result.get('passed', False)
            status = "PASS" if passed else "FAIL"

            print(f"Test #{test_num}: {status}")

            if 'level' in test_result:
                print(f"  Level: {test_result['level']}")

            expected = test_result.get('expected', '?')
            received = test_result.get('received', test_result.get('actual', '?'))

            print(f"  Expected: {expected}")
            print(f"  Received: {received}")
            print()

    if 'summary' in validation:
        summary = validation['summary']
        total = summary.get('total', len(test_cases))
        passed = summary.get('passed', 0)
        failed = summary.get('failed', 0)

        print("=" * 50)
        print(f"Results: {passed} passed, {failed} failed out of {total} total")
        print("=" * 50)

        if failed == 0:
            print("\n✓ All tests passed! Ready to advance to the next level.")
        else:
            print(f"\n✗ {failed} test(s) failed. Please fix and try again.")
    else:
        print("Results submitted successfully.")


if __name__ == "__main__":
    main()
