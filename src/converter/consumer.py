import pika, sys, os, time
from pymongo import MongoClient
import gridfs
# Our package named "convert", with a module named "to_mp3":
from convert import to_mp3


def main():
    # NOTE: mongodb runs as a local service on "localhost",
    #       it is not running as a aprt of the Kubernetes cluster.
    # ORIGINAL: client = MongoClient("host.minikube.internal", 27017)
    client = MongoClient("mongo", 27017)

    # Set the databases that we will use from within "mongodb"
    db_videos = client.videos
    db_mp3s = client.mp3s

    # gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    # Configure rabbitmq connection
    # NOTE: The Kubernetes "service name" is "rabbitmq",
    #       and it will resolve to the host IP of the service.
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    # Called when a new message is pulled off the "videos" queue by the consumer service:
    def callback(ch, method, properties, body):
        # Call a function in our "to_mp3" module:
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            # Send a "negative acknowledgment" (NACK) to the queue:
            # => Message will not be removed from the queue (=> Can be processed later).
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            # No errors => Acknowledge the message on the queue:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # Consume messages from the "videos" queue
    channel.basic_consume(
        # 1. Get the name of the "videos" queue from environment variable.
        # 2. Define a callback function that will be called when a message is pulled off the queue.
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback
    )

    print("Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
