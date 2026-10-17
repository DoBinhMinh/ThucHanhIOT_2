# BUỔI 2 - THỰC HÀNH LẬP TRÌNH PYTHON VỚI GIAO THỨC AMQP

## Thông tin sinh viên thực hiện

| STT | Họ và tên | Mã sinh viên |
|-----|-----------|--------------|
| 1 | Nguyễn Đại Nghĩa | B23DCCN598 |
| 2 | Đỗ Bình Minh | B23DCCN542 |

## 1. Giới thiệu

Bài thực hành sử dụng Python và giao thức AMQP để xây dựng các chương trình gửi, nhận và xử lý message thông qua RabbitMQ Broker.

Nội dung gồm 3 bài:

- Bài 1: Gửi và nhận message cơ bản qua Queue.
- Bài 2: Mô phỏng cảm biến IoT gửi dữ liệu môi trường.
- Bài 3: Mô phỏng hệ thống điều phối cảnh báo IoT với Exchange.

## 2. Môi trường thực hiện

- Ngôn ngữ: Python 3.x
- Thư viện: pika
- Broker: RabbitMQ
- Giao thức: AMQP
- Công cụ lập trình: Visual Studio Code
- Môi trường triển khai RabbitMQ: Docker Desktop

### Thông tin Broker

| Thành phần | Giá trị |
|------------|---------|
| Broker | RabbitMQ |
| Host | localhost |
| Port | 5672 |
| Username | guest |
| Password | guest |
| Management UI | http://localhost:15672 |

## 3. Cấu trúc thư mục

```text
ThucHanhIOT_PTIT/
│
├── Buoi1/
│
├── Buoi2/
│   ├── producer_bai1.py
│   ├── consumer_bai1.py
│   ├── sensor_producer_bai2.py
│   ├── monitor_consumer_bai2.py
│   ├── alert_producer_bai3.py
│   ├── warning_consumer_bai3.py
│   └── critical_consumer_bai3.py
│
└── README.md
```

## 4. Cài đặt và khởi động

### 4.1. Cài đặt thư viện Python

Mở Terminal trong VS Code:

```bash
python -m pip install pika
```

### 4.2. Khởi động RabbitMQ

Nếu chưa tạo container RabbitMQ:

```bash
docker run -d --name iot-rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```

Nếu container đã tồn tại:

```bash
docker start iot-rabbitmq
```

Kiểm tra trạng thái:

```bash
docker ps
```

Truy cập giao diện quản lý RabbitMQ:

http://localhost:15672

Đăng nhập với tài khoản `guest` và mật khẩu `guest`.

### 4.3. Chuyển vào thư mục thực hành

Từ thư mục gốc của repository:

```bash
cd Buoi2
```

## 5. Bài 1 - Gửi và nhận message cơ bản qua Queue

### 5.1. Mục tiêu

Tìm hiểu cách Producer gửi message đến RabbitMQ Queue và Consumer nhận message từ Queue.

Queue sử dụng:

```text
iot_lab_queue
```

### 5.2. Chạy chương trình

Mở Terminal 1, chạy Consumer:

```bash
python consumer_bai1.py
```

Mở Terminal 2, chạy Producer:

```bash
python producer_bai1.py
```

Nhập thông tin sinh viên khi chương trình yêu cầu.

Ví dụ:

```text
Ho ten: Do Binh Minh
Ma sinh vien: B23DCCN542
```

### 5.3. Kết quả mong đợi

Producer gửi message:

```text
Xin chao tu ung dung Python AMQP - B23DCCN542 - Do Binh Minh
```

Consumer nhận message:

```text
Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN542 - Do Binh Minh
Thoi gian nhan: 14:05:21
```

### 5.4. Kết quả đạt được

- Kết nối ứng dụng Python với RabbitMQ Broker.
- Tạo và sử dụng Queue `iot_lab_queue`.
- Producer gửi message chứa thông tin sinh viên.
- Consumer nhận và hiển thị nội dung message.
- Hiển thị thời điểm nhận message.
- Hỗ trợ gửi nhiều message liên tiếp.

## 6. Bài 2 - Mô phỏng cảm biến IoT gửi dữ liệu môi trường

### 6.1. Mục tiêu

Mô phỏng cảm biến IoT gửi dữ liệu nhiệt độ và độ ẩm định kỳ qua RabbitMQ.

Queue sử dụng:

```text
sensor_data_queue
```

### 6.2. Chạy chương trình

Mở Terminal 1, chạy Monitoring Consumer:

```bash
python monitor_consumer_bai2.py
```

Mở Terminal 2, chạy Sensor Producer:

```bash
python sensor_producer_bai2.py
```

Sensor Producer tự động tạo và gửi dữ liệu mỗi 3 giây.

