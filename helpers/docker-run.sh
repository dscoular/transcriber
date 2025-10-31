#!/bin/bash
set -eu

# Script usage: ./docker-run.sh [INPUT_DIR_HOST] [ARGS] [DOCKER_IMAGE_NAME]
#
# Description:
#   This script is only intended to be called from our Makefile to
#  ensure consistent Docker execution.

# Parameters:
#   INPUT_DIR_HOST: (optional) Path to the input directory on the host machine.
#                   If provided, it will be mounted to /mnt/user_videos in the container.
#   ARGS: Additional arguments to pass to the transcribe.py script.
#   DOCKER_IMAGE_NAME: Name of the Docker image to use.
#

INPUT_DIR_HOST="$1"
ARGS="$2"
DOCKER_IMAGE_NAME="$3"

# 1. Set up base variables
DOCKER_VOLUMES="-v \"$(pwd)\":/app"
DOCKER_VOLUMES=""
# ARGS already contains "--interactive" from the Makefile (passed via $2),
# so we just prepend the base flag to ensure it's there.
# Note: Since the Makefile already wraps this, we'll keep the logic simple here:

RUN_ARGS="$ARGS"

# 2. Conditional logic based on INPUT_DIR_HOST
if [ -n "$INPUT_DIR_HOST" ]; then
    # Check if the directory exists on the host
    if [ ! -d "$INPUT_DIR_HOST" ]; then
        echo "ERROR: INPUT_DIR_HOST='$INPUT_DIR_HOST' does not exist on your host system."
        exit 1
    fi

    # Append the video volume mount
    DOCKER_VOLUMES="$DOCKER_VOLUMES -v \"$INPUT_DIR_HOST\":/mnt/user_videos"

    # Update arguments for the Python script
    RUN_ARGS="--input-path /mnt/user_videos $RUN_ARGS"

    echo "    (Mounting host directory '$INPUT_DIR_HOST' to '/mnt/user_videos' in container.)"
else
    echo "    (Project directory mounted. Run with INPUT_DIR_HOST=/path/to/your/videos to specify the input path.)"
    echo "    (Without it, the script will use its default input path (project root) in container.)"
fi

# 3. Execute the Docker command
if [[ $RUN_ARGS == *"--interactive"* ]]; then
    echo "🚀 Running transcriber in Docker (interactive):"
else
    echo "🚀 Running transcriber in Docker (non-interactive):"
fi
echo "   - Use the ARGS variable on the "make" command-line to override default parameters."
echo "   - A default set of exclude file patterns is used and can be found in the Makefile."
echo "   - You can override this if you use \"ARGS=--exclude=''\" or edit the Makefile."
# Using 'eval' to correctly parse the DOCKER_VOLUMES string,
eval docker run --rm -it \
    "$DOCKER_VOLUMES" \
    -u "$(id -u):$(id -g)" \
    "$DOCKER_IMAGE_NAME" \
    /app/.venv/bin/python src/transcriber/transcribe.py "$RUN_ARGS"
