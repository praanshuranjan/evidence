#!/bin/bash
echo "[$(date -Iseconds)] START pid=$$ (shell script)" >> ~/heimdall_poc_shell.log
tick=0
while true; do
  sleep 30
  tick=$((tick+1))
  echo "[$(date -Iseconds)] alive pid=$$ tick=$tick" >> ~/heimdall_poc_shell.log
done
