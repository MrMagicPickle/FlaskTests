from flask import (Blueprint, render_template, g, redirect, url_for, flash, request, jsonify)
from jpApp.db import get_db
from datetime import datetime
from jpApp.studyFunctions import *

bp = Blueprint("study", __name__)


@bp.route('/study/<int:level>', methods=['GET'])
def study(level):    
    words = getDBWordsForStudy(level)
    if words is None:
        return redirect(url_for("study.levelCompleted"))

    currWord = words[0]
    return render_template('study/studyVocab.html', studyWord = currWord, currLevel = level)


@bp.route('/study/addStudiedWord', methods=['POST'])
def addStudiedWord():
    print("Studied word called")
    id = request.args.get('id')
    print(id)
    addStudiedWordToDB(id)
    return ('', 204)

@bp.route('/study/studyTableRecords', methods=['GET'])
def studyTableRecords():
    db = get_db()
    words = db.execute(
        'SELECT * FROM studiedVocab'
        ' LEFT JOIN coreJpDict ON studiedVocab.dict_id = coreJpDict.id'
    ).fetchall()
    return render_template('study/studyRecords.html', records = words)
    
        
    


    

