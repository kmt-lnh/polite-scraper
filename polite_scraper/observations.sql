-- DDL to create db that holds observations over time

CREATE TABLE observations (
       id INTEGER PRIMARY KEY,
       company TEXT,
       jobid TEXT,
       jobtitle TEXT,
       jobdescription TEXT,
       firstobserved TEXT -- date on which record was created
);
