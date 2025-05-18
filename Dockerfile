FROM python:3.12-slim


# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar os arquivos do projeto
COPY . /app

