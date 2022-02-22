#!/bin/sh
set -e

sleep 20

celery -A app worker --pool solo --loglevel=debug --concurrency=4