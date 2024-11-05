# Makefile

# Virtual environment name
VENV_NAME = airflow_dag_1

# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Set up the environment
setup: create_venv install_dependencies

# Create virtual environment using python's venv
create_venv:
	@if [ -d "$(VENV_NAME)" ]; then \
		echo "The virtual environment $(VENV_NAME) already exists."; \
	else \
		echo "Creating the virtual environment $(VENV_NAME)..."; \
		/home/marcosparicio/.pyenv/shims/python3.10 -m venv $(VENV_NAME); \
	fi

# Install dependencies from requirements.txt
install_dependencies:
	@echo "Installing dependencies..."
	$(VENV_NAME)/bin/pip install --upgrade pip
	$(VENV_NAME)/bin/pip install -r requirements.txt

# Run
run_user_pipeline:
	@echo "Running user_pipeline DAG..."
	. $(VENV_NAME)/bin/activate && airflow dags trigger user_pipeline

# Clean virtual environment (optional)
clean:
	@echo "Removing virtual environment..."
	rm -rf $(VENV_NAME)

# para crear el entorno virtual: make setup
# para activarlo: source airflow_dag_1/bin/activate
# para limpiarlo: make clean
# para desactivarlo: deactivate
# para ejecutar el DAG user_pipeline: make run_user_pipeline