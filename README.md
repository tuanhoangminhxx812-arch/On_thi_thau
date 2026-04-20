# Ứng dụng Học Trắc Nghiệm (Streamlit)

Đây là một ứng dụng hỗ trợ ôn luyện trắc nghiệm nội bộ trực quan và hiện đại được phát triển bằng ngôn ngữ Python với framework Streamlit. Ứng dụng tự động tải, phân tích và chuẩn hóa dữ liệu từ các tệp bài tập (Excel) và hiển thị bài thi trắc nghiệm dưới một giao diện đẹp mắt có hỗ trợ tính năng chấm trực tiếp tại chỗ.

## Tính Năng Chính
- **Tự động trích xuất dữ liệu**: Thuật toán thông minh có thể đọc nhiều định dạng dữ liệu Excel khác nhau (nhận diện câu hỏi có đánh số, nhận diện nhãn Q, A, a, b, c,...) và tổng hợp lại.
- **Hỗ trợ 3 chủ đề kiến thức nội bộ**:
  - An Toàn Thông Tin (ATTT)
  - Kiến thức Đấu Thầu
  - Văn Hóa Doanh Nghiệp
- **Giao diện hiện đại (Glassmorphism layout)**: Hỗ trợ layout trải rộng `wide` để dễ dàng đọc những mệnh đề dài mà không bị bẻ phím. Tích hợp phông chữ hiện đại làm tăng trải nghiệm người dùng.
- **Phản hồi tức thì**: Kiểm tra ngay mỗi câu hỏi xem đáp án đúng hay sai, hiển thị trực quan cảnh báo và đáp án đúng nếu lỡ trả lời sai.

## Hướng Dẫn Cài Đặt

1. **Yêu cầu hệ thống**: Python 3.9+ 
2. **Cài đặt thư viện**: Bạn có thể dễ dàng cài đặt các thư viện cần thiết thông qua tập tin `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Chạy Ứng Dụng

Sau khi quá trình cài đặt môi trường thành công, bạn có thể khởi chạy ứng dụng bằng câu lệnh tại thư mục hiện tại:

```bash
streamlit run app.py
```
Ứng dụng sẽ tự động mở lên trên trình duyệt của bạn (Thông thường tại địa chỉ http://localhost:8501).

---
*Developed by Antigravity AI.*
