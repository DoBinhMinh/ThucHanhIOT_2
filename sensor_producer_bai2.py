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


import json
import random
import time
from datetime import datetime
import pika

QUEUE = "sensor_data_queue"


def main():
    connection = get_connection()
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE, durable=True)
        print("Cam bien dang gui du lieu moi 3 giay. Ctrl+C de dung...")
        try:
            while True:
                payload = {
                    "device_id": "sensor01",
                    "temperature": round(random.uniform(20.0, 42.0), 1),
                    "humidity": round(random.uniform(25.0, 85.0), 1),
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                }
                message = json.dumps(payload, ensure_ascii=False)
                channel.basic_publish(
                    exchange="", routing_key=QUEUE, body=message.encode("utf-8"),
                    properties=pika.BasicProperties(delivery_mode=2, content_type="application/json"),
                )
                print("Da gui:", message)
                time.sleep(3)
        except KeyboardInterrupt:
            print("Da dung mo phong cam bien")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
