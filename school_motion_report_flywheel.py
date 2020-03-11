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

outfilename = "/Volumes/MusicProject/School_Study/Data/Functional/motion_reports/Gr5/Baseline/"+ "dvars.csv"

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


	filename = subjfolder + 'stop_run1.html'
	filename2 = subjfolder + 'stop_run2.html'
	filename3 = subjfolder + 'MID_run1.html'
	filename4 = subjfolder + 'MID_run2.html'



	if os.path.exists(filename):

		count = count + 1
		index = str(count)
		textfilename = subjfolder + "stop_run1qa_text.txt"
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
		FDmax1 = mmmax1[68:]

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
		print(red + "%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s%s" %(subject,1,dvarsmax1,dvarsmean1,dvars_sigma1,FDmax1,FDmean1,FD_sigma1,mainColor))

		data = data.append({"ID": subj, "task": "stop","run": '1',"dvars_max":dvarsmax1, "dvars_mean":dvarsmean1, "dvars_variance": dvars_sigma1, "FD_max": FDmax1, "FD_mean": FDmean1,"FD_variance": FD_sigma1}, ignore_index=True)




	else:
		print(sectionColor + "No QA file for %s%s stop signal run1"  %(subject,mainColor))




	if os.path.exists(filename2):

		textfilename2 = subjfolder + "stop_run2qa_text.txt"
		textfile2 = open(filename2,'r')
		filetext2 = textfile2.read()
		filetext2 = str(filetext2)
		file2 = open(textfilename2,"w")
		file2.write(filetext2)
		file2.close()
		file2 = open(textfilename2,"r")
		filetext2 = file2.read()
		start2 = filetext2.find("DVARS -->")
		myselect2 = filetext2[start2:]


		myvals2 = re.findall(r'max:(.*) ',myselect2)
		myvals2 = str(myvals2)
		dvarsmax2 = myvals2[:myvals2.index("$")]
		dvarsmax2 = dvarsmax2[3:len(dvarsmax2)-1]

		mmmax2 = re.search("(.*)mm", myvals2)
		mmmax2 = myvals2[:myvals2.index("mm")]
		FDmax2 = mmmax2[68:]

		mymeans2 = re.findall(r'mean:(.*) ',myvals2)
		mymeans2 = str(mymeans2)
		dvarsmean2 = mymeans2[:mymeans2.index("$")]
		dvarsmean2 = dvarsmean2[3:len(dvarsmean2)-1]

		FDmean2 = re.search('mean: (.*)mm',mymeans2)
		FDmean2st = str(FDmean2)
		FDmeanie = FDmean2st[:FDmean2st.index("mm")]
		FDmean2 = FDmeanie[46:]

		myvars2 = re.findall(r'sigma(.*)',myvals2)
		myvars2 = str(myvars2)
		myvars2_first = myvars2[myvars2.index(":"):myvars2.index(",")]
		dvars_sigma2 = myvars2_first[2:len(myvars2_first)-1]

		myvars2_second = myvars2[myvars2.index("sigma$:"):]
		FD_sigma2 = myvars2_second[8:len(myvars2_second)-5]

		textfile2.close()
		print(red + "%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s%s" %(subject,2,dvarsmax2,dvarsmean2,dvars_sigma2,FDmax2,FDmean2,FD_sigma2,mainColor))

		data = data.append({"ID": subj, "task": "stop","run": '2',"dvars_max":dvarsmax2, "dvars_mean":dvarsmean2, "dvars_variance": dvars_sigma2, "FD_max": FDmax2, "FD_mean": FDmean2,"FD_variance": FD_sigma2}, ignore_index=True)



	else:
		print(sectionColor + "No QA file found for %s%s stop signal run2"  % (subject,mainColor))

	if os.path.exists(filename3):

		count = count + 1
		index = str(count)
		#read in the data from the motion report file 1
		textfilename = subjfolder + "MID_run1qa_text.txt"
		textfile1 = open(filename3,'r')
		filetext1 = textfile1.read()
		filetext1 = str(filetext1)
		file1 = open(textfilename,"w")
		file1.write(filetext1)
		file1.close()
		file1 = open(textfilename,"r")
		filetext1 = file1.read()
		start1 = filetext1.find("DVARS -->")
		myselect1 = filetext1[start1:]


		# newfile = html2text.html2text(filetext)
		# file1 = open("myhtmltext.txt","a")
		# file1.write(newfile)
		# file1.close()
		# file1 = open("myhtmltext.txt","r")
		# filetext = file1.read()

		myvals1 = re.findall(r'max:(.*) ',myselect1)
		myvals1 = str(myvals1)
		dvarsmax1 = myvals1[:myvals1.index("$")]
		dvarsmax1 = dvarsmax1[3:len(dvarsmax1)-1]

		mmmax1 = re.search("(.*)mm", myvals1)
		mmmax1 = myvals1[:myvals1.index("mm")]
		FDmax1 = mmmax1[68:]

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
		print(red + "%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s%s" %(subject,1,dvarsmax1,dvarsmean1,dvars_sigma1,FDmax1,FDmean1,FD_sigma1,mainColor))

		data = data.append({"ID": subj, "task": "MID","run": '1',"dvars_max":dvarsmax1, "dvars_mean":dvarsmean1, "dvars_variance": dvars_sigma1, "FD_max": FDmax1, "FD_mean": FDmean1,"FD_variance": FD_sigma1}, ignore_index=True)
		# newdf['ID'][index] = subj
		# newdf['run'][index] = 1
		# newdf['abs_motion'][index] = motion_ab1
		# newdf['rel_motion'][index] = motion_rel1



	else:
		print(sectionColor + "No QA file for %s%s MID run1"  %(subject,mainColor))




	if os.path.exists(filename4):

		textfilename2 = subjfolder + "MID_run2qa_text.txt"
		textfile2 = open(filename4,'r')
		filetext2 = textfile2.read()
		filetext2 = str(filetext2)
		file2 = open(textfilename2,"w")
		file2.write(filetext2)
		file2.close()
		file2 = open(textfilename2,"r")
		filetext2 = file2.read()
		start2 = filetext2.find("DVARS -->")
		myselect2 = filetext2[start2:]


		myvals2 = re.findall(r'max:(.*) ',myselect2)
		myvals2 = str(myvals2)
		dvarsmax2 = myvals2[:myvals2.index("$")]
		dvarsmax2 = dvarsmax2[3:len(dvarsmax2)-1]

		mmmax2 = re.search("(.*)mm", myvals2)
		mmmax2 = myvals2[:myvals2.index("mm")]
		FDmax2 = mmmax2[68:]

		mymeans2 = re.findall(r'mean:(.*) ',myvals2)
		mymeans2 = str(mymeans2)
		dvarsmean2 = mymeans2[:mymeans2.index("$")]
		dvarsmean2 = dvarsmean2[3:len(dvarsmean2)-1]

		FDmean2 = re.search('mean: (.*)mm',mymeans2)
		FDmean2st = str(FDmean2)
		FDmeanie = FDmean2st[:FDmean2st.index("mm")]
		FDmean2 = FDmeanie[46:]

		myvars2 = re.findall(r'sigma(.*)',myvals2)
		myvars2 = str(myvars2)
		myvars2_first = myvars2[myvars2.index(":"):myvars2.index(",")]
		dvars_sigma2 = myvars2_first[2:len(myvars2_first)-1]

		myvars2_second = myvars2[myvars2.index("sigma$:"):]
		FD_sigma2 = myvars2_second[8:len(myvars2_second)-5]

		textfile2.close()
		print(red + "%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s%s" %(subject,2,dvarsmax2,dvarsmean2,dvars_sigma2,FDmax2,FDmean2,FD_sigma2,mainColor))

		data = data.append({"ID": subj, "task": "MID","run": '2',"dvars_max":dvarsmax2, "dvars_mean":dvarsmean2, "dvars_variance": dvars_sigma2, "FD_max": FDmax2, "FD_mean": FDmean2,"FD_variance": FD_sigma2}, ignore_index=True)



	else:
		print(sectionColor + "No QA file found for %s%s  MID run2"  % (subject,mainColor))


	data.to_csv(outfilename,index =False)
