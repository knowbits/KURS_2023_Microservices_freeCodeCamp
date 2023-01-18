# Python: Use "Pipenv" : for "virtual environments" and Dependencies (Pipfile)

* About "Pipenv": Basic usage: <https://pipenv.pypa.io/en/latest/basics>

## Install the "Pipenv" tool and create a "virtual environment" in the current project

* First, install "Pipenv" itself: `$ pip install pipenv`
* Second, install a virtual environment in a given folder:
  * `$ pipenv --python 3.10`

* => Results:
  1. Creates a "virtualenv" for this project using the activated/registered Python interpreter in the current terminal.
     * The virtualenv is created in the folder /home/echobravo/.local/share/virtualenvs/<"name-of-env--autogenerated">/

  2. Creates a "Pipfile" in the current directory.
     * The `Pipfile` is used to track which dependencies your project needs in case you need to re-install them.
     * `Pipfile` can also be converted to `requirements.txt`
       * NOTE: Using "requirements.txt" is an older way of handling dependencies, which is used in the video.

* Example result (output):
  * => Virtualenv location: `/home/echobravo/.local/share/virtualenvs/auth-IX-3-SWm`

* Verify that "Pipfile" has the dependencies fo your Python project:
  * `$ more ./Pipfile`

* Launches a subshell in the Python "virtual environment" (that was created above):
  * `$ pipenv shell`
  * => Activates the "virtualenv":
    * By launching a subshell in the project’s directory.
    * Verify that the correct "environment variables" were set: `$ env | grep VIRTUAL`
    * => `VIRTUAL_ENV=/home/echobravo/.local/share/virtualenvs/gateway-MTzm1DFj`

* To "exit" the "virtual environment" subshell:
  * `$ exit`

* To remove the "virtual environment" completely
  * `$ pipenv --rm`

## "Pipenv": Basic usage

* Show "Help": All available commands
  * `$ pipenv --help`

* Install a package: `$ pipenv install [package names]`
  * Option: "--system": Use the system pip command rather than the one from your "virtualenv" (check the `$ virtualenv` command).

* Uninstall a package: `$ pipenv uninstall [package name]`

* Install all the dependencies for a project:
  * `$ pipenv install`

* Install all the dependencies for a project (including dev packages):
  * `$ pipenv install --dev`

## Use "Pipenv" to install the Python libraries imported into "server.py"

* First, start the project's "virtual environment" by running `$ pipenv shell`

* `$ pipenv install pyjwt`
* `$ pipenv install flask`
* The following needs "libmysqlclient-dev" (se above):
* `$ pipenv install flask_mysqldb`
* Verify that the dependencies are added to "Pipfile" file.
* Finally, run your script to check that all required packages are installed:
  * `$ pipenv run python server.py`
  
  