##### FLYWHEEL META DATA MANIPULATION + GEAR RUNNING + QA DOWNLOADING ####


# Sarah Hennessy 2020

# This script does the following :
## 1. Goes into flywheel, sets the 'intent' of all functional scans to "functional" (necessary for gears in flywheel)
## 2. Runs the MRIQC gear for all relevant scans
## 3. Downloads the qa.html files and sorts them appropriately
## 4. Scrapes the html file and puts the relevant DVARS and FD values in a nice spreadsheet

## Also, see  "school_motion_report_flywheel.py"


# For this script you need the appropriate api key which can be found on the flywheel website

import flywheel
from pprint import pprint
import pandas as pd
import time

sectionColor = "\033[94m"
sectionColor2 = "\033[96m"
groupColor = "\033[90m"
mainColor = "\033[92m"

pink = '\033[95m'
yellow = '\033[93m'
red = '\033[91m'

ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

outpath = input("Drag in where you want your QA files to go!: ")

api_key = input('Please input your Flywheel API Key: ')
fw = flywheel.client(api_key)

gear = fw.lookup('gears/mriqc')

proj = input("Please input your flywheel group and project in the following format 'group/project': ")
result = fw.resolve(proj)
project = result.path[-1]

for el in result.children:

        print('%s: %s' % (el.label, el.id))
        subject = fw.get(el.id)

        if el.label.startswith('5'):
            subj_path = outpath + "Gr5/Baseline/" + el.label
        elif el.label.startswith('2'):
            subj_path = outpath + "Gr2/Baseline/" + el.label

        stopcount = 0
        midcount = 0
        for session in subject.sessions():
            print(sectionColor + 'Opening %s: %s' % (session.id, session.label))
            session = fw.get(session.id)

            for acquisition in session.acquisitions():
                if acquisition.label == 'StopSignal' or acquisition.label == 'MID':
                    print(sectionColor2 + 'Fixing intent for %s: %s' %(el.label,acquisition.label))
                    acquisition = fw.get(acquisition.id)
                    dicom = acquisition.files[0].name
                    acquisition.replace_file_classification(dicom, {'Intent': ['Functional']}, modality='MR')
                    nifti = acquisition.files[1].name
                    acquisition.replace_file_classification(nifti, {'Intent': ['Functional']}, modality='MR')

                    print(yellow + 'starting MRIQC gear for %s: %s' %(el.label,acquisition.label))
                    inputs = {'nifti': acquisition.get_file(nifti)}
                    config = {}
                    job_id = gear.run(inputs=inputs, destination=acquisition)

                    print(red + "Waiting for gear to finish......")

                    timeout = time.time() + 1200
                    while len(acquisition.files) < 3:
                        if time.time() > timeout:
                            print(red + 'QA FAILED! TIMED OUT! MOVING ON.')
                            break
                    else:
                        print(acquisition.local_timestamp.isoformat())

                        if acquisition.label == 'StopSignal':
                            stopcount = stopcount + 1
                            run = str(stopcount)
                            filelab = subj_path + "/stop_run%s.html" %(run)

                        elif acquisition.label == "MID":
                            midcount = midcount + 1
                            run = str(midcount)
                            filelab = subj_path + "/MID_run%s.html" %(run)

                        print(mainColor + "Downloading qa html file for %s, run %s" %(el.label, run, acquisition.label))
                        wnatfile = acquisition.files[3].name
                        acquisition.download_file(wantfile, filelab)

print(sectioncolor + "All files that ran are now in your qafile folder")

command ="Volumes/MusicProject/School_Study/Data/Functional/motion_reports/school_motion_report_flywheel.py"
print(command)
call(command,shell = True)

print(sectioncolor + "MRIQC values are now in the spreadsheet! Take a look :)")
