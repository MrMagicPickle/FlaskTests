"use strict";

function updateStudyDb() {
    console.log("hey");
    let req = new XMLHttpRequest();
    let query = "id=" + id;

    
    req.open('POST', 'http://localhost:5000/study/addStudiedWord?'+query, true);
    req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    req.onload = function(data, code) {
	console.log(code);
	console.log("callback");
    }
    req.send(query);    
    
}

function loadPage(url) {
    let req = new XMLHttpRequest();
    req.open('GET', url, true);
    req.send();
    return req.responseText;
}



function goNext() {
    updateStudyDb('http://localhost:5000/study/' + level);
    let doc = document.getElementById("mainContainer");
    doc.innerHTML = loadPage()
}
