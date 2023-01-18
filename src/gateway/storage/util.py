import pika, json

def upload(f, fs, channel, access):
    try:
        print("Saving file to MongoDB: ", f)
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return "Failed saving file to RabbitMQ: internal server error", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        print("Putting message on RabbitMQ: ", json.dumps(message))
        channel.basic_publish(
            exchange="",
            routing_key="videos",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        print(err)
        fs.delete(fid)
        return "Failed posting message on RabbitMC: internal server error", 500
