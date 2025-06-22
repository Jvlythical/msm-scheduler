FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /tmp/build

# Install package without leaving build artefacts behind
COPY . .
RUN pip install --no-cache-dir . && rm -rf /tmp/build

# Create an unprivileged user to run the service
RUN useradd -mU msm_scheduler && mkdir -p /home/msm_scheduler/app \
    && chown -R msm_scheduler:msm_scheduler /home/msm_scheduler

WORKDIR /home/msm_scheduler/app
USER msm_scheduler

ENV PORT=8080

# Expose the service port and start the HTTP server
CMD ["sh", "-c", "python3 -m msm_scheduler.serve ${PORT}"]
