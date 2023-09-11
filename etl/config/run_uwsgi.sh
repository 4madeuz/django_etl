#!/usr/bin bash


chown www-data:www-data /var/log

uwsgi --strict --ini /opt/config/uwsgi.ini
