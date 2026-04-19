from flask import Blueprint, request, jsonify
from logic import *
import math
from errors import error_response

key_bp = Blueprint("key", __name__)


@key_bp.route("/api/generate-key", methods=["POST"])
def generate_key():
    try:
        data = request.json

        A = data.get("A")
        M = data.get("M")
        u = data.get("u")

        # ===== Validation =====
        if A is None or M is None or u is None:
            return jsonify(error_response("EMPTY_INPUT")), 400

        if not isinstance(A, list) or len(A) == 0:
            return jsonify(error_response("EMPTY_INPUT")), 400

        if not all(isinstance(x, int) for x in A):
            return jsonify(error_response("INVALID_CHARACTER")), 400

        if not all_elements_are_positive(A):
            return jsonify(error_response("INVALID_CHARACTER")), 400

        if not is_superincreasing(A):
            return jsonify(error_response("INVALID_SUPERINCREASING")), 400

        if not isinstance(M, int) or M <= 0:
            return jsonify(error_response("INVALID_MODULUS")), 400

        if M <= 2 * A[-1]:
            return jsonify(error_response("INVALID_MODULUS")), 400

        if not isinstance(u, int) or math.gcd(u, M) != 1:
            return jsonify(error_response("NOT_COPRIME")), 400

        # ===== Generate key =====
        A.sort()
        S = tinh_vector_s(A, M, u)

        return jsonify({
            "public_key": {
                "S": S,
                "M": M
            },
            "private_key": {
                "A": A,
                "u": u
            }
        })

    except Exception:
        return jsonify(error_response("EMPTY_INPUT")), 500