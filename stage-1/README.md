# Stage 1 - Write Some Code

## Dependencies
[Github](https://github.com/)

## Background

You are working as part of an insurance company as an engineer.
Customer Support has just identified a problem with one of our service applications. For an unknown reason, our latest customers between ages 40 and 59 have paid an incorrect amount for their insurance products.

We need to identify the affected customers and notify Customer Support with the customer's name, phone number and email address inside a .txt file.

There is a list of our latest customers [here](./latest-customers.txt)


## Test

Please write some code in your chosen language to produce the .txt file.

Once complete: 
 - Create a feature branch
 - Commit your created .txt file
 - Push this repository to your own Github profile
 - Raise a pull/merge request
 - Send Customer Support (ClearRoute hiring manager) the URL of the PR

### Notes

 - The Customer Support teams tends to not be very technical so keep that mind when producing the .txt file.
 - Clean Code will be one of the score marks

## Install
- Setup a virtual env and install requirements:
```
python -m venv venv
source venv/bin/activate
pip -r requirements.txt
```
- Navigate to folder and set python path with:
```
cd stage-1; PYTHONPATH=$(pwd)
```
- Run extractor with the following (use flag -h for more options):
```
python src/insurance_extractor.py latest-customers.txt -o output/customers_to_check.txt
```
- Run tests with:
```
pytest -vsrfp test/test_insurance_extractor.py
```
