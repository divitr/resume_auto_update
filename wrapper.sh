#!/bin/bash

# Scheduled to run every minute through cron job

sleep_time=6
iterations=$((60/sleep_time))

DIR=$(dirname "$(realpath "$0")")

cd "$DIR" 

for ((i=0; i<iterations; i++)); do
    	start_time=$(date +%s.%N)
    	./auto_update.sh
    	end_time=$(date +%s.%N)
    	elapsed_time=$(echo "$end_time - $start_time" | bc)

    	remaining_sleep=$(echo "$sleep_time - $elapsed_time" | bc)
    	if (( $(echo "$remaining_sleep > 0" | bc -l) )); then
        	sleep "$remaining_sleep"
    	fi
done
