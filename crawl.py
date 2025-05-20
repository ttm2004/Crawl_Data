import requests
from bs4 import BeautifulSoup
import pymysql
import time

# Kết nối MySQL
conn = pymysql.connect(host='localhost', user='root', password='', database='monngon', charset='utf8mb4')
cursor = conn.cursor()

headers = {
    "User-Agent": "Mozilla/5.0"
}


so_luong = 50
# Crawl chi tiết món ăn
def crawl_chi_tiet(link):
    try:
        res = requests.get(link, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # Tìm phần nội dung đầy đủ (gồm hình ảnh, đoạn văn, tiêu đề...)
        content_div = soup.select_one("div.blog-entry")
        html_raw = content_div.decode_contents() if content_div else "Không có"

        # Có thể vẫn lưu thêm dạng text tóm tắt
        nglieu = "Không có"
        if content_div:
            text_preview = content_div.get_text(strip=True)
            nglieu = text_preview[:500] + "..."  # lấy đoạn tóm tắt

        return nglieu.strip(), html_raw.strip()

    except Exception as e:
        print(f"❌ Lỗi khi crawl chi tiết: {e}")
        return "Không có", "Không có"
def crawl_chi_tiet(link):
    try:
        res = requests.get(link, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        content_div = soup.select_one("div.blog-entry")
        html_raw = content_div.decode_contents() if content_div else "Không có"

        nguyen_lieu = []
        cach_nau = []
        is_nglieu = is_cachnau = False

        if content_div:
            for tag in content_div.find_all(["p", "ul", "ol", "h2", "h3", "h4"]):
                text = tag.get_text(strip=True).lower()

                # Nhận biết phần nguyên liệu bắt đầu
                if "nguyên liệu" in text:
                    is_nglieu = True
                    is_cachnau = False
                    continue

                # Nhận biết phần cách nấu/bước làm bắt đầu
                if any(keyword in text for keyword in ["cách làm", "thực hiện", "chế biến", "hướng dẫn", "bước"]):
                    is_cachnau = True
                    is_nglieu = False
                    continue

                # Ghi nhận nội dung
                if is_nglieu:
                    nguyen_lieu.append(tag.get_text(strip=True))
                elif is_cachnau:
                    cach_nau.append(tag.get_text(strip=True))

        nglieu = "\n".join(nguyen_lieu).strip() or "Không có"
        cachnau = "\n".join(cach_nau).strip() or "Không có"

        return nglieu, cachnau, html_raw.strip()

    except Exception as e:
        print(f"❌ Lỗi khi crawl chi tiết: {e}")
        return "Không có", "Không có", "Không có"


# Crawl danh sách món ăn
monan_quet = 0  # Đếm tổng số món đã xử lý (bất kể đã có hay chưa)
page = 1
while monan_quet < so_luong:
    url = f"https://monanngon.vn/mon-ngon/page/{page}/"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    items = soup.select('div.restaurant-grid-item')
    if not items:
        print(f"⛔ Không còn món ăn ở trang {page}")
        break

    for item in items:
        if monan_quet >= 30:
            break

        try:
            ten_mon = item.select_one('h5.cat-tt2').text.strip()
            link = item.select_one('a')['href']
            img_tag = item.select_one('img')
            img = img_tag.get('data-lazy-src') or img_tag.get('src')

            monan_quet += 1  # ✅ Tăng bất kể món có tồn tại hay chưa

            cursor.execute("SELECT id FROM mon_an WHERE link = %s", (link,))
            if cursor.fetchone():
                print(f"⏩ [{monan_quet}] Đã có: {ten_mon}")
                continue

            cursor.execute(
                "INSERT INTO mon_an (ten_mon, hinh_anh, link) VALUES (%s, %s, %s)",
                (ten_mon, img, link)
            )
            conn.commit()
            print(f"✅ [{monan_quet}] Thêm mới: {ten_mon}")
            time.sleep(0.2)
        except Exception as e:
            print(f"❌ Lỗi: {e}")

    page += 1


# Bước 2: Crawl chi tiết theo danh sách đã có
print("\n🔍 Bắt đầu crawl chi tiết cho từng món...")

cursor.execute("""
    SELECT mon_an.id, mon_an.link 
    FROM mon_an 
    LEFT JOIN chi_tiet_mon_an ON mon_an.id = chi_tiet_mon_an.mon_an_id 
    WHERE chi_tiet_mon_an.id IS NULL
    ORDER BY mon_an.id ASC
    LIMIT %s
""", (so_luong,))

rows = cursor.fetchall()

for idx, (mon_an_id, link) in enumerate(rows, start=1):
    try:
        # GỌI LẠI HÀM CRAWL CHI TIẾT TỪ LINK
        nglieu, cachnau, html_raw = crawl_chi_tiet(link)

        # XÓA BẢN GHI CŨ (nếu cần)
        cursor.execute("DELETE FROM chi_tiet_mon_an WHERE mon_an_id = %s", (mon_an_id,))

        # CHÈN DỮ LIỆU MỚI
        cursor.execute("""
            INSERT INTO chi_tiet_mon_an (mon_an_id, nguyen_lieu, cach_nau, noi_dung_html)
            VALUES (%s, %s, %s, %s)
        """, (mon_an_id, nglieu, cachnau, html_raw))

        conn.commit()
        print(f"📌 Chi tiết [{idx}] OK: {link}")
        time.sleep(0.2)

    except Exception as e:
        print(f"❌ Chi tiết lỗi [{idx}]: {e}")


conn.close()
print("🎉 Hoàn tất toàn bộ crawl!")
