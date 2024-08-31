#!/bin/bash 
PORT=8000

while read entry; do
    IFS=' '
    read -ra strarr <<< "$entry"
    echo "Entry: $entry"
    if [[ ${strarr[1]} =~ ^[0-9]+$ ]]; then
        OUTPUT="$(kill -9 ${strarr[1]})"
        echo "killed PID: ${strarr[1]} ${OUTPUT}"
    fi
done < <(lsof -i tcp:$PORT)

while read entry; do
    IFS=' '
    read -ra strarr <<< "$entry"
    echo "Entry: $entry"
    if [[ ${strarr[2]} =~ ^[0-9]+$ ]]; then
        OUTPUT="$(kill -9 ${strarr[2]})"
        echo "killed PID: ${strarr[2]} ${OUTPUT}"
    fi
    if [[ ${strarr[1]} =~ ^[0-9]+$ ]]; then
        OUTPUT="$(kill -9 ${strarr[1]})"
        echo "killed PID: ${strarr[1]} ${OUTPUT}"
    fi
done < <(ps -aef | grep main.py)

#nohup fastapi dev main.py > nohup.out 2>&1 </dev/null &

#nohup uvicorn main:app --reload --host 127.0.0.1 --port $PORT --log-config=log_conf.yaml> nohup.out 2>&1 </dev/null &

nohup uvicorn main:app --host 127.0.0.1 --port $PORT --log-config=log_conf.yaml> nohup.out 2>&1 </dev/null &