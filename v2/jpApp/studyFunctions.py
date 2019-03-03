from jpApp.db import get_db
from jpApp.functions import *
from datetime import datetime

def getDBWordsForStudy(level):
    db = get_db()

    #Select records from coreJpDict that dont exist in studyVocab
    words = db.execute(
        'SELECT * FROM coreJpDict'
        ' LEFT JOIN studiedVocab ON studiedVocab.dict_id = coreJpDict.id'
        ' WHERE studiedVocab.dict_id IS NULL'
    ).fetchall()

    if len(words) == 0 :
        return None
    return words
    
def addStudiedWordToDB(id):
    db = get_db()
    db.execute(
        'INSERT INTO studiedVocab (dict_id)'
        ' VALUES (?)',
        (id)
    )
    db.commit()
