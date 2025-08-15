#!/usr/bin/env bash
exec gunicorn crm_arbitrage.wsgi:application -b 0.0.0.0:8000 --workers 3 --timeout 60
