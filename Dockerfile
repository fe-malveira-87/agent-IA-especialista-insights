# Usa Python 3.10
FROM python:3.10-slim

# Instala o uv dentro do container (copiando binário oficial)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# 1. Copia apenas arquivos de dependência primeiro (Cache Layer)
COPY pyproject.toml uv.lock ./

# 2. Instala dependências no ambiente do sistema (sem venv isolado, pois é container)
RUN uv sync --frozen --no-dev

# 3. Copia o código fonte
COPY . .

# Variáveis de ambiente padrão
ENV PORT=8080

# Comando de execução usando o ambiente gerenciado pelo uv
CMD ["uv", "run", "gunicorn", "--bind", ":8080", "app.main:app"]