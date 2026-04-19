from flask import Blueprint, request, jsonify
from logic import *
from errors import error_response

encrypt_bp = Blueprint("encrypt", __name__)


@encrypt_bp.route("/api/encrypt", methods=["POST"])
def encrypt():
    try:
        data = request.json

        S = data.get("S")
        M = data.get("M")
        P = data.get("P")

        # ===== Validation =====
        if S is None or M is None or P is None:
            return jsonify(error_response("EMPTY_INPUT")), 400

        if not isinstance(S, list) or len(S) == 0:
            return jsonify(error_response("EMPTY_INPUT")), 400

        if not all(isinstance(x, int) for x in S):
            return jsonify(error_response("INVALID_CHARACTER")), 400

        if not isinstance(M, int) or M <= 0:
            return jsonify(error_response("INVALID_MODULUS")), 400

        if not isinstance(P, str):
            return jsonify(error_response("INVALID_CHARACTER")), 400

        # ===== Handle empty plaintext =====
        if P.strip() == "":
            return jsonify({
                "bits": [],
                "cipher": []
            })

        # ===== Convert text → bits =====
        try:
            bits = text_to_5bit_list(P)
        except Exception:
            return jsonify(error_response("INVALID_CHARACTER")), 400

        # ===== Encrypt =====
        try:
            C = ma_hoa_ban_ro_5bit(bits, S, M)
        except Exception:
            return jsonify(error_response("INVALID_MODULUS")), 400

        return jsonify({
            "bits": bits,
            "cipher": C
        })

    except Exception:
        return jsonify(error_response("EMPTY_INPUT")), 500