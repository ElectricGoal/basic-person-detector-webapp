#!/bin/bash

# Run gunicorn with uvicorn worker
gunicorn app.main:app -c config.py