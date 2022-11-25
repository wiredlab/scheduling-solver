Flask app to display results from scheduling solver

# Dependencies

See the contents of [`requirements.txt`](requirements.txt)


```bash
#export PHOTOROSTER_JPG_CACHE=/path/to/jpg/cache
export FLASK_APP=app.py

flask run
```

With Apache's mod_wsgi, start with `scheduling-app.wsgi` and `scheduling-app.conf`.


# Installation with Apache and mod_wsgi

```bash
cd /var/www/apps/scheduling-solver

sudo virtualenv env
sudo env/bin/pip install -r requirements.txt
```

