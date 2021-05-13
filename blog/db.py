import sqlite3
import click
from flask.cli import with_appcontext
from flask import(
    g, current_app
)

def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

#init database
@click.command('init-db')
@with_appcontext
def init_db_command():
    click.echo("start initializing db ...")
    init_db()
    click.echo("Done!")

#get database
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("userdb.db")
        g.db.row_factory = sqlite3.Row
        #to make db to appear as a dictionary instead of a tuple
    return g.db

#close database
def close_db(e):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
