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

outfilename = "/Volumes/MusicProject/School_Study/Data/Functional/motion_reports/Gr5/Baseline/"+ "dvars2.csv"

data = pd.DataFrame()
data['ID'] = ''
data['task']=''
data['run'] = ''
data['dvars_max'] = ''
data['dvars_mean'] = ''
data['dvars_variance'] = ''
data['FD_max'] = ''
data['FD_mean'] = ''
data['FD_variance'] = ''


subjectDir = "/Volumes/MusicProject/School_Study/Data/Functional/qa_files/Gr5/Baseline/"
subjectList = [elem for elem in os.listdir(subjectDir) if "." not in elem]
subjectList.sort()

for subj in subjectList:

	subject = subj
	subjfolder = subjectDir + subject + "/"

	files = [elem for elem in os.listdir(subjfolder) if ".html" in elem]

	for file in files:
		if "stop" in file:
			task = "stop"
		elif "MID" in file:
			task = "MID"
		else:
			continue
		run = file[len(file)-6:len(file)-5]
		filename = subjfolder + '%s_run%s.html' %(task,run)

		# count = count + 1
		# index = str(count)
		textfilename = subjfolder + "%s_run%sqa_text.txt" %(task,run)
		textfile1 = open(filename,'r')
		filetext1 = textfile1.read()
		filetext1 = str(filetext1)
		file1 = open(textfilename,"w")
		file1.write(filetext1)
		file1.close()
		file1 = open(textfilename,"r")
		filetext1 = file1.read()
		start1 = filetext1.find("DVARS -->")
		myselect1 = filetext1[start1:]


		myvals1 = re.findall(r'max:(.*) ',myselect1)
		myvals1 = str(myvals1)
		dvarsmax1 = myvals1[:myvals1.index("$")]
		dvarsmax1 = dvarsmax1[3:len(dvarsmax1)-1]

		mmmax1 = re.search("(.*)mm", myvals1)
		mmmax1 = myvals1[:myvals1.index("mm")]
		FDmax1 = mmmax1[67:]

		mymeans1 = re.findall(r'mean:(.*) ',myvals1)
		mymeans1 = str(mymeans1)
		dvarsmean1 = mymeans1[:mymeans1.index("$")]
		dvarsmean1 = dvarsmean1[3:len(dvarsmean1)-1]

		FDmean1 = re.search('mean: (.*)mm',mymeans1)
		FDmean1st = str(FDmean1)
		FDmeanie = FDmean1st[:FDmean1st.index("mm")]
		FDmean1 = FDmeanie[46:]

		myvars1 = re.findall(r'sigma(.*)',myvals1)
		myvars1 = str(myvars1)
		myvars1_first = myvars1[myvars1.index(":"):myvars1.index(",")]
		dvars_sigma1 = myvars1_first[2:len(myvars1_first)-1]

		myvars1_second = myvars1[myvars1.index("sigma$:"):]
		FD_sigma1 = myvars1_second[8:len(myvars1_second)-5]

		textfile1.close()
		print(red + "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s%s" %(subject,run,dvarsmax1,dvarsmean1,dvars_sigma1,FDmax1,FDmean1,FD_sigma1,mainColor))

		data = data.append({"ID": subj, "task": task,"run": run,"dvars_max":dvarsmax1, "dvars_mean":dvarsmean1, "dvars_variance": dvars_sigma1, "FD_max": FDmax1, "FD_mean": FDmean1,"FD_variance": FD_sigma1}, ignore_index=True)


data.to_csv(outfilename,index =False)
