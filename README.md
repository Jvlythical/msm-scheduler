### Installation

1. Install pyenv
2. Install poetry
3. Run `pyenv install <PYTHON-VERSION>`
4. Run `pyenv local <PYTHON-VERSION>`
5. Run `poetry install`

### Usage

#### Schedule
```
poetry run python3 -m msm_scheduler.schedule
```

#### Availability
```
poetry run python3 -m msm_scheduler.availability
```

### Test

#### Run all
```
./test_scripts.sh
```

#### Run Individual
```
poetry run python3 -m msm_scheduler.tests.csv_test
```
```
poetry run python3 -m msm_scheduler.tests.sanity_test
```
```
poetry run python3 -m msm_scheduler.tests.google_spreadsheet_test

```

### Docker

Build and run the service using Docker Compose:

```bash
docker compose up --build
```

The service listens on `PORT` (default `8080`) which is mapped to the same port on
your host in the provided `docker-compose.yml`. The log level can be adjusted by
setting `MSM_SCHEDULER_LOG_LEVEL` (e.g. `debug`, `info`).
