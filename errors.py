ERRORS = {
    "INVALID_CHARACTER": "Chỉ hỗ trợ 26 chữ cái tiếng Anh A-Z",
    "INVALID_SUPERINCREASING": "A không phải dãy siêu tăng",
    "INVALID_MODULUS": "M phải > 2 * A[n]",
    "NOT_COPRIME": "u và M phải nguyên tố cùng nhau",
    "EMPTY_INPUT": "Dữ liệu đầu vào rỗng"
}

def error_response(code):
    return {
        "error_code": code,
        "message": ERRORS[code]
    }