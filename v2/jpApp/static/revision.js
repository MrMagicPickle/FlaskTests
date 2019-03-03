"use strict";




function processInput() {
    console.log("hi");
    let userMeaning = document.getElementById("meaning").value;
    let userPrc = document.getElementById("pronunciation").value;

    //Make an API call.
    let req = new XMLHttpRequest();
    let query = "userMeaning=" + userMeaning;
    query += "&userPrc=" + userPrc;
    query += "&jpWord=" + jpWord;
    
    req.open('GET', 'http://localhost:5000/revision/processUserInput?'+query, true);
    req.onload = editHTMLBasedOnInput;  
    req.send();
}

function editHTMLBasedOnInput(data, code) {
    console.log(data);
    console.log("edit html based on input callback called");
    let validInput = JSON.parse(data.target.response).validInput;

    // We can do edit the html DOM here.

    if (validInput) {
	correctAnsEdit();
    } else {
	wrongAnsEdit();
    }
    //Show the "Next" button.
    document.getElementById("nextBtnContainer").style.display = "block";

    //Hide the "Submit" button.
    document.getElementById("submitBtn").style.display = 'none';
}



function correctAnsEdit() {
    let containerDiv = document.getElementById("mainContainer");	    
    containerDiv.style.backgroundColor = "lightblue";		    
}

function wrongAnsEdit() {
    let containerDiv = document.getElementById("mainContainer");
    containerDiv.style.backgroundColor = "red";

    displayTrueInfo();
}

function displayTrueInfo() {
    let btnDiv = document.getElementById("nextBtnContainer");
    // Just to make sure.
    if (btnDiv.style.display !== "block") btnDiv.style.display = "block";

    let req = new XMLHttpRequest();
    let query = "jpWord=" + jpWord;
    req.open('GET', 'http://localhost:5000/getJpWordInfo?'+query, true);
    req.onload = function(data, code) {
	console.log("in displaytrueinfo function");
	console.log(data);
	let res = JSON.parse(data.target.response);
	let trueMeaning = res.meaning;
	let truePrc = res.prc;	
	let trueJpInfoDiv = document.getElementById("trueJpInfo");
	trueJpInfoDiv.style.display = "block";
	trueJpInfoDiv.style.backgroundColor = "darkgreen";
	let meaningRef = getElem("trueMeaning");
	let prcRef = getElem("truePrc");
	meaningRef.innerHTML = trueMeaning;
	prcRef.innerHTML = truePrc;	
	
    };
    req.send();
    
}

function getElem(id) {
    return document.getElementById(id);
}

