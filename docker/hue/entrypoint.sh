#!/bin/bash

function wait_for_it() {
    local serviceport=$1
    local service=${serviceport%%:*}
    local port=${serviceport#*:}
    local retry_seconds=5
    local max_try=100
    local i=1

    # Check service availability
    nc -z $service $port
    result=$?

    until [ $result -eq 0 ]; do
      echo "[$i/$max_try] check for ${service}:${port}..."
      echo "[$i/$max_try] ${service}:${port} is not available yet"
      if (( $i == $max_try )); then
        echo "[$i/$max_try] ${service}:${port} is still not available; giving up after ${max_try} tries."
        exit 1
      fi

      echo "[$i/$max_try] retrying in ${retry_seconds}s..."
      i=$((i+1))
      sleep $retry_seconds

      # Retry checking service availability
      nc -z $service $port
      result=$?
    done
    echo "[$i/$max_try] $service:${port} is available."
}

# Check all preconditions
for i in ${SERVICE_PRECONDITION[@]}; do
    wait_for_it ${i}
done

# Execute the command passed to the container
exec "$@"
