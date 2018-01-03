# pgpool-pyui
Rudimentary UI for [PGPool][pgpool] written in Python.

## Usage
* Edit database URL in `pgpool-pyui.cfg`, see [Database URL][database_url].
```
pip install -r requirements.txt
export FLASK_APP="pyui/pyui.py"
flask run
```

[pgpool]: https://github.com/sLoPPydrive/PGPool
[database_url]: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#db-url
