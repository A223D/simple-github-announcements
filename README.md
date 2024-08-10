# simple-github-announcements

`simple-github-announcements` is a project which aims to build a non-intrusive announcement system in the most easiest way to use possible.

> This repository serves as the "central server" for announcements and is meant to be forked. For a simple GitHub announcements client, visit [this repository(LINK TBD)🚧]().  

A pub-sub type architecture is used along with client polling to receive announcements to a local machine.

The prime directive of this project is to provide a way for people to subscribe to certain topics they want to receive information about and for selected people to be able to publish announcements on these topics.

The main goal for this project is to achieve the above with low(ideally 0) server costs, and as lightweight a polling client as possible, while still maintaining desirable functionality.

The idea is for people to be able to fork this repository and publish their own announcements, while using GitHub as a central server(to be able to serve a large audience) for free.

## Theory of Operation

Committing and pushing changes to the `newAnnouncements.txt` file will trigger a GitHub action workflow called `Announcer` to parse this file and convert it to an [RSS valid XML format](https://www.rssboard.org/rss-specification). This XML data will then be added to the respective topic XML file in the `announcements` branch and pushed.

Clients are expected to poll their chosen topic XML files(which are in the RSS format) hosted on GitHub to choose which announcements to display to the user. GitHub handles load balancing and serving these files to the clients.

There is a concern that clients will have to download ever-increasing topic files, but for now the limit of a topic file is capped at 10KB. In the future. This project may or may not support topic file splitting by date to make the load easier on client machines and GitHub.

## How to Use

1. Edit the `newAnnouncement.txt` file in the main branch to create a new announcement.

   * If this is a new topic or the very first announcement after forking, there is some additional information that should be included in this file, **along with the information in the next point**.

     * A description about this topic aka `Topic Description` (required)

     * [The language you will publish announcements in aka `Language`. This must be a valid language code as described here](https://www.rssboard.org/rss-language-codes). (required)

     * A link about this specific topic aka `Topic Link`. This can just be the link to all the announcements. (optional)

     * The person in-charge of the content aka `Managing Editor` (required)

   * If the topic you intend to publish to has had announcements before, then only the following information may be needed. There needs to be atleast a title or a description.

     * The topic aka `Topic` (required)

     * Title aka `Title` (optional if `Description` is present)

     * Description aka `Description` (optional if `Title` is present)

     * Link aka `Link` - This is where someone can go to find more information about the announcement. (optional)

     * Image support will be added in the future

    > The order in which the the information is provided does not matter, and extra information is ignored.

2. Once the announcement is ready, commit and push the file to the `main` branch.

3. Make sure any client(or RSS software) is pointed to the link for the auto-generated XML files. This will look somewhat like:
 

```
https://raw.githubusercontent.com/<username>/simple-github-announcements/announcements/<some topic>.xml
```

> If you choose to use the official client for `simple-github-announcements`, you will have the ability to point to multiple repositories and subscribe to certain topics within each of them.

## Examples of announcements

### Example of New Topic or First Announcement After Forking

Here is an example of a file which is creating a new topic and the first announcement for that topic.

```python
# Edit this file, commit, and push to trigger a new announcement. Comments start with #, so uncomment the relevant information.
# The required fields are marked with an asterisk(*)
# Order of information presented does not matter. 
# Here are the details needed for a new announcement to an existing topic:
# 
# Topic*:
# Title*:
# Description*:
# Link:
#
# Additional information required for a new topic
# Topic Description*:
# Language*:
# Topic Link:
# Managing Editor*:
#
# You can remove this guideline if needed, but it is recommended to keep it and just copy the above lines below

Topic*: Free Food
Topic Description*: This announcement chain tracks free food around the office.
Topic Link: https://www.businessinsider.com/free-food-silicon-valley-tech-employees-apple-google-facebook-2018-7
Language*: en-ca
Managing Editor*: Kushagra(example@email.com)
Title*: Left-over pizza on the 9th floor 🍕
Description*: FW team had an event so leftover pizza available on an FCFS basis
Link: https://www.menshealth.com/nutrition/a26149219/is-pizza-healthy/
```

### Example of a New Announcement to an Existing Topic

Here is an example of a file which is creating a new announcement for an existing topic.

```python
# Edit this file, commit, and push to trigger a new announcement. Comments start with #, so uncomment the relevant information.
# The required fields are marked with an asterisk(*)
# Order of information presented does not matter. 
# Here are the details needed for a new announcement to an existing topic:
# 
# Topic*:
# Title*:
# Description*:
# Link:
#
# Additional information required for a new topic
# Topic Description*:
# Language*:
# Topic Link:
# Managing Editor*:
#
# You can remove this guideline if needed, but it is recommended to keep it and just copy the above lines below

Topic*: Free Food
Title*: More left-over pizza on the 5th floor 🍕
Description*: HW team ordered too much...
Link: https://www.pmq.com/pizza-is-good-for-you/
```

## Misc.

### Trying to Change Topic Information Later

If you add information like `Topic Description`, `Language`, or `Managing Editor` to a new announcement to an existing topic, this information will be ignored. This type of information is set at the conception of a new topic and is **supposed to be immutable by design**. Functionality to delete a topic(and all of its announcements) will be added later on.

### What Happens When a Client Polls a topic with multiple previously published announcements for the first time?

This depends on the behaviour of the client, and is not the server's concern. Here is how the official client handles this: LINK TBD 🚧