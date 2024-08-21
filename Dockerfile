FROM python:3.9-slim

COPY . /tmp/msm-scheduler
RUN cd /tmp/msm-scheduler && pip install . && rm -rf /tmp/msm-scheduler
RUN useradd -mU msm_scheduler

USER msm_scheduler
WORKDIR /home/msm_scheduler

ENTRYPOINT ["python3", "-m",  "msm_scheduler.serve"]
EXPOSE 8080
