# GrimoireGitter MSR Hackathon 2022
Participants:

- Kalvin Eng
- Hareem Sahar

In this repostiory, we replicate the data collection pipeline of the paper: "*[How are issue reports discussed in Gitter chat rooms?](https://softwareprocess.es/pubs/sahar2020JSS-Gitter-Issues.pdf "How are issue reports discussed in Gitter chat rooms?")*" using [GrimoireLab](https://github.com/chaoss/grimoirelab "GrimoireLab").

The components of GrimoireLab we use are:
![image](https://user-images.githubusercontent.com/9467666/152590177-e0286a2b-f2ed-460a-81f5-84e779fb45c8.png)

### Projects Collected
For the hackathon, we chose a 7 of the original 24 Gitter chat rooms to test our GrimoireLab data pipeline. The projects are:
- aws/aws-sdk-go ([Github](https://github.com/aws/aws-sdk-go "Github") | [Gitter](https://gitter.im/aws/aws-sdk-go "Gitter"))
- patchthecode/JTAppleCalendar ([Github](https://github.com/patchthecode/JTAppleCalendar "Github") | [Gitter](https://gitter.im/patchthecode/JTAppleCalendar "Gitter"))
- mailboxer/mailboxer ([Github](https://github.com/mailboxer/mailboxer "Github") | [Gitter](https://gitter.im/mailboxer/mailboxer "Gitter"))
- PerfectlySoft/Perfect ([Github](https://github.com/PerfectlySoft/Perfect "Github") | [Gitter](https://gitter.im/PerfectlySoft/Perfect "Gitter"))
- amberframework/amber ([Github](https://github.com/amberframework/amber "Github") | [Gitter](https://gitter.im/amberframework/amber "Gitter"))
- shuup/shuup ([Github](https://github.com/shuup/shuup "Github") | [Gitter](https://gitter.im/shuup/shuup "Gitter"))
- kriasoft/react-starter-kit ([Github](https://github.com/kriasoft/react-starter-kit "Github") | [Gitter](https://gitter.im/kriasoft/react-starter-kit "Gitter"))

These projects were chosen because each project contains less than 5000 total issues and pull requests making the Github rate limit a minimal issue.

Using GrimoireLab, retrieving additional projects is a non-issue as `grimoirelab-settings/projects.json` can be edited to add more projects. However, the data retrieval from Github will be rate limited making data retrieval or repositories containing a large number (>10,000) of issues and pull requests take ages.

##  Setup
### System Requirements
This data pipeline has been tested on Ubuntu 18.04 with 4 CPUs and 8GB of memory.

Docker and Docker Compose are also installed on the system with the following commands:
```sh
sudo curl -sSL https://get.docker.com/ | sh
sudo usermod -a -G docker $(whoami)
sudo service docker start
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
After running the commands and a restart of your machine, the `docker-compose` and `docker` commands should work.

<hr>

### API Token Creation
Tokens need to be created for both Github and Gitter.
#### Github
Follow the instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

No permissions need to be granted, and a non-expiring token should be created.

Ideally, multiple tokens should be created for Github using a collection of accounts as API requests are limited to 5000 per hour.

#### Gitter
You can obtain your Gitter API key by visiting and signing in here: https://developer.gitter.im/apps

**Note:** You must join the chat room to use your token for mining the chat room.

<hr>

### Elasticsearch
To enable querying services such as [Mirage](https://opensource.appbase.io/mirage/ "Mirage") and [Dejavu](https://dejavu.appbase.io/ "Dejavu"), we create an `grimoirelab-settings/elasticsearch.yml` that contains settings for adding CORS headers. More information about configuring Elasticsearch can be found [here](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/settings.html "here"). 

The `grimoirelab-settings/elasticsearch.yml` is mounted to `/usr/share/elasticsearch/config/elasticsearch.yml` via Docker Compose.

<hr>

### Defining Projects
Projects are defined in `grimoirelab-settings/projects.json` with the format defined here: https://github.com/chaoss/grimoirelab-sirmordred/blob/171cb813b636f8bc8f34c4ccbfa5d4b7d18c8f20/README.md#projectsjson-

To help with the generation of `grimoirelab-settings/projects.json` for our data pipeline with `create_projects_file.py`.  A list of projects need to be added to the source code of the script.

<hr>

### GrimoireLab Configuration
We have provided an example configuration file in `grimoirelab-settings/setup.cfg.example` which will need:
1. The API tokens for Gitter and Github to be inserted
2. To be renamed to `grimoirelab-settings/setup.cfg.example`

<hr>

### Running GrimoireLab
Once all the setup steps have been completed, in the root repository run the following command:
```sh
docker-compose up -d
```
- The Kibiter dashboard can be accessed at: `http://localhost:5601`
- The ElasticSearch instance can be accessed at: `http://localhost:9200`
- The HatStall web interface can be accessed at: `http://localhost:8000`

#### Useful commands
- See list of containers running: `docker ps`
- Check SirMordred logs: `tail -f /tmp/all.log -n 200`
- Restart SirMordred container: `docker restart grimoiregitter_mordred_1`
- View Docker logs: `docker-compose logs -f`

More detailed Docker Compose instructions can be found here: https://github.com/chaoss/grimoirelab/tree/master/docker-compose

#### Known Issues
* Mounting of single files to docker container requires restart of container for file to be updated
* To reenrich indexes, elasticsearch enriched index must be deleted (sometimes it fails, so delete and restart mordred container)

## GrimoireLab Adaptations
### GrimoireElk Gitter Enrichment
We modify the Gitter enrichment of GrimoireElk to do the following:
- Better error reporting detailing UUID and repository
- Handle improper URLs from the Gitter API (Issue: https://github.com/chaoss/grimoirelab-elk/issues/1029)
- Improve issue classfication by leveraging the Github website (Issue: https://github.com/chaoss/grimoirelab-elk/issues/1028)

As a hotfix, we mount the updated file directly to the SirMordred container.

### SortingHat Identity Alignment
We also implement a naive script, to align identities that SortingHat may not have automatically aligned.

To get started we have created a Jupyter Docker environment for running the script without dependencies:
1. Navigate to the `jupyter` folder and run the following command:
```sh
docker-compose up -d
```
2. Access Jupter Lab by running `docker logs jupyter_jupyter_1` and finding the instruction to access under the line `   Or copy and paste one of these URLs:`
3. Run the `SortingHat.ipynb` notebook by navigating to the following `Run > Restart Kenel and Run All Cells...`

When the script has completed, the bottom of the notebook will have instructions on how to access HatStall and merge identities.

## Preliminary Results
We gather data to replicate some of the results in *[How are issue reports discussed in Gitter chat rooms?](https://softwareprocess.es/pubs/sahar2020JSS-Gitter-Issues.pdf "How are issue reports discussed in Gitter chat rooms?")*.

The scripts for accessing the data can be run as follows:
1. Navigate to the `jupyter` folder and run the following command:
```sh
docker-compose up -d
```
2. Access Jupter Lab by running `docker logs jupyter_jupyter_1` and finding the instruction to access under the line `   Or copy and paste one of these URLs:`
3. Run the `Preliminary Results.ipynb` notebook by navigating to the following `Run > Restart Kenel and Run All Cells...`

To generate the visualizations replicating a comparison between the:
1. **The Count of Gitter API Issues**: It is generated in `Preliminary Results.ipynb` with the output to `jupyter/output/api_counts.pdf`
![image](https://user-images.githubusercontent.com/9467666/152589685-81f6ed72-df6e-4965-852b-eb6cffa5989d.png)
2. **Resolution time comparison between previous pipeline and GrimoireLab**: Run the RScript `resolution_time.R` (instructions for input files are in the comments)
![image](https://user-images.githubusercontent.com/9467666/152589773-9929ddaf-8ef7-4a9c-a52c-f65a0b47210e.png)
3. **Ratio of number of issue comments in Github one week after and before issue reference in Gitter**: Run the RScript `comments-ratio-boxplot.R` (instructions for input files are in the comments)
![image](https://user-images.githubusercontent.com/9467666/152589935-8d6345e7-625d-48ca-9170-8eec2ef4fd5b.png)


## Exploring Data
To explore the data, you can use the Kibiter dashboard at http://localhost:5601

![image](https://user-images.githubusercontent.com/9467666/152590037-7fb2a10b-a173-4a2a-936c-133fda6eeb9e.png)

Note that the `gitter` index needs to be refreshed by visiting http://localhost:5601/app/kibana#/management/kibana/indices/gitter and clicking the refresh button in the top right. 

For additional panels related to github issues and pull requests, you can load them with the following Kidash commands in the SirMordred container:
```sh
docker exec -it grimoiregitter_mordred_1 kidash -e http://elasticsearch:9200 --import panels/github_issues-index-pattern.json
docker exec -it grimoiregitter_mordred_1 kidash -e http://elasticsearch:9200 --import panels/github_issues_timing.json 
docker exec -it grimoiregitter_mordred_1 kidash -e http://elasticsearch:9200 --import panels/github_issues_efficiency.json
docker exec -it grimoiregitter_mordred_1 kidash -e http://elasticsearch:9200 --import panels/github_pull_requests_efficiency.json
docker exec -it grimoiregitter_mordred_1 kidash -e http://elasticsearch:9200 --import panels/github_pull_requests_timing.json
```
The panels can viewed by visiting http://localhost:5601/app/kibana#/dashboards

The panels are called Sigils downloaded from:
- https://chaoss.github.io/grimoirelab-sigils/panels/github-issues-timing/
- https://chaoss.github.io/grimoirelab-sigils/panels/github-issues-efficiency/
- https://chaoss.github.io/grimoirelab-sigils/panels/github-pullrequests-efficiency/
- https://chaoss.github.io/grimoirelab-sigils/panels/github-pullrequests-timing/

Note that these panels are available since the `panels` folder is mounted to the SirMordred container.

## Need help?
File an issue on this repository and we will respond to you as soon as possible.
