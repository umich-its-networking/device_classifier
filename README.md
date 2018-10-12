# Network Device Classifier

This is a proof-of-concept project created by the University of Michigan's ITS Infrastructure Networking team.

### Setup

1. Clone this repository
2. Change to the cloned directory: `cd device_classifier`
3. Create a python virtual environment: `virtualenv venv`
4. Activate the virtualenv: `source ./venv/bin/activate`
5. Install the "ndc" package: `pip install -e .`

### Run server with dummy data

1. `export FLASK_DEBUG=1`
2. `export FLASK_APP=ndc.api`
3. `export FLASK_ENV=development`
4. `export RAW_DATA=fake_data/raw.csv`
5. `flask run`

Once the development server is running, you can try these URLs to see different predictions...

**Display info about the trained classifier: <http://127.0.0.1:5000/info>**
```
{
  "accuracy": 1.0, 
  "sample_size": 900
}
```

**Make a prediction about [DHCP options](https://www.iana.org/assignments/bootp-dhcp-parameters/bootp-dhcp-parameters.xhtml#options) fingerprint ("req_list"): <http://127.0.0.1:5000/?req_list=15,24,6,2,9,24,9,19,10>**
```
{
  "predicted_class": "pc", 
  "probabilities": {
    "mobile": 0.39055, 
    "other": 0.03776, 
    "pc": 0.57169
  }
}
```


**Make a prediction about a [MAC OUI](https://en.wikipedia.org/wiki/Organizationally_unique_identifier) ("oui"): <http://127.0.0.1:5000/?oui=41:70:00>**
```
{
  "predicted_class": "mobile", 
  "probabilities": {
    "mobile": 0.96968, 
    "other": 0.00839, 
    "pc": 0.02192
  }
}
```
