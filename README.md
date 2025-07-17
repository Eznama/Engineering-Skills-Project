# Engineering Skills Project

This repo contains my Dockerized solution for the IEUK 2025 Engineering Skills Project.

## Files

- `load_logs.py`: parses `sample-log.log` into a DataFrame.
- `eda.py`: performs analysis, generates `traffic_over_time.png`, and prints your top IPs/URLs and bot stats.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: builds a container to run `eda.py`.
- `.dockerignore`: excludes unnecessary files from the image.

## Build & Run

```bash
# 1. Build the Docker image
docker build -t log-analyzer:latest .

# 2. Run the container
docker run --rm log-analyzer:latest