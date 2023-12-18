# #!/bin/bash

# # Start the server in the background
# ./run.sh &

# # Store the server's process ID
# PID=$!

# # Run your tests here (replace with actual test commands)
# # Example: newman run your_test_collection.postman_collection.json -e env.json



# # Ensure the server is killed when tests are done
# kill $PID


# !/bin/sh

# Exit immediately if Newman complains
set -e

# Kill the server on exit
trap 'kill $PID' EXIT

# Start the server in the background and record the PID
./run.sh &
PID=$!

# Run Newman with the specified Postman collections and environment
echo "running tests..."

# newman run /Create User.postman_collection.json

echo "tests completed"
