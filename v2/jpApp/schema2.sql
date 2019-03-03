-- Remove the drop table line later on.
DROP TABLE IF EXISTS studiedVocab;
DROP TABLE IF EXISTS coreJpDict;

CREATE TABLE studiedVocab (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 dict_id INTEGER,
 dateRevised TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 revisable BIT NOT NULL DEFAULT 1,
 stability FLOAT NOT NULL DEFAULT 1.0,
 FOREIGN KEY (dict_id) REFERENCES coreJpDict (id)
);


CREATE TABLE coreJpDict (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 jpWord TEXT NOT NULL,
 pronunciation TEXT NOT NULL,
 meaning TEXT NOT NULL,
 jpSentence TEXT NOT NULL,
 enSentence TEXT NOT NULL,
 wordLevel INTEGER NOT NULL
);
