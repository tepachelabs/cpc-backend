#!/bin/sh

# Run migrations
doppler run -- poetry run python manage.py migrate

# Start supervisor
/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf