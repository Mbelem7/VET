FROM python:3.13-slim

# Instala dependencias mínimas para ODBC y el driver de Microsoft
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        unixodbc \
        unixodbc-dev \
        libgssapi-krb5-2 \
        curl \
        gnupg2 \
        apt-transport-https && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 10000

CMD ["python", "app.py"]