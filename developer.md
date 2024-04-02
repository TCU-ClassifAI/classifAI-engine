# Developer quickstart

Please read the full deveper doccumentation at the site. 

## Useful commands

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
sudo systemctl start rqworker@1
sudo journalctl -u classifai
```
- The first command will check the status of the classifai service.
- The second command will restart the classifai service.
- The third command will start the rqworker service.
- You can 'spawn' multiple rqworker services by changing the number at the end of the command. For example, `rqworker@1`, `rqworker@2`, `rqworker@3`, etc.
- The fourth command will check the logs of the classifai service.


