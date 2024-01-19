#!/bin/bash

trigger_filepath="/Users/divitrawal/Desktop/resume/resume_data.json"
log_filepath="/Users/divitrawal/Desktop/resume/resume_generator/auto_update_log.txt"

# Initialize the previous modification time
PREV_MOD_TIME=$(stat -f "%m" "$trigger_filepath")

# Infinite loop to keep the script running
while true; do
  # Get the current modification time
  CURRENT_MOD_TIME=$(stat -f "%m" "$trigger_filepath")

  # Compare the current modification time with the previous modification time
  if [[ "$CURRENT_MOD_TIME" != "$PREV_MOD_TIME" ]]; then
    truncate -s 0 "/Users/divitrawal/Desktop/resume/resume_generator/auto_update_log.txt"
    # Run the command if the file has been updated
    python3 "/Users/divitrawal/Desktop/resume/resume_generator/resume_generator.py" >> "$log_filepath" 2>&1

    # Update the previous modification time
    PREV_MOD_TIME=$CURRENT_MOD_TIME
  fi

  # Wait for a second before checking again
  sleep 1
done