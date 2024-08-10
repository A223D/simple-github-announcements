'''
This script should be invoked when a new announcement is triggered. 

1. Parse the data from the newannouncement file and generate a dictionary containing the information.

2. Run check to see if all keys requires are provided and create a new announcement file(if needed)

3. Create the new announcement.

4. Run XML linter on the new annoucement file. 
'''

import sys
import xml.etree.ElementTree as ET
import os
import shutil
import datetime

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
    "managing editor",
    "topic link"
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
    if len(line) == 0 or line[0] == "#":
        continue
    #find the first colon in this line
    index = line.find(":")

    #ignore line that does not have colon
    if index < 0:
        continue

    #split string via first colon
    key = line[:index].strip().lower().replace("*", "") #strip removes leading and trailing whitespaces, also removing asterisks
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
    dateTimeString = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %Z") #for eg Tue, 10 Jun 2003 04:00:00 GMT
    channel.find("pubDate").text = dateTimeString
    if debug: print("Assigned pubDate to", channel.find("pubDate").text)
    channel.find("lastBuildDate").text = dateTimeString
    if debug: print("Assigned lastBuildDate to", channel.find("lastBuildDate").text)

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

#check if file is over 10 KB. Implement file splitting later
if os.path.getsize(topicFilePath) > 10000:
    raise RuntimeError("The announcement file is too large. Delete it and try again.")

#from here, you can assume that the file is present(under limit), build the item object and attach it
rssFileTree = ET.parse(topicFilePath)
rssFileRoot = rssFileTree.getroot()
rssFileChannel = rssFileRoot.find("channel")

newAnnouncementItem = ET.SubElement(rssFileChannel, 'item')

if 'title' not in tempAnnouncementDict and 'description' not in tempAnnouncementDict:
    raise ValueError("An announcement must have a title or a description")

#add title
newAnnouncementTitle = ET.SubElement(newAnnouncementItem, 'title')
newAnnouncementTitle.text = tempAnnouncementDict['title']

#add description
newAnnouncementDescription = ET.SubElement(newAnnouncementItem, 'description')
newAnnouncementDescription.text = tempAnnouncementDict.get("description", "")

#add link
newAnnouncementLink = ET.SubElement(newAnnouncementItem, 'link')
newAnnouncementLink.text = tempAnnouncementDict.get('link', "https://raw.githubusercontent.com/"+os.environ["REPO_OWNER"]+"/"+os.environ["REPO_NAME"].split('/')[1]+"/announcements/"+tempAnnouncementDict["topic"]+".xml")

#add author
newAnnouncementAuthor = ET.SubElement(newAnnouncementItem, 'author')
newAnnouncementAuthor.text = os.environ["ANNOUNCER"]

#set the pubDate and the latest buildDate
dateTimeString = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %Z") #for eg Tue, 10 Jun 2003 04:00:00 GMT
newAnnouncementPubDate = ET.SubElement(newAnnouncementItem, 'pubDate')
newAnnouncementPubDate.text = dateTimeString
rssFileChannel.find("lastBuildDate").text = dateTimeString

#write the file
rssFileTree.write(topicFilePath)

#run the linter - Think about how to move this from the parser script to workflow
os.system("cat \""+topicFilePath+"\" | xmllint --format - | tee \""+topicFilePath+"\"")