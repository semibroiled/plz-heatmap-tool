# plz-heatmap-tool

python -m main hm --load TRUE 

This runs from the savefile

Issues are:

To add other workflows;
Add Unit Tests

# General

To run this tool, there are still a couple of extra steps you have to perform.
Hopefully this gets chalked up to automation and deployment later down the line.

First off, get a csv version of the seminar gesamt liste in its current iteration as a csv file.

The name convention i use for this file is __Seminargesamtliste__0923

with 09 being month, 23 being year, of current iteration

Save this CSV file with all its columns in the data directory.

Next, we need to treat it appropraitely to run it in main.

I am currently using the jupyter prototype for this. Run the code as is, if its the first time a file is being treated, and watch out to put in its name where required. Then, transform the the data.

This is the ETL pipeline in the making.

Transformation can ask for some changes to column names. best to take care of a convention from csv conversion point.

run all jupyter steps to save as a pickle file.

then run command on main for appropriat epickle file

current version is working on the test venv

have to append stuff to make it work in a main env

also add markers on key cities for later update

