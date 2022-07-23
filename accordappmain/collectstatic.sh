#!/bin/bash

while true
do
  python3 manage.py collectstatic --noinput
  sleep 30
done
