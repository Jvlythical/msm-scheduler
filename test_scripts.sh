#!/bin/bash

scripts=(
    "msm_scheduler.tests.sanity_test" 
    "msm_scheduler.tests.google_spreadsheet_test" 
    "msm_scheduler.tests.csv_test")

for script in "${scripts[@]}"; do
    echo "Running $script..."
    poetry run python3 -m "$script" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "$script ran successfully."
    else
        echo "$script failed to run."
        exit 1  # Exit if any script fails
    fi
done

echo "All scripts ran successfully."
