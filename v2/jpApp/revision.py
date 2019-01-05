from flask import (Blueprint, render_template, g, redirect, url_for, flash, request)
from jpApp.db import get_db
from datetime import datetime
import math
bp = Blueprint("revision", __name__)

@bp.route('/test', methods=('GET','POST'))
def test():
    
    if request.method == 'POST':
        meaning = request.form['meaning']
        pronunciation = request.form['pronunciation']
        error = None

        if not meaning:
            error = "Please enter the meaning of the word."
        if not pronunciation:
            error = "Please enter the pronunciation of the word in romaji."
            
        if error is not None:
            flash(error) 
        else:
            #get words for testing.
            testVocab = getDBWordsForTest()
            
            #there are no words for revising right now.
            if testVocab is None:
                #TODO: Add a page to tell users that they have fully revised.
                return redirect(url_for("main.wordList"))                

            currWord = testVocab[0]

            #check correct or not.
            correct = checkInput(meaning, pronunciation, currWord)

            #TODO: Bad code structure, better to make 2 functions: 1 for wrong, 1 for correct.
            updateRevisionDB(currWord, correct)
            print("Input meaning: " + meaning)
            print("Input prc: " + pronunciation)

    #I need to pull from db here again... --After the updates.
    testVocab = getDBWordsForTest()
    if testVocab is None:
        #TODO: Add a page to tell users that they have fully revised.
        return redirect(url_for("main.wordList"))                        

    currWord = testVocab[0]

    for word in testVocab:
        print(word['jpWord'] + " meaning: " + word['meaning'] + " prc: " + word['pronunciation'] + " stability: " + str(word['stability']))

    return render_template('revision/testVocab.html', testWord = currWord)

def checkInput(inputMeaning, inputPrc, dbWord):
    wrong = False
    if inputMeaning != dbWord['meaning']:
        print("Input Meaning: " + str(inputMeaning) + " db meaning: " + str(dbWord['meaning']))
        wrong = True
        print("meaning mismatch")
    if inputPrc != dbWord['pronunciation']:
        print("Input Prc: " + str(inputPrc) + " db prc: " + str(dbWord['pronunciation']))        
        wrong = True
        print("prc mismatch")
    return not wrong

def updateRevisionDB(word, correct):
    db = get_db()
    learntDate = word['dateRevised']
    currDate = datetime.now()
    daysElapsed = (currDate - learntDate).days + 1
    print("Correct: " + str(correct))
    if correct:
        #*2 our stability.
        currS = word['stability']
        newS = currS * 2

    else:
        #if its wrong, we need to drop the stability so that it pops up slightly more frequently.
        #we assume that our memory retainment of this word is now 0.05, we get our S accordingly.
        newS = getS(0.05, daysElapsed)

    #check whether its revisable.
    memoryRet = getR(newS, daysElapsed)
    print("Memory ret: " + str(memoryRet) + " word is: "+ word['jpWord'])
    if isRevisable(memoryRet):
        revisable = 1
    else:
        revisable = 0
        

    db.execute(
        'UPDATE jpVocab SET stability = ?, revisable = ?'
        ' WHERE id = ?',
        (newS, revisable, word['id'])
    )
    db.commit() 
    print("updated db from revision")

def getDBWordsForTest(): 
    db = get_db()
    #get test words.
    testVocab = db.execute(
        'SELECT * FROM jpVocab'
        ' WHERE revisable = 1'
        ' ORDER BY stability ASC'
    ).fetchall()

    if len(testVocab) == 0:
        return None

    return testVocab
   
    
#--- Maths functions to compute stabiltiy / retainment.
def getS(r, t):
    ln = math.log
    return ( -1 * (t/ln(r)) )

def getR(s, t):
    e = math.exp
    r = e(-1*t/s)
    
    return r
        
def isRevisable(r):
    return r < 0.50
'''
if fail the test, set retainment to 0.05, compute s with getS
if pass the test, double stability value, compute r with getR

Our ideal stability value would be 512, if we hit 512, then it will take 1 year for us to retest.
'''
