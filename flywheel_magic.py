##### FLYWHEEL META DATA MANIPULATION + GEAR RUNNING + QA DOWNLOADING/ exporting ####


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
import shutil
import os
from subprocess import call

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


for i in range(2):

    result = fw.resolve(proj)
    project = result.path[-1]

    for el in result.children:

            print('%s: %s' % (el.label, el.id))
            subject = fw.get(el.id)
            mylab = el.label[:len(el.label)-9]
            mylab = mylab + 'baseline'

            stopcount = 0
            midcount = 0

            if el.label.startswith('5'):
                subj_path = outpath + "Gr5/Baseline/" + mylab
            elif el.label.startswith('2'):
                subj_path = outpath + "Gr2/Baseline/" + mylab
            else:
                continue

            for session in subject.sessions():
                print(sectionColor + 'Opening %s: %s' % (session.id, session.label))
                session = fw.get(session.id)

                for acquisition in session.acquisitions():
                    if acquisition.label == 'StopSignal' or acquisition.label == 'MID':
                        print(sectionColor2 + 'Fixing intent for %s: %s' %(el.label,acquisition.label))
                        acquisition = fw.get(acquisition.id)

                        if i == 0:
                            dicom = acquisition.files[0].name
                            acquisition.replace_file_classification(dicom, {'Intent': ['Functional']}, modality='MR')
                            nifti = acquisition.files[1].name
                            acquisition.replace_file_classification(nifti, {'Intent': ['Functional']}, modality='MR')

                            print(yellow + 'starting MRIQC gear for %s: %s' %(el.label,acquisition.label))
                            inputs = {'nifti': acquisition.get_file(nifti)}
                            config = {}
                            job_id = gear.run(inputs=inputs, destination=acquisition)

                            print(red + "Waiting for gear to finish......")

                        elif i ==1:

                        # timeout = time.time() + 1200
                        # while len(acquisition.files) != 3:
                        #     if time.time() > timeout:
                        #         print(red + 'QA FAILED! TIMED OUT! MOVING ON.')
                        #         break
                        # else:
                        #     print(acquisition.local_timestamp.isoformat())

                            if acquisition.label == 'StopSignal':
                                stopcount = stopcount + 1
                                run = str(stopcount)
                                filelab = subj_path + "/stop_run%s.html" %(run)
                                file_ext = "stop_run%s.html" %(run)

                            elif acquisition.label == "MID":
                                midcount = midcount + 1
                                run = str(midcount)
                                filelab = subj_path + "/MID_run%s.html" %(run)
                                file_ext = "MID_run%s.html" %(run)
                            if len(acquisition.files) == 3:
                                print(mainColor + "Downloading qa html file for %s, run %s, %s" %(el.label, run, acquisition.label))
                                wantfile = acquisition.files[2].name
                                acquisition.download_file(wantfile,file_ext)
                                source = "/Volumes/MusicProject/School_Study/Data/Functional/motion_reports/%s" %(file_ext)
                                destination = subj_path
                                checkfile = subj_path + file_ext
                                if os.path.exists(filelab):
                                    print("QA already here! moving on")
                                    continue
                                else:
                                    dest = shutil.move(source,destination)
                            else:
                                print('NO QA FILE HERE. moving on.')

print(pink + "All files that ran are now in your qafile folder")

command ="Volumes/MusicProject/School_Study/Data/Functional/motion_reports/school_motion_report_flywheel.py"
print(command)
call(command,shell = True)

print(mainColor + "MRIQC values are now in the spreadsheet! Take a look :)")
