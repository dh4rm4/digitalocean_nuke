<h1 align="center">DigitalOcean Nuke</h1>
<p align="center">
<a href=""><img src="https://media.giphy.com/media/uSHMDTUL7lKso/giphy.gif" alt="Nuke"></a>

Small tool to periodically nuke every DigitalOcean ressources of a given account.

## How To

### Requirements

You must define few environnement variables to configure the execution.

- DO_VAR_RSRC_TIMEOUT: max lifetime fore ressources in seconds (e.g. 1h -> 3600)
- DO_VAR_TOKEN: main DigitalOcean [token](https://www.digitalocean.com/docs/api/create-personal-access-token/)
- DO_VAR_SPACES_ACCESS_ID: DigitalOcean [space access_id](https://www.digitalocean.com/community/tutorials/how-to-create-a-digitalocean-space-and-api-key)
- DO_VAR_SPACES_ACCESS_KEY: DIitalOcean [space access_key](https://www.digitalocean.com/community/tutorials/how-to-create-a-digitalocean-space-and-api-key)

### [Pipeline schedules](https://docs.gitlab.com/ee/user/project/pipelines/schedules.html)

You can take advantage of Gitlab's Pipeline schedules to launch the tool periodically.

To do so just define the job  with its env variables in the "CI/CD -> Schedules" panel.

### Manual
To execute the tool manually:
1. clone the repository
```
cd ${HOME}/Documents && git clone git@gitlab.com:posedao/digitalo_nuke.git
```
2. define the environnement variables
```
export DO_VAR_SPACES_ACCESS_ID=XXXXXXXXX
export DO_VAR_SPACES_ACCESS_KEY=XXXXXXXXX
export DO_VAR_TOKEN=XXXXXXXXX
export DO_VAR_RSRC_TIMEOUT=1800

```
3. install the dependancies
```
pip3 install -r ./requirements.txt
```
4. Launch the nukes
```
python ./src/control_center.py
```

boid
