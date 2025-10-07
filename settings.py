# ==============================
# Settings / Configuration
# ==============================

# URL of the BITNET API endpoint used for sending invoice text
# to the language model for parsing.
# This URL will be used for communication with the external service
# that performs invoice text processing using the specified language model.
BITNET_URL = "https://api-embeddings-ollama.c-zentrix.com/api/chat"

# Name of the language model to use for invoice parsing.
# "mistral:latest" specifies that the latest version of the Mistral model
# will be used for invoice text interpretation.
# You can change this value to use different models as per your requirements.
BITNET_MODEL_NAME = "mistral:latest"

# Port number for running the FastAPI application locally
# The FastAPI app will listen for incoming requests on this port.
# Change this if you need the app to run on a different port.
PORT = 9005

# Directory where log files will be saved
# Ensure this directory exists and the app has write permissions.
# All log-related activities will be stored in this directory.
# If the directory doesn't exist, the app might fail to write logs.
LOG_DIR = "/var/log/czentrix/"

# Name of the log file for this invoice processing service
# This log file will capture any relevant messages or errors related to
# the running of the invoice processing service.
LOG_FILENAME = "invoice_process.log"

# Name of the systemd service file associated with this application
# This is used by systemd to manage and track the service's status.
# The service file controls how the application is started, stopped, and restarted.
SERVICE_FILE = "invoice-process"
