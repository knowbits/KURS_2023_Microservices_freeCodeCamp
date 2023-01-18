# "gridfs": to store larger files in MongoDb:
import os, gridfs
# pika: to interface with "queue" (RabbitMQ for messages)
import pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo

# These packages needs to be created:
# (containing the imported "modules": validate, access, util):
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)
# NOTE: "host.minikube.internal"
#       => Gives access to "localhost" from within the Kubernetes cluster.
#       But not on WSL it seems...
# ORIGINAL: mongo_videos = PyMongo(server, uri="mongodb://host.minikube.internal:27017/videos")
# Now running mongodb in the Kubernetes cluster instead:
mongo_videos = PyMongo(server, uri="mongodb://mongo:27017/videos")

# PyMongo will wrap our "Flask server" => We can interface with our mongodb.
# ORIGINAL: mongo_mp3s = PyMongo(server, uri="mongodb://host.minikube.internal:27017/mp3s")
mongo_mp3s = PyMongo(server, uri="mongodb://mongo:27017/mp3s")

# "GridFS" will wrap our mongodb => Enables us to use MongoDB's "GridFS".
fs_videos = gridfs.GridFS(mongo_videos.db)
fs_mp3s = gridfs.GridFS(mongo_mp3s.db)

# Configure the RabbitMQ connection
# NOTE: The RabbitMQ service will be deployed as StatefulSet in Kubernetes
# Pass the "RabbittMQ host" for the "RabittMQ service":
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

# ======================================
@server.route("/login", methods=["POST"])
def login():
    # Calls the login() function in the "access" module.
    # Returns a "JWT" token from the "auth service".
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


# ======================================
@server.route("/upload", methods=["POST"])
# The function serving "upload" route:
def upload():
    # 1) Validate user: Token must be present (from a previous "/login" call).

    # Calls the upload() function in the "validate" module.
    # Returns the decoded "payload" of the JWT: as a JSON formatted string.
    # The payload contains the claims: One of them is our custom "admin" claim (true or false).
    access, err = validate.token(request)

    if err:
        return err

    # Deserialize a JSON document to a Python object:
    # => The fields of the "access" variable will be the same as in "createJWT()":
    #    username, exp, iat, admin ("admin" is CUSTOM)
    access = json.loads(access)

    # Check the "admin" claim from the decoded JWT payload ("access" variable).
    # If "admin" is "True" => Give the user access to this endpoint ("/upload").
    if access["admin"]:
        # Verify that there indeed is exactly 1 file to be uploaded in the request:
        # => The request must contain a "dictionary" in "files":
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required", 400

        # => There was exactly 1 file in the request => Store it in GridFS ? Send message.
        # The "files" dictionary: Has a "key" for the file, the "value" is the actual file.
        # => Iterate throgh the "key, value" pairs:
        for _, f in request.files.items():
	    # Upload the file to GridFS:
            err = util.upload(f, fs_videos, channel, access)

            if err:
                return err

        return "success!", 200
    else:
        return "not authorized", 401


# ======================================
@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        # Make sure the "file id" exists in the request.
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required", 400

        # Get the file from mongodb:
        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f"{fid_string}.mp3")
        except Exception as err:
            print(err)
            return "internal server error", 500

    return "not authorized", 401


# ======================================
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
