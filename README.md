# CHƯƠNG TRÌNH TẠO VÀ GIẢI MÃ HỆ MHK (MERKLE-HELLMAN KNAPSACK)

## 1. SETUP

- Tạo và setup venv:
  - Mở terminal, truy cập folder, chạy lệnh: python -m venv [your-venv-name]
  - Activate venv vừa tạo, sau đó chạy lệnh: python -m pip install -r requirements.txt

## 2. HƯỚNG DẪN SỬ DỤNG

### 2.1 Sử dụng thông thường

- Chạy chương trình: chạy file app.py

- Sử dụng:
  - Trường A: Nhập vector siêu tăng,
  - Trường u và M: Nhập số bất kỳ sao cho:
    - M: Lớn hơn 2 * A(max)
    - u: GCD(u, M) = 1

### 2.2 Chạy test cases

- Click vào chữ Test Cases ở nav bar (header), sau khi chuyển trang bấm nút Run test

- Chương trình có sẵn bộ 15 test cases được lưu ở file json trong tệp tests, kiểm tra các tình huống cơ bản (đọc file errors.py để tìm hiểu thêm).
