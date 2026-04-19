from flask import Blueprint, request, jsonify
from logic import *
import math
from errors import error_response

decrypt_bp = Blueprint("decrypt", __name__)


@decrypt_bp.route("/api/decrypt", methods=["POST"])
def decrypt():
    try:
        data = request.json

        A = data.get("A")
        u = data.get("u")
        M = data.get("M")
        C = data.get("C")

        # ===== Validation =====
        if A is None or u is None or M is None or C is None:
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

        if not isinstance(u, int) or math.gcd(u, M) != 1:
            return jsonify(error_response("NOT_COPRIME")), 400

        if not isinstance(C, list):
            return jsonify(error_response("INVALID_CHARACTER")), 400

        # ===== Empty cipher =====
        if len(C) == 0:
            return jsonify({
                "c_phay": [],
                "bits": [],
                "text": ""
            })

        # ===== Decrypt =====
        try:
            u_inv = pow(u, -1, M)
            c_phay = tinh_c_phay(C, u_inv, M)
            bits = giai_ma(c_phay, A)
            text = bit5_list_to_text(bits)
        except Exception:
            return jsonify(error_response("INVALID_MODULUS")), 400

        return jsonify({
            "c_phay": c_phay,
            "bits": bits,
            "text": text
        })

    except Exception:
        return jsonify(error_response("EMPTY_INPUT")), 500