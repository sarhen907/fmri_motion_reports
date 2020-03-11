#!/usr/bin/env python

import os,sys
#from commando import commando
#from commando import writeToLog
import argparse
import numpy as np
import re
from datetime import datetime
from subprocess import call
from subprocess import check_output
import csv
import pandas as pd

#set analysis values

numconfounds = 8
smoothmm = 5	#smoothing sigma fwhm in mm
smoothsigma = smoothmm/2.3548	#convert to sigma
additive = 10000	#value added to distinguish brain from background
brightnessthresh = additive * .75


#logging colors
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


count = 0
outfilename = "/Volumes/MusicProject/School_Study/Data/Functional/motion_reports/Gr5/Baseline/"+ "fsl.csv"

colnames = ['ID','task','run','abs_motion', "rel_motion"]
newdf = pd.DataFrame(columns = colnames)

taskList = ['stop','MID']
groupList = ['Control','Music']
for task in taskList:
	for group in groupList:
		subjectDir = "/Volumes/MusicProject/School_Study/Data/Functional/func_analysis_3.1thresh/Gr5/Baseline_%s/%s/" %(task,group)
		subjectList = [elem for elem in os.listdir(subjectDir) if "." not in elem]
		subjectList.sort()
		for subj in subjectList:
			subject = subj
			subjfolder = subjectDir + subject + "/"
			feat1 = subjfolder + 'firstlevel_%s_run1.feat' %(task)
			feat2 = subjfolder + 'firstlevel_%s_run2.feat' %(task)
			filename = feat1 + '/report_prestats.html'
			filename2 = feat2 + '/report_prestats.html'

			if os.path.exists(filename):
				count = count + 1
				index = str(count)
				#read in the data from the motion report file 1
				textfile = open(filename,'r')
				filetext = textfile.read()
				textfile.close()
				#find absolute motion
				result_ab1 = re.search('absolute=(.*)mm,',filetext)
				motion_ab1 = result_ab1.groups()[0]
				#find relative motion
				result_rel1= re.search('relative=(.*)mm',filetext)
				motion_rel1 = result_rel1.groups()[0]
				print(red + "%s\t%s\t%d\t%s\t%s%s" %(subject,task,1,motion_ab1,motion_rel1,mainColor))

				newdf = newdf.append({"ID":subj, "task": task, "run":'1', "abs_motion": motion_ab1, "rel_motion": motion_rel1}, ignore_index=True)
				# newdf['ID'][index] = subj
				# newdf['run'][index] = 1
				# newdf['abs_motion'][index] = motion_ab1
				# newdf['rel_motion'][index] = motion_rel1


			else:
				print(sectionColor + "No FEAT1 folder found for %s %s%s"  %(task,subject,mainColor))




			if os.path.exists(filename2):
				count = count + 1
				index = str(count)
				#read in the data from the motion report file 2
				textfile2 = open(filename2,'r')
				filetext2 = textfile2.read()
				textfile2.close()
				#find absolute motion
				result_ab2 = re.search('absolute=(.*)mm,',filetext2)
				motion_ab2 = result_ab2.groups()[0]
				#find relative motion
				result_rel2 = re.search('relative=(.*)mm',filetext2)
				motion_rel2 = result_rel2.groups()[0]
				print(red + "%s\t%s\t%d\t%s\t%s%s" %(subject,task,2,motion_ab2,motion_rel2,mainColor))

				newdf = newdf.append({"ID":subj,"task": task, "run":'2', "abs_motion": motion_ab2, "rel_motion": motion_rel2},ignore_index=True)
				# newdf['ID'][index] = subj
				# newdf['run'][index] = 2
				# newdf['abs_motion'][index] = motion_ab2
				# newdf['rel_motion'][index] = motion_rel2
			else:
				print(sectionColor + "No FEAT2 folder found for %s %s%s"  % (task,subject,mainColor))


newdf.to_csv(outfilename,index =False)
