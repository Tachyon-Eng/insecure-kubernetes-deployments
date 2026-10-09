# SSH Automation Utilities

This directory contains a small Erlang SSH service and a Python client used for scheduled integration checks.

Deploy the server and client with their respective scripts:

```bash
cd server
./deploy.sh
cd ../client
./deploy.sh
```

The server runs in the `erlang` namespace. The client periodically connects to the service and stores callback data under `/app/results`.
