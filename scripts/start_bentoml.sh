#!/bin/bash

if [ -f .env ]; then
    PORT=$(grep ^PORT .env | cut -d '=' -f2)
    if [ -z "$PORT" ]; then
        echo "Error: PORT not found in .env file"
        exit 1
    fi
else
    echo "Error: .env file not found"
    exit 1
fi

SERVING_MODES=("serve" "serve-grpc")

PS3="Select serving mode (use arrows and press Enter): "
select SERVING_MODE in "${SERVING_MODES[@]}"; do
    if [ -n "$SERVING_MODE" ]; then
        break
    else
        echo "Invalid selection. Please try again."
    fi
done

case "$SERVING_MODE" in
    "serve")
        bentoml serve luna.bentoml_service:svc --port "$PORT" --api-workers 1 --reload
        ;;
    "serve-grpc")
        bentoml serve-grpc luna.bentoml_service:svc --port "$PORT" --api-workers 1 --reload
        ;;
    *)
        echo "Error: Invalid serving mode. Please use 'serve' or 'serve-grpc'"
        exit 1
        ;;
esac