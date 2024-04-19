# Developer quickstart

Please read the full developer doccumentation at the site. 

## Useful commands


## Check services!!!

```bash
sudo systemctl status classifai
sudo systemctl status gemma
sudo supervisorctl status all
```

## Restart services

```bash
sudo systemctl restart classifai
sudo systemctl restart gemma
sudo supervisorctl restart all
```

## Read logs

```bash
sudo journalctl -u classifai
sudo journalctl -u gemma
sudo supervisorctl tail -5000 <procname> stderr
sudo supervisorctl tail -f <procname> stdout # to follow the logs in real time
```

## View configuration files for services

```bash
sudo systemctl cat classifai
sudo systemctl cat gemma
less /etc/supervisor/supervisord.conf
```

### Start up a worker without supervisor:
    
```bash
# from classifAI-engine/
source PATH_TO_VENV/bin/activate # try venv-3.10
rq worker -c config.worker_config
```


### General running commands

```bash
fuser -k 5000/tcp
```
- This command will kill the process running on port 5000. So, you can restart the server, assuming you are running the server on port 5000.


```bash
source PATH_TO_VENV/bin/activate
```
- This command will activate the virtual environment.
Reminder, you can generate the virtual environment by running the following command:

```bash
python3 -m venv PATH_TO_VENV
deactivate
pip install -r requirements.txt
```

### Checking the process

```bash
sudo systemctl status classifai
sudo systemctl restart classifai
sudo journalctl -u classifai
```
- The first command will check the status of the classifai service.
- The second command will restart the classifai service.
- The third command will show the logs of the classifai service.


## Run the Flask server without service

```bash
# from classifAI-engine/
sudo systemctl stop classifai # stop the service
source PATH_TO_VENV/bin/activate # try venv-3.10
python3 src/app.py
```

## Run the GEMMA server without service

```bash
# from gemma-classification-1
sudo systemctl stop gemma # stop the service
source PATH_TO_VENV/bin/activate # try .venv
# do other installation steps if needed (see gemma README.md)
python3 src/app.py
```

