# ===========================================
# COURSE: Freecodecamp:
#   https://www.youtube.com/watch?v=hmkF77F9TLw (5h)
#   "Microservice Architecture and System Design with Python & Kubernetes – Full Course"
#
# Flow of the "auth" service:
#   1) User User makes request to the "login" route.
#   2) Enters credentials: username and password.
#   3) Service checks if user exists in the MySQL db
#   4) If yes, then the user is considered authenticated
#   5) => A JWT is created and returned,
#   6) The JWT will include the "Custom claim" named "admin",
#      which determines access level: which endpoints the user has access to.
#      "admin" rights => Access is granted to ALL endpoints.
# ===========================================
# os: for environment variables
# datetime: for expiration time of JWT
import jwt, datetime, os
# Flask: for the server
from flask import Flask, request
from flask_mysqldb import MySQL

# Flask: A http server. Serves routes etc
server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
# EB: Had to add int() to avoid ERROR:
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))

# TEST: print an "env var":
# NOTE: Set in terminal first: $ export MYSQL_HOST=localhost
# print(server.config["MYSQL_HOST"])

# Set up the "login" route in the Flask server
@server.route("/login", methods=["POST"])
def login():
    # Requires a header to be present in the http request: Basic Authentication scheme.
    auth = request.authorization

    # "auth" will be empty (none) if Header is not present in the HTTP request.
    if not auth:
        return "missing credentials", 401

    # _username = auth.username
    # _password = auth.password

    # check db for username and password:
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalide credentials", 401
# ------------------------------------------


# ------------------------------------------
# Create a route to validate JWTs
@server.route("/validate", methods=["POST"])
def validate():
    # The header has this format: "Authorization: <type> <token>"

    # To save some time:
    # => Will not check for "Bearer" (type) in the HTTP "Authorization: <type> <token>" header.
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        # "decoded": Will include the JWT payload: The claims: username (email),
        #            Their privileges: our custom "admin" (true/fales) claim.
        decoded = jwt.decode(
          # Use the same "key" to decode the token that we used to encode the JWT:
          encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200
# ------------------------------------------


# ------------------------------------------
# authz: true/false: Tells if user has admin provoleges or not.
#        Claims in the Payload part (section 2) of the JWT.
def createJWT(username, secret, authz):
    # To create a JWT we need to pass:
    #   1) Dictionary with our claims,
    #   2) The secret (private key),
    #   3) The type of signing algorithm (HS256).
    return jwt.encode(
        {   # Dictionary: Claims:
            "username": username,
            # Token expires in 1 day (24 h):
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            # iat: Issued At: When token was issued:
            "iat": datetime.datetime.utcnow(),
            # Our "custom claim": If the user has administrator privileges or not.
            "admin": authz,
        },
        # The private key used to sign with HS256 algorithm:
        secret,
        # Pass in the signing algorithm to be used to create the JWT:
        algorithm="HS256",
    )
# ------------------------------------------


# ------------------------------------------
# Define ENTRYPOINT: If we run this file using
#   the "python server.py" command
#   => __name__ will resolve to "__main__"
#
# Start the SERVER on port 5000
#
if __name__ == "__main__":
    # "0.0.0.0" => Will listen to ALL public IP-addresses on our host.
    #              NOTE: default is "localhost", if not specified.
    server.run(host="0.0.0.0", port=5000)

