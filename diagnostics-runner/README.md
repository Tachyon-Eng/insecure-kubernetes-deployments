# Diagnostics Runner

Diagnostics Runner packages PowerShell and a set of Linux administration tools in a container. The accompanying Compose file can run it alongside a Datadog agent for development telemetry.

## Run locally

```bash
export DD_API_KEY="<api-key>"
docker compose build
docker compose up -d
docker exec -it diagnostics /usr/bin/pwsh
```

Stop the containers when finished:

```bash
docker compose down
```
