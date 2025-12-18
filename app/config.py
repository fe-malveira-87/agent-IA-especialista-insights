import os
from google import genai
from google.cloud import bigquery

# --- CONFIGURAÇÕES ---
PROJECT_ID = os.getenv("GCP_PROJECT", "prj-juma-farol360-poc")
PORT = int(os.environ.get("PORT", 8080))

# Caminho da chave (para rodar local vs docker)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_PATH = os.path.join(BASE_DIR, "service_account.json")
if os.path.exists(KEY_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH
    print(f"✅ Chave carregada: {KEY_PATH}")
else:
    print("⚠️ Aviso: service_account.json não encontrado (ok se estiver no Cloud Run).")

# --- CLIENTES (SINGLETON) ---
# Instanciamos aqui para importar nos outros arquivos
try:
    bq_client = bigquery.Client(project=PROJECT_ID)
    # Vertex AI init
    genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
    print(f"✅ Clientes GCP iniciados para projeto: {PROJECT_ID}")
except Exception as e:
    print(f"❌ Erro ao iniciar clientes: {e}")
    bq_client = None
    genai_client = None