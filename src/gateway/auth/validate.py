import os, requests


# Validate the token (JWT) that is sent by the client
# The token sent as a part of a user HTTP request to the "API Gateway" (gateway/server.py)
#
# The user's HTTP request will contain an "Authorization header" containing the JWT.
# => Tells the "API Gateway" that the client (user) has been granted access to the application endpoints.
def token(request):
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("missing credentials", 401)

    # Response: will be the decoded body (payload: a JSON string) of the JWT:
    #           Containing the CLAIMS: username, privileges (i.e. our custom "admin" claim):
    response = requests.post(
        # Forward the JWT token to the "auth" service "/validate" endpoint:
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        # Pass along the "Authorization" token to the "validate" function in the "auth" service:
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
