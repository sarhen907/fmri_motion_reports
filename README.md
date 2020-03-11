# fmri_motion_reports
DVARS from flywheel and FSL motion report (abs/rel motion) compiler from .html files

flywheel_magic.py: reformats metadata from functional scans so that they are appropriately read by flywheel, runs the MRIQC gear, downloads qa.html files [for each subject in a project]. an api-key is needed to run this script. It also runs school_motion_report_flywheel.py, which scrapes the html file and puts relevant data into a spreadsheet. 

Motion_reports scripts: 
These scripts take .html files from either flywheel .qa files, or motion reporting from FSL FEATs and extract motion information.
Output is a separate CSV for each format.
These scripts can be run independently. 
Currently formatted for the Brain & Music Lab's school study baseline gr5 Stop Signal and MID task. 
Tasks are compiled into the same csv. 

