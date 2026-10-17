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


from datetime import datetime

QUEUE = "iot_lab_queue"


def on_message(ch, method, properties, body):
    print("Da nhan message:", body.decode("utf-8"))
    print("Thoi gian nhan:", datetime.now().strftime("%H:%M:%S"))
    print("-" * 40)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = get_connection()
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=QUEUE, on_message_callback=on_message)
        print(f"Dang lang nghe queue {QUEUE}. Nhan Ctrl+C de dung...")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
