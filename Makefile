.PHONY: check-versions
check-versions: ## Check for outdated package versions (including major bumps)
	@echo "🚀 Checking for outdated package versions"
	@uv run pip-review | grep -v 'transcriber==' || true

.PHONY: update
update: ## Update all project dependencies to the latest compatible versions and refresh the lock file.
	@echo "🔒 Resolving and freezing latest compatible versions in uv.lock..."
	@uv lock  # This does the update to the latest versions

	@echo "🚀 Installing new versions into virtual environment..."
	@uv sync # This installs the new versions from uv.lock

.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync
	@uv run pre-commit install

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@uv run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@uv run deptry src tests

.PHONY: test
test: ## Test the code with pytest -vv gives us pytest-smart output.
	@echo "🚀 Testing code: Running pytest"
	@uv run python -m pytest --cov --cov-config=pyproject.toml -vv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@./.venv/bin/mkdocs serve --dev-addr 127.0.0.1:8000 --watch docs --watch src/transcriber

.PHONY: man
man: ## Build and serve the documentation
	@uv run python src/transcriber/transcribe.py --help

.PHONY: transcribe
transcribe: ## Transcribe video files to SRT subtitle files interactively
	@uv run python src/transcriber/transcribe.py --interactive --exclude \
	"_Model/sheets/jpgs/output.mp4" \
	"_Model/OD_Textures/Open Source/AmbientCG/space-generation-success.mp4" \
	"_Model/OD_Textures/Open Source/AmbientCG/space-generation-fail.mp4" \
	"_Model/Animation/final video.mp4"

# Define a variable for your Docker image name/tag
DOCKER_IMAGE_NAME := transcriber-app:latest

# Define dependencies that will trigger a Docker build
DOCKER_DEPENDENCIES := Dockerfile pyproject.toml uv.lock src/transcriber

# Touch this file after the docker build
DOCKER_BUILD_TRIGGER := .docker-build-timestamp

.PHONY: docker-build
docker-build: $(DOCKER_DEPENDENCIES)
	@echo "🚀 Building Docker image $(DOCKER_IMAGE_NAME)"
	@docker build -t $(DOCKER_IMAGE_NAME) .
	@touch $(DOCKER_BUILD_TRIGGER)

.PHONY: docker-run
# Default target to run the transcriber script in a Docker container (interactive mode)
docker-run: docker-run-interactive

.PHONY: docker-run-non-interactive
docker-run-non-interactive: docker-build ## Run the transcriber script in a Docker container (non-interactive by default)
	@echo "🚀 Running transcriber in Docker (non-interactive)"
	# This target allows specifying INPUT_DIR_HOST=/path/to/your/videos
	# If INPUT_DIR_HOST is NOT set, the script will use its default input path (which is /app inside the container).
	# This is suitable if the user's videos are placed within the project's mounted /app directory.

	# Construct the docker run command
	@chmod +x helpers/docker-run.sh # Ensure the script is executable.
	@./helpers/docker-run.sh \
		"$(INPUT_DIR_HOST)" \
		"--exclude \"_Model/sheets/jpgs/output.mp4\" \"_Model/OD_Textures/Open Source/AmbientCG/space-generation-success.mp4\" \"_Model/OD_Textures/Open Source/AmbientCG/space-generation-fail.mp4\" \"_Model/Animation/final video.mp4\" $(ARGS)" \
		"$(DOCKER_IMAGE_NAME)"

.PHONY: docker-run-interactive
docker-run-interactive: docker-build ## Run the transcriber script in a Docker container (interactive mode)
	@chmod +x helpers/docker-run.sh # Ensure the script is executable.
	@./helpers/docker-run.sh \
		"$(INPUT_DIR_HOST)" \
		"--interactive --exclude \"_Model/sheets/jpgs/output.mp4\" \"_Model/OD_Textures/Open Source/AmbientCG/space-generation-success.mp4\" \"_Model/OD_Textures/Open Source/AmbientCG/space-generation-fail.mp4\" \"_Model/Animation/final video.mp4\" $(ARGS)" \
		"$(DOCKER_IMAGE_NAME)"

.PHONY: docker-clean
docker-clean: ## Remove the transcriber Docker image
	@echo "🚀 Cleaning Docker image $(DOCKER_IMAGE_NAME)"
	docker rmi $(DOCKER_IMAGE_NAME) || true

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
