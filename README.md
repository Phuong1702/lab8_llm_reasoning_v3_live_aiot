# Lab 8 - LLM Reasoning for AIoT with Live Sensor, YOLO, Ollama and Gemini

## 1. Giới thiệu

Dự án này là bài thực hành Lab 8 thuộc học phần Triển khai, phát triển ứng dụng AI và IoT. Mục tiêu của bài lab là tích hợp Large Language Model vào hệ thống AIoT để hỗ trợ suy luận, giải thích tình huống và đề xuất hành động dựa trên dữ liệu cảm biến, kết quả AI model và bằng chứng từ camera.

Trong bài này, LLM không thay thế cảm biến hoặc các mô hình AI trước đó. LLM đóng vai trò là tầng reasoning, nhận context packet từ hệ thống và trả về quyết định dạng JSON có kiểm tra an toàn.

## 2. Công nghệ sử dụng

* Python
* FastAPI
* Uvicorn
* OpenCV
* YOLOv8n
* Ollama local LLM
* Gemini API
* HTML, CSS, JavaScript
* JSON, CSV, JSONL

## 3. Chức năng chính

* Mô phỏng dữ liệu cảm biến phòng học thông minh
* So sánh 3 tầng xử lý:

  * Sensor only
  * Sensor + AI models
  * Sensor + AI models + LLM
* Tích hợp webcam thật bằng OpenCV
* Phát hiện người bằng YOLOv8n
* Gọi Ollama local LLM ở chế độ `mode=local`
* Gọi Gemini API ở chế độ `mode=api`
* Chat trực tiếp với Gemini qua endpoint `/gemini-chat`
* Tạo context packet cho LLM reasoning
* Kiểm tra kết quả bằng validation và safety gate
* Xuất log phục vụ báo cáo

## 4. Kiến trúc hệ thống

```text
Sensor Simulator
→ AI Evidence từ Lab 3, Lab 4, Lab 6, Lab 7
→ Webcam + YOLOv8n
→ Context Packet
→ LLM Reasoning
   → Ollama local
   → Gemini API
→ Safety Gate
→ Dashboard / JSON Output
```

## 5. Ý nghĩa của các tầng so sánh

### Sensor only

Tầng này chỉ đọc dữ liệu cảm biến hiện tại và áp dụng rule cứng. Ví dụ nếu CO2 chưa vượt ngưỡng thì hệ thống có thể đánh giá rủi ro thấp.

### Sensor + AI models

Tầng này dùng thêm các bằng chứng AI như anomaly detection, forecasting, motion event và vision event. Nhờ đó hệ thống có thể phát hiện rủi ro tốt hơn so với chỉ đọc cảm biến thô.

### Sensor + AI models + LLM

Tầng này dùng LLM để tổng hợp bằng chứng, giải thích tình huống và đề xuất hành động. Kết quả được trả về dưới dạng JSON decision và đi qua safety gate trước khi hiển thị.

## 6. Vai trò của LLM trong Lab 8

LLM được dùng để:

* Đọc context packet từ hệ thống AIoT
* Tổng hợp dữ liệu cảm biến, dự báo và camera
* Giải thích tình huống bằng ngôn ngữ dễ hiểu
* Đề xuất hành động cho người vận hành
* Trả về JSON có cấu trúc
* Hỗ trợ ra quyết định nhưng không tự động điều khiển thiết bị

## 7. Safety Gate

Safety gate có nhiệm vụ kiểm tra kết quả từ LLM trước khi chấp nhận. Trong lab mode, hệ thống không cho phép điều khiển thiết bị trực tiếp. Vì vậy trường `control_allowed` thường được đặt là `false`.

Safety gate giúp hạn chế rủi ro khi LLM trả lời sai, thiếu dữ liệu hoặc đề xuất hành động chưa an toàn.

## 8. Cài đặt môi trường

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install ultralytics opencv-python numpy google-genai
```

## 9. Cấu hình file .env

Tạo file `.env` trong thư mục dự án:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:1.7b
LLM_TEMPERATURE=0.2
LLM_NUM_CTX=4096
LLM_TIMEOUT_SEC=60

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
```

Lưu ý: Không upload file `.env` lên GitHub vì file này chứa API key.

## 10. Chạy chương trình

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Sau đó mở trình duyệt:

```text
http://127.0.0.1:8000/
```

## 11. Các endpoint quan trọng

### Dashboard chính

```text
http://127.0.0.1:8000/
```

### API Docs

```text
http://127.0.0.1:8000/docs
```

### Bật camera

```text
POST /camera/start
```

### Xem trạng thái camera YOLO

```text
GET /camera/latest
```

### Xem frame camera có bbox

```text
GET /camera/frame
```

### So sánh 3 tầng bằng Ollama local

```text
GET /compare-three-levels/lab_overcrowded_high_co2?mode=local
```

### So sánh 3 tầng bằng Gemini API

```text
GET /compare-three-levels/lab_overcrowded_high_co2?mode=api
```

