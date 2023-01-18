# Auth Service code (Python)

## Create a Python project

* From 5:05 in https://www.youtube.com/watch?v=hmkF77F9TLw
* $ mkdir python/src/auth; cd python/src/auth
* Create a virtual environment in Python:
  $ python3 -m venv venv
* Activate the Python "virtual env":
  * `$ source ./venv/bin/activate`
  * Verify. `$ env | grep VIRTUAL`
    * `$ ls` => "venv"

* Install misc utils for the "vim" code editor:
  * $ pip install pylint
  * $ pip install Jedi

* Create the Python source code file for "auth" service
  * $ nano server.py
  * Youtube at 12:03: Add code etc..

* First install the "MySQL database development files"
  * $ sudo apt install libmysqlclient-dev

## OLD WAY: Install the Python libraries imported into "server.py"

* $ pip install pyjwt
* $ pip install flask
* $ pip install flask_mysqldb   # Needs "libmysqlclient-dev" (se above).

## NEW WAY: Use "Pipenv" : for "virtual environments" and Dependencies (Pipfile)

* See "[Pipenv setup and usage](PART_2c_Python__Pipenv_and_Pipfile_for_dependencies.md)".

## INSTALL: Misc MySQL tools

* See [Install MySQL tools for VS Code and terminal](PART_2b_MySQL_tools_for_VS_Code_and_terminal.md)

## MySQL related: Create tables etc

* Create database with username and password (for http authentication)
  * 19:45 into video
  * Create "init.sql" in "src/auth/"
  * Create a "database user" to access MySQL:
    * auth_user / Auth123 (PWD)
  * Create a "User" table.

* Check which databases exist:
  * `$ mysql --user=root --password=Tarmslyng_112`
    * User was created [here](PART_1b_Install_MySQL_on_Ubuntu_and_WSL2.md).
  
  * Run SQL command: `mysql> show databases;`

* Run the "init.sql" SQL script:
  * `$ mysql --user=root --password=Tarmslyng_112 < init.sql`
  * NOTE: If you get _"ERROR 1819 (HY000) at line 1: Your password does not satisfy the current policy requirements"_
    * => Run this command: `mysql> UNINSTALL COMPONENT 'file://component_validate_password';`. Will disable password validation.

* Try some "sql" commands:
  * `$ mysql --user=root --password=Tarmslyng_112`
  * `mysql> use auth;`
  * `mysql> show tables;`
  * `mysql> describe user;`
  * `mysql> select * from user;`

## Create JWT: encode using header, payload and "private key" (HS256)

* Video: 35:00
* The "auth" service: To authenticate users and return a JWT (JSON Web Token) to the "API Gateway".
* JWT:
  1. HEADER: Algorithm and Token Type ("JWT").
     * Will use the "HS256" Symmetric signing algorithm (uses just one key (private)).
     * Our "auth" service is the only "entity" that knows our "single private key".
  2. CLAIMS: Our custom claims: Claims for each user. 
     * We will define 1 custom claim: If the user has "admin" provoleges, or not (true/false).
       * "admin": true
     * Pre-defined claims also exist: Expiration of token etc.
     * The client/user Access Level is defined by claims in the Payload (part 2 of the Token).
  3. VERIFY SIGNATURE: Signs the following data using the HS256 signing algorithm:
     * Header (1)(b64-encoded), Payload (2)(b64-encoded), The "Private Key".

## Validate a JWT: decode the JWT "bearer token"

* Video: 49:00

* A) "Basic Authentication Scheme" (HTTP)
  * Requires header: "Authorization: Basic: <base64(username:password)>"
  * See RFC7617.

* B) For JWT authentication "Bearer" is used instead of "Basic"
  * => JWT auth. requires header: "Authorization: Bearer: <token>"
  * See RFC6750: "OAuth 2.0"-protected resources.
