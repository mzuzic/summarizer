#!/bin/sh
set -e

/wait-for custom_extraction:5006 -- celery -A app worker --pool solo --loglevel=debug --concurrency=4