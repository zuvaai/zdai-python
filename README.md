# Kira Document AI (KDAI) Python Wrapper

# Wrapper

The API wrapper is designed to reflect the decoupled nature of KDAI's microservices. Meaning, there is one wrapper 
class for each microservice.

## Setup

The following commands will set up the wrapper and test your credentials to make sure they're valid.

```terminal
python3 -m kdai --set-token <put token here>
python3 -m kdai --set-url <put url here>
python3 -m kdai --test connection
```

Add the kdai folder to your Python Interpreter's site-packages to make it easier to use/import in your projects.

Sometimes Python ```requests``` module throws ```urllib3``` Connection Errors, which may be addressable by installing
the below packages:

```pip3 install pyopenssl ndg-httpsclient pyasn1```

## Authorization

Every API call to the KDAI requires an Authorization token in the header. You can provide these in the wrapper's
configuration file found in config/access.json and access them using the below method, or provide them from other sources.

### Method 1: Provide the token via the KDAISDK Constructor

```python
from kdai import KDAISDK, config

url, token = config.get_access()

kdai = KDAISDK(url = url, token = token)
```

### Method 2: Provide the token via the config/access.json

```python
from kdai import KDAISDK

kdai = KDAISDK(from_config = True)
```

## Files

To create a file in KDAI:

```python
from kdai import KDAISDK

kdai = KDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = kdai.file.create(content = f.read())
    file_id = file.id
```

## Fields
To get the AI models that can be used for document text extractions:

```python
from kdai import KDAISDK

kdai = KDAISDK(from_config = True)

fields, _ = kdai.fields.get()

for field in fields:
    print(f'{field.id}: {field.name}')
```

## Classification

To create a classification request on a file, as well as obtain the request's status:

```python
from kdai import KDAISDK

kdai = KDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = kdai.file.create(content = f.read())

classification_jobs, _ = kdai.classification.create(file_ids = [file.id])
classification_status, _ = kdai.classification.get(request_id = classification_jobs[0].request_id)
```

Note that the above accepts a list of ```file_ids```.

## Extraction

To create an extraction request on a file, as well as obtain the request's status and results:

```python
from kdai import KDAISDK

kdai = KDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = kdai.file.create(content = f.read())

extraction_jobs, _ = kdai.extraction.create(file_ids = [file.id], field_ids = ['<field_id>', '<field_id>'])
extraction_status, _ = kdai.extraction.get(request_id = extraction_jobs[0].request_id)

# Only successful if the extraction_status.status is complete or failed
extraction_results, _ = kdai.extraction.get_result(request_id = extraction_jobs[0].request_id)
```

Note that the above accepts a list of ```file_ids``` and a list of ```field_ids```.

## Language

To create an language request on a file, as well as obtain the request's status:

```python
from kdai import KDAISDK

kdai = KDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = kdai.file.create(content = f.read())

language_jobs, _ = kdai.language.create(file_ids = [file.id])
language, _ = kdai.language.get(request_id = language_jobs[0].request_id)
```

Note that the above accepts a list of ```fild_ids```

# Models

The KDAI wrapper returns instances of the data model associated with the action that took place.  
These models are listed above in the ```/models``` folder.

The data models are what allow you to easily reference the data that come back from the KDAI API.

The above acts as a layer of abstraction on top of the JSON that came back from KDAI. Using the above example,  
you can obtain the KDAI response by using ```file.json()``` which will show what KDAI responded with.

# Examples

## Obtain a file's Classification

```python
from kdai import KDAISDK
import time

kdai = KDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = kdai.file.create(content = f.read())

print(f'Created file as {file.id}')

jobs, _ = kdai.classification.create(file_ids = [file.id])

while len(jobs) > 0:
    for job in jobs:
        latest, _ = kdai.classification.get(request_id = job.request_id)

        print(f'Job {job.request_id} is {latest.status}')

        if not latest.is_done():
            continue

        print(f'Classification: {latest.classification}')
        jobs.remove(job)

    time.sleep(1)
```

## Obtain a newly-submitted file's ID

```python
from kdai import KDAISDK

kdai = KDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = kdai.file.create(content = f.read())

print(f'The file was submitted - its file_id is {file.id} and it expires on {file.expiration}')
```
