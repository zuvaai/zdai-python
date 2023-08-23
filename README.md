# Zuva DocAI (ZDAI) Python Wrapper

# Wrapper

The API wrapper is designed to reflect the decoupled nature of ZDAI's microservices. Meaning, there is one wrapper
class for each microservice.

## Setup

Install the `zdai` package from this repository.

```
pip3 install git+https://github.com/zuvaai/zdai-python.git
```

The following commands will set up the wrapper and test your credentials to make sure they're valid.

```terminal
python3 -m zdai --set-token <put token here>
python3 -m zdai --set-url <put url here>
python3 -m zdai --test connection
```

Sometimes Python `requests` module throws `urllib3` Connection Errors, which may be addressable by installing
the below packages:

```
pip3 install pyopenssl ndg-httpsclient pyasn1
```

## Authorization

Every API call to the ZDAI requires an Authorization token in the header. You can provide these in the wrapper's
configuration file found in config/access.json and access them using the below method, or provide them from other sources.

### Method 1: Provide the token via the ZDAISDK Constructor

```python
from zdai import ZDAISDK, config

url, token = config.get_access()

sdk = ZDAISDK(url = url, token = token)
```

### Method 2: Provide the token via the config/access.json

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)
```

## Files

To create a file in ZDAI:

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = sdk.file.create(content = f.read())
    file_id = file.id
```

You may also set the file's expiration date. The default in DocAI is 7 days.

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    # The following will submit the file and set its expiration to 1 day
    # from the time the API call is run.
    file, _ = sdk.file.create(content=f.read(), expiration = '1d')
    # The following will update the file's expiration to 13d in the future.
    content, _ = sdk.file.set_expiration(file_id = file.id, expiration = '13d')
    print(f'The file will expire on {content.expiration}.')
```

## Fields

To get the AI models that can be used for document text extractions:

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)

fields, _ = sdk.fields.get()

for field in fields:
    print(f'{field.id}: {field.name}')
```

## Classification

To create a classification request on a file, as well as obtain the request's status:

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = sdk.file.create(content = f.read())

classification_jobs, _ = sdk.classification.create(file_ids = [file.id])
classification_status, _ = sdk.classification.get(request_id = classification_jobs[0].id)
```

Note that the above accepts a list of `file_ids`.

## (Alpha) Multi-level Classification

To create a multi-level classification request on a file, as well as obtain the results:

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = sdk.file.create(content = f.read())

mlc_jobs, _ = sdk.mlc.create(file_ids = [file.id])
mlc_status, _ = sdk.mlc.get(request_id = mlc_jobs[0].id)

# Once the request has completed (mlc_job.is_finished() or mlc_job.is_successful(), you can obtain the request's MLC properties
# Below are sample outputs using the above print statement
# Contract, Business Transaction Agt, Letter of Intent
# Contract, Structured Finance Agt, ISDA

for mlc in mlc_jobs:
    if mlc.is_successful():
        print(f'{mlc.classification_1}, {mlc.classification_2}, {mlc.classification_3}')
        print(f'Is amendment? {mlc.is_amendment}')
        print(f'Is master agreement? {mlc.is_master_agreement}')
        print(f'Language: {mlc.language_name}')

```

## Extraction

To create an extraction request on a file, as well as obtain the request's status and results:

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = sdk.file.create(content = f.read())

extraction_jobs, _ = sdk.extraction.create(file_ids = [file.id], field_ids = ['<field_id>', '<field_id>'])
extraction_status, _ = sdk.extraction.get(request_id = extraction_jobs[0].id)

# Only successful if the extraction_status.status is complete or failed
results, _ = sdk.extraction.get_result(request_id = extraction_jobs[0].id)

for result in results:
    print(result)

```

Note that the above accepts a list of `file_ids` and a list of `field_ids`.

## Training

To create a training request for a field, as well as obtain the request's status and accuracy and validation details:

```python
from time import sleep
from zdai import ZDAISDK
from zdai.CustomFieldTrainer import CustomFieldTrainer

sdk = ZDAISDK(from_config = True)
custom_field = CustomFieldTrainer(sdk = sdk, name = 'customfieldname')

custom_field.create_empty()
with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = sdk.file.create(content= f.read())
ocr_request , _ = sdk.ocr.create(file_ids = [file.id])
while not (ocr_request[0].is_finished()):
    ocr_request[0].update()
    sleep(5)
custom_field.add_annotation(file_id = file.id, start = 100, end = 150)
custom_field.add_annotation(file_id = file.id, start = 500, end = 550)
custom_field.train()

