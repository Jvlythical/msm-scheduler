### Installation

1. Install pyenv
2. Install poetry
3. Run `pyenv install <PYTHON-VERSION>`
4. Run `pyenv local <PYTHON-VERSION>`
5. Run `poetry install`

### Usage

#### Schedule
```
python3 -m msm_scheduler.schedule
```

#### Availability
```
python3 -m msm_scheduler.availability
```

### Test
```
./test_scripts.sh
python3 -m msm_scheduler.tests.csv_test
python3 -m msm_scheduler.tests.sanity_test
python3 -m msm_scheduler.tests.google_spreadsheet_test
```
