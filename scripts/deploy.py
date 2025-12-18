import subprocess
import sys
import os

# --- CONFIGURAÇÕES DO PROJETO ---
PROJECT_ID = "prj-juma-farol360-poc"
REGION = "us-central1"
APP_NAME = "agente-juma-api"  # Nome do serviço no Cloud Run
IMAGE_TAG = f"gcr.io/{PROJECT_ID}/{APP_NAME}"

# Cores para o terminal
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

def run_command(command, step_name):
    """Executa um comando no shell e verifica erros."""
    print(f"\n{CYAN}--- INICIANDO: {step_name} ---{RESET}")
    print(f"Executando: {command}")
    
    try:
        # shell=True permite rodar como se estivesse digitando no terminal
        result = subprocess.run(command, shell=True, check=True, text=True)
        print(f"{GREEN}✔ SUCESSO: {step_name} concluído.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"\n{RED}❌ ERRO em {step_name}.{RESET}")
        print(f"{RED}O comando falhou. Verifique o log acima.{RESET}")
        
        # Dica específica para erros de autenticação comuns
        if "auth" in str(e) or "credentials" in str(e):
            print(f"\n{CYAN}DICA: Tente rodar 'gcloud auth login' no terminal.{RESET}")
            
        sys.exit(1)

def main():
    # 1. Verifica se o usuário está logado (opcional, mas boa prática)
    # run_command("gcloud auth print-access-token", "Verificação de Auth")

    # 2. Configura o projeto atual para garantir
    run_command(f"gcloud config set project {PROJECT_ID}", "Configurar Projeto")

    # 3. Build e Push da Imagem (Google Container Registry)
    # --quiet evita prompts de confirmação (Y/N)
    build_cmd = f"gcloud builds submit --tag {IMAGE_TAG} --quiet"
    run_command(build_cmd, "BUILD & PUSH (Criar Imagem)")

    # 4. Deploy no Cloud Run
    deploy_cmd = (
        f"gcloud run deploy {APP_NAME} "
        f"--image {IMAGE_TAG} "
        f"--region {REGION} "
        f"--platform managed "
        f"--allow-unauthenticated "
        f"--quiet"
    )
    run_command(deploy_cmd, "DEPLOY (Cloud Run)")

    print(f"\n{GREEN}🚀 DEPLOY COMPLETO! Seu backend está no ar.{RESET}")

if __name__ == "__main__":
    main()