print(custom_field.get_accuracy())
print(custom_field.get_validation_details())
print(custom_field.get_metadata())

```

Note that at least 30 files are needed for well trained fields.
Note that OCR on files for training must be complete before training.

## Language

To create an language request on a file, as well as obtain the request's status:

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = sdk.file.create(content = f.read())

language_jobs, _ = sdk.language.create(file_ids = [file.id])
language, _ = sdk.language.get(request_id = language_jobs[0].id)
```

Note that the above accepts a list of `file_ids`

# Date Normalization

DocAI can be used to normalize strings that contain dates, so that the `year`, `month` and `day` are returned.

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)

date_phrases = [
    "The amortization schedule will begin on April 6, 1990",
    "The agreement start date is December 25, 2055",
    "The End Date of the agreement on the 5th day of December, 2022",
    "The Start Date is on the 12th day of April, 1540",
    "This has no dates",
]

for phrase in date_phrases:
    response, _ = sdk.normalization.get_dates(text = phrase)

    if not response.dates:
        print(f'[N/A] {response.text}')
        continue

    for date in response.dates:
        print(f'[{date.year}-{date.month}-{date.day}] {response.text}')

```

# Currency Normalization

DocAI can be used to normalize strings that contain currencies, so that the `value` and `symbol` are returned.

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)

currency_phrases = [
      "The landlord is charging two thousand five hundred dollars",
      "The mortgage owner agrees to pay a value of three hundred and fifty euros per month",
      "During their trip to Korea, the couple agreed to pay the establishment 500 Won per day",
      "The agreement defines the Payment to be nine hundred and ten million five hundred and one thousand five hundred and fifty five dollars"
    ]

for phrase in currency_phrases:
    response, _ = sdk.normalization.get_currencies(text = phrase)

    for currency in response.currencies:
        print(f'[{currency.symbol} {currency.value}] {response.text}')
```

# Duration Normalization

DocAI can be used to normalize strings that contain durations, so that the `value` and `unit` are returned.

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)

duration_phrases = [
    "This agreement between the two counterparties will expire two years after its execution",
    "The owner of the agreement must pay the client the after the 5th anniversary of its execution",
    "The lendee, after five weeks of obtaining the loan, will begin paying interest",
    "The interest of this agreement will increase by .5% after three years",
    "My birthday starts six (6) days into the month of April"
]

for phrase in duration_phrases:
    response, _ = sdk.normalization.get_durations(text = phrase)

    for duration in response.durations:
        print(f'[{duration.value} {duration.unit}] {response.text}')

```

# Examples

## How to obtain a document's text, document classification, language and field extractions

```python
from zdai import ZDAISDK, DocumentClassificationRequest, LanguageClassificationRequest, OCRRequest, FieldExtractionRequest
import time

sdk = ZDAISDK(from_config = True)

fields = sdk.fields.get()[0]

with open('path/to/file.ext', 'rb') as f:
    file, _ = sdk.file.create(content=f.read())

print(f'Created {file.id}')

field_names = ['Title', 'Parties', 'Date', 'Governing Law', 'Indemnity']

requests = []
requests.extend(sdk.ocr.create(file_ids = [file.id])[0])
requests.extend(sdk.classification.create(file_ids = [file.id])[0])
requests.extend(sdk.language.create(file_ids = [file.id])[0])
requests.extend(sdk.extraction.create(file_ids = [file.id], field_ids = [f.id for f in fields if f.name in field_names])[0])


while len(requests) > 0:
    for request in requests:
        print(request.type, request.id, request.status)
        request.update()
        if request.is_finished():
            if request.is_type(OCRRequest):
                text = request.get_text()
                print(f'Finished: {text[0:50]}')
            elif request.is_type(DocumentClassificationRequest):
                print(f'Finished: {request.classification}, {request.is_contract}')
            elif request.is_type(LanguageClassificationRequest):
                print(f'Finished: {request.language}')
            elif request.is_type(FieldExtractionRequest):
                for result in request.get_results():
                    print(result.field_id, result.text, result.spans)

            requests.remove(request)
    time.sleep(2)
```

## Obtain a newly-submitted file's ID

```python
from zdai import ZDAISDK

sdk = ZDAISDK(from_config = True)

with open('file_zones/upload_files/...', 'rb') as f:
    file, _ = sdk.file.create(content = f.read())

print(f'The file was submitted - its file_id is {file.id} and it expires on {file.expiration}')
```
