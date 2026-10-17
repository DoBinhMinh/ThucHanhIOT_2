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

EXCHANGE = "iot_alert_exchange"
ALERTS = [
    ("info", "He thong IoT dang hoat dong binh thuong info"),
    ("warning", "Nhiet do phong may vuot nguong warning"),
    ("critical", "Cam bien kho lanh mat ket noi critical"),
]


def main():
    connection = get_connection()
    try:
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct", durable=True)
        for routing_key, message in ALERTS:
            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=message.encode("utf-8"),
                properties=pika.BasicProperties(delivery_mode=2),
            )
            print(f"Da gui [{routing_key}]: {message}")
        print("Luu y: neu chua bind queue, message co the bi bo qua.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
