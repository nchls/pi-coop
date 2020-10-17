#!/bin/bash

ftimestamp=$(stat -c %Y "/home/pi/coop/camera/sentinel")
three_minutes_ago=$(expr $(date +%s) - 180)
[ "$ftimestamp" -lt "$three_minutes_ago" ] && systemctl is-active --quiet motion && /usr/sbin/service motion stop
