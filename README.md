# 🍜 Hệ Thống Tra Cứu Món Ăn – Món Ngon Việt Nam

## 📌 Giới thiệu

Dự án xây dựng hệ thống thu thập và tra cứu món ăn từ website [monanngon.vn](https://monanngon.vn). Hệ thống giúp người dùng dễ dàng tìm kiếm công thức nấu ăn theo tên món hoặc nguyên liệu. Dữ liệu được lưu trữ khoa học trong cơ sở dữ liệu MySQL và hiển thị qua giao diện người dùng đơn giản, trực quan.

## 📁 Cấu trúc cơ sở dữ liệu

Hệ thống sử dụng MySQL với 2 bảng chính:

- **mon_an**: Chứa thông tin tổng quan về món ăn (tên, ảnh, link).
- **chi_tiet_mon_an**: Lưu chi tiết công thức, nguyên liệu và cách nấu.

### 🔗 Quan hệ:
`mon_an.id` (PK) ← `chi_tiet_mon_an.mon_an_id` (FK)

## 🔍 Tính năng chính

- Tìm kiếm món ăn theo **tên món** hoặc **nguyên liệu**
- Sắp xếp kết quả theo **bảng chữ cái** hoặc **mã mới nhất**
- Giao diện tìm kiếm sử dụng **Bootstrap** để tối ưu trải nghiệm người dùng
- Hiển thị kết quả gồm: ảnh, tên món, nguyên liệu, liên kết xem chi tiết

## 🛠️ Công nghệ sử dụng

- Backend: **Python **
- Cơ sở dữ liệu: **MySQL (XAMPP)**
- Frontend: **HTML**, **CSS**, **Bootstrap**
- Tìm kiếm: **SQL LIKE**
- Trình quản lý CSDL: **phpMyAdmin**

## ✅ Kết quả đạt được

- Thu thập thành công dữ liệu món ăn từ website
- Xây dựng hệ thống truy vấn và tìm kiếm hiệu quả
- Tạo giao diện người dùng thân thiện, có tính ứng dụng cao

## ⚠️ Hạn chế

- Chưa có phân loại món ăn theo nhóm (món chính, chay, tráng miệng...)
- Giao diện chưa hỗ trợ phân trang hoặc lọc nâng cao
- Hệ thống chạy trên localhost, chưa triển khai online

## 🚀 Cài đặt & sử dụng

1. Clone repo:
   ```bash
   git clone https://github.com/ttm2004/Crawl_Data.git
