Flask app to display results from scheduling solver

# Dependencies

See the contents of [`requirements.txt`](requirements.txt)


Install `pip` and the Python `venv` package, if not already present.
Instructions are for a Debian/Ubuntu-based system:

```console
$ sudo apt install python3-pip python3-venv
```



Create a Python virtual environment and install dependencies:

```console
# Fetch the code and enter the new folder
$ git clone https://github.com/wiredlab/scheduling-solver.git
$ cd scheduling-solver

# Create a Python virtual environment and install dependencies
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```


The following will run a development server for local use, the command will output the URL the server is listening on:

```console
$ flask run
```



# Installation with Apache and mod_wsgi

With Apache's mod_wsgi, start with `scheduling-app.wsgi` and `scheduling-app.conf`.

```bash
cd /var/www/apps/scheduling-solver

sudo virtualenv env
sudo env/bin/pip install -r requirements.txt
```

