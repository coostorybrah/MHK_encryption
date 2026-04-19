from flask import Blueprint, jsonify, current_app
import json

test_bp = Blueprint("test", __name__)


@test_bp.route("/api/run-tests", methods=["GET"])
def run_tests():
    try:
        with open("tests/test_cases.json", "r") as test_file:
            test_cases = json.load(test_file)

        client = current_app.test_client()
        results = []

        for test in test_cases:
            input_data = test["input"]
            expected = test["expected"]

            A = input_data["A"]
            u = input_data["u"]
            M = input_data["M"]
            P = input_data["plaintext"]

            expected_error = expected.get("error_code")

            # ===== STEP 1: Generate Key =====
            res_key = client.post("/api/generate-key", json={
                "A": A,
                "M": M,
                "u": u
            })

            if res_key.status_code != 200:
                actual_error = res_key.json.get("error_code")

                passed = (expected_error == actual_error)

                results.append(build_error_result(test, A, u, M, P, expected, actual_error, passed))
                continue

            S = res_key.json["public_key"]["S"]

            # ===== STEP 2: Encrypt =====
            res_enc = client.post("/api/encrypt", json={
                "S": S,
                "M": M,
                "P": P
            })

            if res_enc.status_code != 200:
                actual_error = res_enc.json.get("error_code")

                passed = (expected_error == actual_error)

                results.append(build_error_result(test, A, u, M, P, expected, actual_error, passed))
                continue

            bits = res_enc.json["bits"]
            C = res_enc.json["cipher"]

            # ===== STEP 3: Decrypt =====
            res_dec = client.post("/api/decrypt", json={
                "A": A,
                "u": u,
                "M": M,
                "C": C
            })

            if res_dec.status_code != 200:
                actual_error = res_dec.json.get("error_code")

                passed = (expected_error == actual_error)

                results.append(build_error_result(test, A, u, M, P, expected, actual_error, passed))
                continue

            text = res_dec.json["text"]

            # ===== SUCCESS CASE =====
            S_ok = (S == expected.get("S"))
            bits_ok = (bits == expected.get("bits"))
            cipher_ok = (C == expected.get("cipher"))
            text_ok = (text == expected.get("plaintext"))

            passed = (expected_error is None) and S_ok and bits_ok and cipher_ok and text_ok

            results.append({
                "id": test["id"],
                "name": test["name"],
                "passed": passed,

                "input": {
                    "A": A,
                    "u": u,
                    "M": M,
                    "plaintext": P
                },

                "checks": {
                    "S": S_ok,
                    "bits": bits_ok,
                    "cipher": cipher_ok,
                    "plaintext": text_ok
                },

                "expected": expected,
                "actual": {
                    "S": S,
                    "bits": bits,
                    "cipher": C,
                    "plaintext": text
                }
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===== HELPER =====
def build_error_result(test, A, u, M, P, expected, actual_error, passed):
    return {
        "id": test["id"],
        "name": test["name"],
        "passed": passed,

        "input": {
            "A": A,
            "u": u,
            "M": M,
            "plaintext": P
        },

        "checks": {
            "S": False,
            "bits": False,
            "cipher": False,
            "plaintext": False
        },

        "expected": expected,

        "actual": {
            "S": [],
            "bits": [],
            "cipher": [],
            "plaintext": "",
            "error_code": actual_error
        }
    }