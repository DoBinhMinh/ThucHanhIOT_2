# Ket noi RabbitMQ local: localhost:5672, guest/guest.
# Co the doi thong qua bien moi truong neu su dung broker cua lop.
import os
import pika


def get_connection():
    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_USERNAME", "guest"),
        os.getenv("RABBITMQ_PASSWORD", "guest"),
    )
    params = pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        virtual_host=os.getenv("RABBITMQ_VHOST", "/"),
        credentials=credentials,
        heartbeat=60,
        blocked_connection_timeout=30,
    )
    return pika.BlockingConnection(params)


import pika

QUEUE = "iot_lab_queue"


def main():
    ho_ten = input("Nhap ho ten: ").strip() or "Nguyen Van A"
    ma_sv = input("Nhap ma sinh vien: ").strip() or "B23DCCN542"
    so_luong = int(input("So message can gui (mac dinh 1): ").strip() or "1")
    if so_luong < 1:
        print("So luong phai lon hon 0")
        return
    connection = get_connection()
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE, durable=True)
        for i in range(so_luong):
            message = f"Xin chao tu ung dung Python AMQP - {ma_sv} - {ho_ten}"
            channel.basic_publish(
                exchange="", routing_key=QUEUE, body=message.encode("utf-8"),
                properties=pika.BasicProperties(delivery_mode=2),
            )
            print(f"Da gui message {i + 1}: {message}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
