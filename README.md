<div align="center">

# 🌐 Cứu Map Mini  
### Hệ thống bản đồ cứu trợ Việt Nam – *Cuutoi.vn Prototype*

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-orange?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-embedded-blue?logo=sqlite)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)

---

</div>

> **Cứu Map Mini** là ứng dụng bản đồ cứu trợ cộng đồng giúp người dân và Mạnh Thường Quân kết nối trong tình huống thiên tai.  
> Ứng dụng sử dụng **Flask + Leaflet + SQLite**, hoạt động ổn định ngay cả trong mạng yếu và có thể chạy độc lập trên Linux hoặc Docker.

---

## 🚀 Tính năng nổi bật

✅ Hiển thị bản đồ cứu trợ theo thời gian thực  
✅ Gửi yêu cầu cứu hộ nhanh (với định vị GPS tự động)  
✅ Mạnh Thường Quân chia sẻ **Live Location** và trạng thái hoạt động  
✅ Tự động ngắt chia sẻ sau **3 giờ** hoặc khi dừng thủ công  
✅ Dữ liệu được xóa tự động sau **7 ngày**  
✅ Hoạt động mượt mà trên mobile và desktop  
✅ Triển khai cực nhanh bằng Docker 🐳  

---

## ⚙️ Cài đặt & Chạy thử

### ▶️ Chạy trực tiếp (Local)
```bash
pip install -r requirements.txt
python app.py
```

Mở trình duyệt: 👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 🐋 Chạy bằng Docker
```bash
# Build image
docker build -t cuutoi-map .

# Run container
docker run -d -p 8000:8000 cuutoi-map
```

Mở trình duyệt: 👉 [http://localhost:8000](http://localhost:8000)

Nếu muốn giữ lại DB giữa các lần chạy:
```bash
docker run -d -p 8000:8000 \
  -v $(pwd)/cuutoi.db:/app/cuutoi.db \
  cuutoi-map
```

---

## 🌐 Danh sách API (REST)

|  #  | Endpoint           | Method   | Mô tả                               |
| :-: | ------------------ | -------- | ----------------------------------- |
|  1  | `/api/points`      | **GET**  | Lấy danh sách toàn bộ điểm cứu trợ  |
|  2  | `/api/points`      | **POST** | Thêm điểm mới (`help` hoặc `donor`) |
|  3  | `/api/live_update` | **POST** | Cập nhật vị trí live của donor      |
|  4  | `/api/live_donors` | **GET**  | Lấy danh sách donor đang online     |
|  5  | `/api/stop_live`   | **POST** | Dừng chia sẻ vị trí trực tiếp       |

---

### 🧠 Ví dụ Request / Response

#### ➤ Thêm điểm cứu trợ
```bash
POST /api/points
```
```json
{
  "lat": 16.0471,
  "lon": 108.2068,
  "note": "Ngập tầng 2, cần thuyền gấp",
  "phone": "0905123456",
  "address": "Đà Nẵng",
  "type": "help"
}
```

**Phản hồi:**
```json
{"ok": true}
```

---

#### ➤ Cập nhật vị trí live
```bash
POST /api/live_update
```
```json
{
  "phone": "0909777788",
  "lat": 16.0610,
  "lon": 108.2130
}
```

**Phản hồi:**
```json
{"ok": true}
```

---

#### ➤ Lấy danh sách donor online
```bash
GET /api/live_donors
```
```json
[
  {
    "name": "Anh Lâm",
    "phone": "0909777788",
    "lat": 16.0600,
    "lon": 108.2100,
    "address": "Hải Châu, Đà Nẵng"
  }
]
```

---

## 📱 Giao diện người dùng

| Vai trò              | Mô tả                          | Màu marker |
| -------------------- | ------------------------------ | ---------- |
| 🆘 Người cần cứu trợ | Gửi yêu cầu + vị trí khẩn cấp  | 🔴 Đỏ      |
| 💚 Mạnh Thường Quân  | Chia sẻ vị trí & hỗ trợ cứu hộ | 🟢 Xanh    |
| 💤 Donor tạm nghỉ    | Ngắt kết nối / hết thời hạn    | ⚪ Xám      |

---

## 🧩 Công nghệ sử dụng

| Thành phần            | Mô tả                                                    |
| --------------------- | -------------------------------------------------------- |
| **Flask**             | Web backend siêu gọn chạy trên Python                    |
| **Leaflet.js**        | Thư viện bản đồ mã nguồn mở, nhẹ, dễ tùy biến            |
| **SQLite**            | Cơ sở dữ liệu nhúng, chạy nhanh trên ext4                |
| **OpenStreetMap CDN** | Cung cấp tile bản đồ miễn phí, không cần API key         |
| **Docker**            | Dễ triển khai, đóng gói, chạy được trên mọi hệ điều hành |

---

## 🧭 Ghi chú kỹ thuật

* Dữ liệu lưu cục bộ bằng **SQLite**, hoạt động tốt khi mạng yếu.
* Tự khởi tạo `cuutoi.db` khi lần đầu chạy.
* Hoàn toàn không phụ thuộc vào Google API.
* Tối ưu cho Linux, macOS, Windows và cả Docker Desktop.
