import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext
import click

def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode('utf8'))
    
def get_db():
    #init our db if it doesnt exist.
    if 'db' not in g:
        print("connecting to our db")
        g.db = sqlite3.connect(current_app.config['DATABASE'],
                               detect_types=sqlite3.PARSE_DECLTYPES
        )        
        g.db.row_factory = sqlite3.Row
        
    return g.db


def close_db(e=None):
    #same as with
    db = g.pop('db', None)

    if db is not None:
        db.close()
        print("closing db")

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(loadTestData)
    app.cli.add_command(clearDb)
    app.teardown_appcontext(close_db)

@click.command('loadTestData')
@with_appcontext
def loadTestData():
    db = get_db()
    testData = []
    testDataFile = open("jpApp/testData.txt", 'r', encoding='utf8')
    for line in testDataFile:
        line = line.strip('\n')
        line = line.split()
        testData.append(line)

        db.execute(
            'INSERT INTO jpVocab (jpWord, pronunciation, meaning)'
            ' VALUES (?,?,?)',
            (line[0],line[1],line[2])
        )
        db.commit()        

    testDataFile.close()
    

    
@click.command('clearDb')
@with_appcontext
def clearDb():
    db = get_db()
    db.execute('DELETE FROM jpVocab')
    db.commit()
    
