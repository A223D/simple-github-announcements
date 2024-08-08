'''

This script should be invoked when a new announcement is triggered. 

1. Take the data from the newannouncement

Run XML linter on 

Last. Reset new announcement script to the standard template given in templates. 


'''
import sys
import xml.etree.ElementTree as ET
import os
import shutil

announcementsBranchLocation = "./announcementsBranch/"

announcementData = ET.Element('item')

tempAnnouncementDict = {}

announcementKeys = {
    "title",
    "link",
    "description",
    "topic",
    "topic description",
    "language",
    "managing editor"
}

debug = True

newAnnouncementFileObject = open(sys.argv[1])
announcementLines = newAnnouncementFileObject.readlines()

#newAnnouncement file parser
for line in announcementLines:
    #find the first colon in this line
    index = line.find(":")

    #ignore line that does not have colon
    if index < 0:
        continue

    #split string via first colon
    key = line[:index].strip().lower() #strip removes leading and trailing whitespaces
    data = line[index+1:].strip() #strip removes leading and trailing whitespaces
    if debug: print("The key I got was", key)
    if debug: print("The data I got was", data)

    if key not in announcementKeys:
        if debug: print(key, "was not a recognised key for an announcement")
        continue
    
    tempAnnouncementDict[key] = data

if debug: print(tempAnnouncementDict)

#now check if the topic file already exists for this announcement
if "topic" not in tempAnnouncementDict:
    raise ValueError("This announcement does not have a topic")

if debug: print("Now checking if", os.path.join(announcementsBranchLocation, tempAnnouncementDict["topic"] + ".xml"), "exists")

if not os.path.isfile(os.path.join(announcementsBranchLocation, tempAnnouncementDict["topic"] + ".xml")):
    if debug: print("The topic file does not exist. Creating it now")
    #create the file from the static template given and close it
    shutil.copyfile("./mainBranch/templates/emptyRSSFile.xml", os.path.join(announcementsBranchLocation, tempAnnouncementDict["topic"] + ".xml"))

    #check if we have all the basic data needed to create this topic file
    
    #open the file and feed basic data

#from here, you can assume that the file is present, build the item object and attach it

#replace newAnnouncements.txt content from the file given in templates
# if debug: print("Removing file")
#if not debug: os.remove(newAnnouncement.txt)

# shutil.copyfile("./templates/newAnnouncementTemplate.txt", "./newAnnouncement.txt")
