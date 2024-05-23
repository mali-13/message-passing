#!/bin/sh

# Start Flask server
flask run --host 0.0.0.0 &

# Start gRPC server
python -m app.person.gRPC.service