# simple-github-announcements
`simple-github-announcements` is a project which aims to build a non-intrusive announcement system in the most easiest way to use possible.

A pub-sub type architecture is used along with client polling to receive announcements to a local machine.

The prime directive of this project is to provide a way for people to subscribe to certain `topics` they want to receive information about and for certain people to be able to publish announcements on these `topics`.

The main goal for this project is to achieve the above with low(ideally 0) server costs, and as lightweight a polling client as possible, while still maintaining desirable functionality.

The idea is for people to be able to fork this repository and publish their own announcements, while using GitHub as a central server(to be able to service large teams) for free.

## How to Use
