FROM python:3.13-slim

# Instala dependências do sistema necessárias para compilar pacotes e postgres
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala o 'uv' globalmente
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de configuração de dependências primeiro
COPY pyproject.toml uv.lock* ./

# Instala as dependências diretamente do pyproject.toml usando o uv
RUN uv pip install --system --no-cache .

# Copia o restante do código do projeto para dentro do container
COPY . .

# Diz ao Python para enxergar a pasta 'src' como raiz para os imports
ENV PYTHONPATH=/app/src

# Expõe a porta padrão do FastAPI
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]