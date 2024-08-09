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

keysRequiredForNewTopic = {
    "topic",
    "topic description",
    "language",
    "managing editor"
}

def checksForNewTopic():
    for keyNeeded in keysRequiredForNewTopic:
        if keyNeeded not in tempAnnouncementDict:
            raise ValueError(keyNeeded, "is required and not given")
            return False
        
    return True
    

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

topicFilePath = os.path.join(announcementsBranchLocation, tempAnnouncementDict["topic"] + ".xml")

if debug: print("Now checking if", topicFilePath, "exists")

if not os.path.isfile(topicFilePath):
    if debug: print("The topic file does not exist. Creating it now")
    
    #create the file from the static template given and close it
    shutil.copyfile("./mainBranch/templates/emptyRSSFile.xml", topicFilePath)

    #check if we have all the basic data needed to create this topic file
    if not checksForNewTopic():
        raise ValueError("All fields required for a new topic are not present")
    #open the file and feed basic data
    newFileTree = ET.parse(topicFilePath)
    root = newFileTree.getroot()
    channel = root.find("channel")

    #assign title
    channel.find("title").text = tempAnnouncementDict["topic"]
    if debug: print("Assigned title(topic) to", channel.find("title").text)

    #assign topic link
    if "topic link" in tempAnnouncementDict:
        channel.find("link").text = tempAnnouncementDict["topic link"]
    else:
        channel.find("link").text = "https://raw.githubusercontent.com/"+os.environ["REPO_OWNER"]+"/"+os.environ["REPO_NAME"].split('/')[1]+"/announcements/"+tempAnnouncementDict["topic"]+".xml"
    if debug: print("Assigned link to", channel.find("link").text)

    #assign topic description
    channel.find("description").text = tempAnnouncementDict["topic description"]
    if debug: print("Assigned topic description to", channel.find("description").text)

    #assign language
    channel.find("language").text = tempAnnouncementDict["language"]
    if debug: print("Assigned language to", channel.find("language").text)

    #assign pubDate and build date
    #TBD

    #assign docs
    channel.find("docs").text = "https://www.rssboard.org/rss-specification"
    if debug: print("Assigned docs to", channel.find("docs").text)

    #assign managing editor
    channel.find("managingEditor").text = tempAnnouncementDict["managing editor"]
    if debug: print("Assigned managing editor to", channel.find("managingEditor").text)

    #assign webmaster
    channel.find("webMaster").text = os.environ["REPO_OWNER"]
    if debug: print("Assigned webMaster to", channel.find("webMaster").text)

    newFileTree.write(topicFilePath)

#from here, you can assume that the file is present, build the item object and attach it

#replace newAnnouncements.txt content from the file given in templates
# if debug: print("Removing file")
#if not debug: os.remove(newAnnouncement.txt)

# shutil.copyfile("./templates/newAnnouncementTemplate.txt", "./newAnnouncement.txt")
