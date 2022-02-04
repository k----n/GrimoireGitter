# GrimoireGitter MSR Hackathon 2022
Participants:

- Kalvin Eng
- Hareem Sahar

In this repostiory, we replicate the data collection pipeline of the paper: "*[How are issue reports discussed in Gitter chat rooms?](https://softwareprocess.es/pubs/sahar2020JSS-Gitter-Issues.pdf "How are issue reports discussed in Gitter chat rooms?")*" using [GrimoireLab](https://github.com/chaoss/grimoirelab "GrimoireLab").

### Projects Collected
For the hackathon, we chose a subset of the original 24 Gitter chat rooms to test our GrimoireLab data pipeline. The projects are:
- aws/aws-sdk-go ([Github](https://github.com/aws/aws-sdk-go "Github") | [Gitter](https://gitter.im/aws/aws-sdk-go "Gitter"))
- patchthecode/JTAppleCalendar ([Github](https://github.com/patchthecode/JTAppleCalendar "Github") | [Gitter](https://gitter.im/patchthecode/JTAppleCalendar "Gitter"))
- mailboxer/mailboxer ([Github](https://github.com/mailboxer/mailboxer "Github") | [Gitter](https://gitter.im/mailboxer/mailboxer "Gitter"))
- PerfectlySoft/Perfect ([Github](https://github.com/PerfectlySoft/Perfect "Github") | [Gitter](https://gitter.im/PerfectlySoft/Perfect "Gitter"))

These projects were chosen because each project contains less than 5000 total issues and pull requests making the Github rate limit a minimal issue.

Using GrimoireLab, retrieving additional projects is a non-issue as `grimoirelab-settings/projects.json` can be edited to add more projects. However, the data retrieval from Github will be rate limited making data retrieval or repositories containing a large number (>10,000) of issues and pull requests take ages.

##  Setup
### System Requirements
This data pipeline has been tested on Ubuntu 18.04 with 4 CPUs and 8GB of memory.

Docker and Docker Compose are also installed on the system with the following commands:
```
sudo curl -sSL https://get.docker.com/ | sh
sudo usermod -a -G docker $(whoami)
sudo service docker start
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
After running the commands and a restart of your machine, the `docker-compose` and `docker` commands should work.

### API Token Creation
Tokens need to be created for both Github and Gitter.
#### Github
Follow the instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

No permissions need to be granted, and a non-expiring token should be created.

Ideally, multiple tokens should be created for Github using a collection of accounts as API requests are limited to 5000 per hour.

#### Gitter
You can obtain your Gitter API key by visiting and signing in here: https://developer.gitter.im/apps

**Note:** You must join the chat room to use your token for mining the chat room.

### Elasticsearch
To enable querying services such as [Mirage](https://opensource.appbase.io/mirage/ "Mirage") and [Dejavu](https://dejavu.appbase.io/ "Dejavu"), we create an `grimoirelab-settings/elasticsearch.yml` that contains settings for adding CORS headers. More information about configuring Elasticsearch can be found [here](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/settings.html "here"). 

The `grimoirelab-settings/elasticsearch.yml` is mounted to `/usr/share/elasticsearch/config/elasticsearch.yml` via Docker Compose.

### Defining Projects
Projects are defined in `grimoirelab-settings/projects.json` with the format defined here: https://github.com/chaoss/grimoirelab-sirmordred/blob/171cb813b636f8bc8f34c4ccbfa5d4b7d18c8f20/README.md#projectsjson-

To help with the generation of `grimoirelab-settings/projects.json` for our data pipeline with `filename.py`.  A list of projects need to be...

### GrimoireLab Configuration
`grimoirelab-settings/setup.cfg`

### Useful Commands

### Known Issues
* Mounting of single files to docker container requires restart of container for file to be updated
* To reenrich indexes, elasticsearch enriched index must be deleted (sometimes it fails, so delete and restart container)

## GrimoireLab Enhancements
<!-- ### GrimoireELK -->
<!-- ### Sigils -->
<!-- ### SortingHat Interface -->

## Preliminary Results

### Discussion

## Future Work
<!-- This data pipeline can be further enhanced by... -->