### 6.3. Dữ liệu gửi

Dữ liệu được gửi dưới dạng JSON:

```json
{
  "device_id": "sensor01",
  "temperature": 36.4,
  "humidity": 38.9
}
```

Trong đó:

- `device_id`: Mã thiết bị cảm biến.
- `temperature`: Nhiệt độ được sinh ngẫu nhiên.
- `humidity`: Độ ẩm được sinh ngẫu nhiên.

### 6.4. Điều kiện cảnh báo

- Nếu nhiệt độ > 35°C: Cảnh báo nhiệt độ cao.
- Nếu độ ẩm < 40%: Cảnh báo độ ẩm thấp.

### 6.5. Kết quả mong đợi

```text
Device: sensor01
Temperature: 36.4
Humidity: 38.9
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
```

### 6.6. Kết quả đạt được

- Mô phỏng cảm biến IoT gửi dữ liệu định kỳ 3 giây/lần.
- Truyền dữ liệu bằng định dạng JSON.
- Consumer nhận và phân tích dữ liệu.
- Hiển thị mã thiết bị, nhiệt độ và độ ẩm.
- Phát hiện và cảnh báo khi nhiệt độ hoặc độ ẩm vượt ngưỡng quy định.

## 7. Bài 3 - Mô phỏng hệ thống điều phối cảnh báo IoT với Exchange

### 7.1. Mục tiêu

Tìm hiểu cơ chế Direct Exchange và Routing Key trong RabbitMQ để phân phối message đến các Queue tương ứng.

Exchange sử dụng:

```text
iot_alert_exchange
```

Loại Exchange:

```text
direct
```

Các Routing Key:

- `info`
- `warning`
- `critical`

Các Queue:

- `warning_queue`
- `critical_queue`

### 7.2. Chạy chương trình

Mở Terminal 1, chạy Warning Consumer:

```bash
python warning_consumer_bai3.py
```

Mở Terminal 2, chạy Critical Consumer:

```bash
python critical_consumer_bai3.py
```

Mở Terminal 3, chạy Alert Producer:

```bash
python alert_producer_bai3.py
```

Lưu ý: Cần khởi động hai Consumer trước khi chạy Producer để các Queue được tạo và liên kết với Exchange.

### 7.3. Nguyên lý hoạt động

Producer gửi message đến Direct Exchange `iot_alert_exchange`.

Exchange dựa vào Routing Key để chuyển message đến Queue tương ứng.

| Routing Key | Queue nhận |
|-------------|------------|
| info | Không có Queue được bind |
| warning | warning_queue |
| critical | critical_queue |

### 7.4. Kết quả mong đợi

Alert Producer gửi các cảnh báo:

```text
[info] He thong IoT dang hoat dong binh thuong
[warning] Nhiet do phong may vuot nguong warning
[critical] Cam bien kho lanh mat ket noi critical
```

Warning Consumer nhận:

```text
[warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
```

Critical Consumer nhận:

```text
[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
```

Message với Routing Key `info` không được hai Consumer trên nhận.

### 7.5. Kết quả đạt được

- Tạo Direct Exchange `iot_alert_exchange`.
- Tạo các Queue nhận cảnh báo.
- Bind Queue với Exchange bằng Routing Key.
- Warning Consumer chỉ nhận cảnh báo mức warning.
- Critical Consumer chỉ nhận cảnh báo mức critical.
- Hiểu cách RabbitMQ định tuyến message thông qua Exchange.

## 8. Tổng kết

| Bài | Nội dung | Kết quả |
|-----|----------|---------|
| Bài 1 | Gửi và nhận message qua Queue | Gửi, nhận thông tin sinh viên và hiển thị thời gian |
| Bài 2 | Mô phỏng cảm biến IoT | Gửi dữ liệu JSON định kỳ và xử lý cảnh báo |
| Bài 3 | Điều phối cảnh báo bằng Exchange | Phân phối message dựa trên Routing Key |

### Kiến thức thu được

Sau buổi thực hành, sinh viên nắm được:

1. Cách kết nối Python với RabbitMQ bằng thư viện pika.
2. Cách sử dụng Producer, Consumer và Queue.
3. Cách gửi và nhận dữ liệu JSON qua AMQP.
4. Cách mô phỏng hệ thống cảm biến IoT.
5. Cách sử dụng Direct Exchange và Routing Key.
6. Cách xây dựng hệ thống điều phối cảnh báo IoT.

## 9. Thành viên thực hiện

| STT | Họ và tên | Mã sinh viên |
|-----|-----------|--------------|
| 1 | Nguyễn Đại Nghĩa | B23DCCN598 |
| 2 | Đỗ Bình Minh | B23DCCN542 |