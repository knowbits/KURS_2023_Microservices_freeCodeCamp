import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor

# Called by the "callback" function
def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # empty temp file
    tf = tempfile.NamedTemporaryFile()
    
    # video contents
    # Get the video contents: get the file from GridFS:
    # See file "src/gateway/storage/util.py": upload() function:
    out = fs_videos.get(ObjectId(message["video_fid"]))

    # add video contents to empty file
    # Add the video contents (bytes) to the "empty file":
    tf.write(out.read())

    # create audio from temp video file
    audio = moviepy.editor.VideoFileClip(tf.name).audio

    # NOTE: File will be deleted when calling close()
    tf.close()

    # write audio to the file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    # Save the audio file to mongodb
    f = open(tf_path, "rb")
    data = f.read()
    # Store the mp3 audio file in GridFS:
    fid = fs_mp3s.put(data)
    f.close()
    # Audio file must be deleted manually:
    os.remove(tf_path)

    # Update the message:
    message["mp3_fid"] = str(fid)

    # Put the message on the "mp3s" queue:
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        # Delete the mp3 file from mongodb:
        fs_mp3s.delete(fid)
        return "failed to publish message"
