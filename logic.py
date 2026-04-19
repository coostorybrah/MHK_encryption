def string_to_list_of_int(raw_text: str) -> list[int]:
	"""Chuyen chuoi phan cach boi dau phay thanh list so nguyen.

	Vi du: "1, 2, 3" -> [1, 2, 3]
	"""
	if raw_text is None:
		return []

	parts = [item.strip() for item in raw_text.split(",")]
	return [int(item) for item in parts if item]


def list_of_ints_to_string(values: list[int]) -> str:
	"""Chuyen list so nguyen thanh chuoi phan cach boi dau phay.

	Vi du: [1, 2, 3] -> "1, 2, 3"
	"""
	return ", ".join(str(value) for value in values)


def text_to_5bit_list(text: str) -> list[int]:
	"""Chuyen chuoi chi gom A-Z thanh danh sach bit 0/1 (moi ky tu 5 bit).

	Quy uoc: A -> 00000, B -> 00001, ..., Z -> 11001
	"""
	if text is None:
		return []

	clean_text = text.strip().upper()
	if not clean_text:
		return []

	bits: list[int] = []
	for ch in clean_text:
		if ch < "A" or ch > "Z":
			raise ValueError("Chi ho tro 26 chu cai tieng Anh A-Z")

		value = ord(ch) - ord("A")
		chunk = f"{value:05b}"
		bits.extend(int(bit) for bit in chunk)

	return bits


def bit5_list_to_text(bits: list[int]) -> str:
	"""Chuyen danh sach bit 0/1 (block 5 bit) thanh chuoi A-Z."""
	if bits is None:
		return ""

	if not bits:
		return ""

	if len(bits) % 5 != 0:
		raise ValueError("So luong bit phai chia het cho 5")

	chars: list[str] = []
	for i in range(0, len(bits), 5):
		chunk = bits[i:i + 5]
		if any(bit not in (0, 1) for bit in chunk):
			raise ValueError("Danh sach bit chi duoc chua 0 va 1")

		value = int("".join(str(bit) for bit in chunk), 2)
		if value < 0 or value > 25:
			raise ValueError("Gia tri 5 bit ngoai pham vi A-Z")

		chars.append(chr(ord("A") + value))

	return "".join(chars)


def ma_hoa_ban_ro_5bit(bits: list[int], s: list[int], m: int) -> list[int]:
	"""Ma hoa truc tiep tu bits list 0/1 theo khoa cong khai S va modulo M."""
	if not s:
		raise ValueError("Vector S rong")
	if m <= 0:
		raise ValueError("M phai > 0")
	if not bits:
		raise ValueError("Bits list rong")
	if any(bit not in (0, 1) for bit in bits):
		raise ValueError("Bits list chi duoc chua 0 va 1")

	n = len(s)
	if len(bits) % n != 0:
		raise ValueError("Do dai bit cua P khong chia het cho do dai S")

	cipher_list: list[int] = []
	for i in range(0, len(bits), n):
		block = bits[i:i + n]
		c = sum(si * xi for si, xi in zip(s, block)) % m
		cipher_list.append(c)

	return cipher_list


def tinh_c_phay(c_list: list[int], u_inv: int, m: int) -> list[int]:
	"""Tinh danh sach C' tu C voi u^-1 da co san.

	Cong thuc: c'_i = (c_i * u^-1) mod m
	"""
	if m <= 0:
		raise ValueError("M phai > 0")
	if not c_list:
		raise ValueError("C rong")

	return [(c * u_inv) % m for c in c_list]


def giai_ma(c_phay_list: list[int], a: list[int]) -> list[int]:
	"""Giai ma tu danh sach C' ve danh sach bits 0/1 bang day sieu tang A'."""
	if not a:
		raise ValueError("A rong")
	if not c_phay_list:
		raise ValueError("C' rong")
	
	n = len(a)
	bits: list[int] = []

	for c_phay in c_phay_list:
		if c_phay < 0:
			raise ValueError("C' phai la so khong am")

		remain = c_phay
		block = [0] * n

		for i in range(n - 1, -1, -1):
			if a[i] <= remain:
				block[i] = 1
				remain -= a[i]

		if remain != 0:
			raise ValueError("Khong giai duoc C' voi day A da cho")

		bits.extend(block)

	return bits


def tinh_vector_s(a: list[int], m: int, u: int) -> list[int]:
	"""Tinh vector S theo cong thuc: s_i = (a_i * u) mod m."""
	return [(ai * u) % m for ai in a]


def is_superincreasing(a: list[int]) -> bool:
	"""Kiem tra day sieu tang: moi phan tu lon hon tong cac phan tu truoc do."""
	total = 0
	for value in a:
		if value <= total:
			return False
		total += value
	return True

def all_elements_are_positive(a: list[int]) -> bool:
    for value in a:
        if value <= 0:
            return False
    return True