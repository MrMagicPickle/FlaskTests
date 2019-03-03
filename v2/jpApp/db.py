import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime
import os

from jpApp.functions import *
import click

#Init the database. - Call this whenever you changed the structure of the .sql
def init_db():
    db = get_db()
    with current_app.open_resource("schema2.sql") as f:
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
    app.cli.add_command(loadData)
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
    

def updateDB():
    db = get_db()
    jpVocabs = db.execute(
        'SELECT * FROM jpVocab'
    ).fetchall()


    for word in jpVocabs:
        learntDate = word['dateRevised']
        currDate = datetime.now()
        daysElapsed = (currDate - learntDate).days + 1
        stability = word['stability']
        memRet = getR(stability, daysElapsed)
        if isRevisable(memRet):
            db.execute(
                'UPDATE jpVocab SET revisable = ?'
                ' WHERE id = ?',
                (1, word['id'])
            )
    db.commit()
        

@click.command('loadData')
@with_appcontext
def loadData():
    db = get_db()

    jpVocabDir = "C:/Users/User-HP/Desktop/My Projects/FlaskTest/v2/jpApp/data/"
    for root, dirs, files in os.walk(jpVocabDir):
        for file in files:
            filepath = root + os.sep + file
            #simple validation.
            if filepath.endswith(".txt"):
                #read the file and load the data into our db.
                infile = open(filepath, 'r', encoding='utf8')
                level = getLevel(file)
                for line in infile:
                    line = line.strip('\n')
                    line = line.split('/')
                    db.execute(
                        'INSERT INTO coreJpDict (jpWord, pronunciation, meaning, enSentence, jpSentence, wordLevel)'
                        ' VALUES (?,?,?,?,?,?)',
                        (line[0], line[1], line[2], line[4], line[3], level)
                    )


                    
                infile.close()
    db.commit()                                    


def getLevel(filename):
    index = filename.find('.txt')
    lv = ""
    for i in range (index, -1, -1):
        if filename[i] == "v":
            break

        lv += filename[i]

    return lv[::-1] #return reversed string.
