# SMDR Sleuth

SMDR Sleuth is a tool for ingesting Avaya IP Office SMDR data, storing it locally, and presenting it in a modern web interface. It features a Python backend (FastAPI, SQLAlchemy), a React frontend, and supports containerized deployment via Docker Compose.


## Prerequisites
- Docker and Docker Compose installed

---

## Installation (Docker Compose)


Create a `docker-compose.yml` file like the following:

```yaml
version: '3.8'
services:
  smdr-sleuth:
    image: aarondyck/smdr-sleuth:latest
    container_name: smdr-sleuth
    ports:
      - "5173:5173"   # React frontend
      - "5000:5000"   # SMDR TCP ingestion
    restart: unless-stopped
```

Start the application:
```
docker-compose up -d
```
Access the web interface at `http://<ip-or-dns-of-server>`.

---


## HTTPS Setup

### Using Nginx as a Reverse Proxy

Create an `nginx.conf` file like this:
```nginx
user  nginx;
worker_processes  auto;
error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    # SSL configuration (uncomment and configure for HTTPS)
    # server {
    #     listen              443 ssl;
    #     server_name         <YOUR_DOMAIN>;
    #     ssl_certificate     /etc/nginx/certs/fullchain.pem;
    #     ssl_certificate_key /etc/nginx/certs/privkey.pem;
    #     ssl_protocols       TLSv1.2 TLSv1.3;
    #     ssl_ciphers         HIGH:!aNULL:!MD5;
    # }

    server {
        listen       80;
        server_name  _;

        location / {
            proxy_pass http://smdr-sleuth:5173;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api/ {
            proxy_pass http://smdr-sleuth:8000/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

To add Nginx to your Docker Compose setup, include the following service:

```yaml
  nginx:
    image: nginx:latest
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro  # Place your SSL certs here
    depends_on:
      - smdr-sleuth
```

### Using Let's Encrypt for Certificates

You can use [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy) and [docker-letsencrypt-nginx-proxy-companion](https://github.com/nginx-proxy/docker-letsencrypt-nginx-proxy-companion) for automatic Let's Encrypt certificates. Example:

```yaml
  nginx-proxy:
    image: nginxproxy/nginx-proxy
    container_name: nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro

  letsencrypt-companion:
    image: nginxproxy/acme-companion
    container_name: letsencrypt-companion
    environment:
      NGINX_PROXY_CONTAINER: nginx-proxy
      ACME_CA_URI: https://acme-v02.api.letsencrypt.org/directory
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./certs:/etc/nginx/certs
```
- Set environment variables like `VIRTUAL_HOST` and `LETSENCRYPT_HOST` in your backend/frontend service definitions.
- See the companion documentation for full details.

### Using a Third-Party Certificate

If you have an SSL certificate from a third-party provider (e.g., DigiCert, Comodo, etc.), place your certificate and key files in the `certs` directory (e.g., `fullchain.pem`, `privkey.pem`).
Update the `nginx.conf` file to reference these paths in the SSL section:

```nginx
    # server {
    #     listen              443 ssl;
    #     server_name         <YOUR_DOMAIN>;
    #     ssl_certificate     /etc/nginx/certs/fullchain.pem;
    #     ssl_certificate_key /etc/nginx/certs/privkey.pem;
    #     ssl_protocols       TLSv1.2 TLSv1.3;
    #     ssl_ciphers         HIGH:!aNULL:!MD5;
    # }
```

---

### Start the Application
```
docker-compose up -d
```
- Access the web interface at `http://<<ip-or-dns-of-server>>`.

---
```yaml
services:
  smdr-sleuth:
    image: aarondyck/smdr-sleuth:latest
    container_name: smdr-sleuth
    ports:
      - "8000:8000"   # FastAPI backend
      - "5173:5173"   # React frontend
      - "5000:5000"   # SMDR TCP ingestion
    restart: unless-stopped

  nginx:
    image: nginx:latest
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro  # Place your SSL certs here
    depends_on:
      - smdr-sleuth
```

### Example `nginx.conf`
```nginx
user  nginx;
worker_processes  auto;
error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    # SSL configuration (uncomment and configure for HTTPS)
    # server {
    #     listen              443 ssl;
    #     server_name         <YOUR_DOMAIN>;
    #     ssl_certificate     /etc/nginx/certs/fullchain.pem;
    #     ssl_certificate_key /etc/nginx/certs/privkey.pem;
    #     ssl_protocols       TLSv1.2 TLSv1.3;
    #     ssl_ciphers         HIGH:!aNULL:!MD5;
    # }

    server {
        listen       80;
        server_name  _;

        location / {
            proxy_pass http://smdr-sleuth:5173;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api/ {
            proxy_pass http://smdr-sleuth:8000/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Start the Application
```
docker-compose up -d
```
- Access the web interface at `http://<<ip-or-dns-of-server>>`.

---

---

## Using Nginx as a Reverse Proxy (Recommended)

### 1. Add Nginx to Docker Compose
Add the following service to your `docker-compose.yml`:

```yaml
  nginx:
    image: nginx:latest
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Docker/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro  # Place your SSL certs here
    depends_on:
      - backend
      - frontend
```

### 2. SSL Certificates
- Place your SSL certificate and key files in the `certs` directory (e.g., `fullchain.pem`, `privkey.pem`).
- Update the `nginx.conf` file to reference these paths in the SSL section.

### 3. Using Let's Encrypt (Automatic SSL)
You can use [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy) and [docker-letsencrypt-nginx-proxy-companion](https://github.com/nginx-proxy/docker-letsencrypt-nginx-proxy-companion) for automatic Let's Encrypt certificates. Example:

```yaml
  nginx-proxy:
    image: nginxproxy/nginx-proxy
    container_name: nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro

  letsencrypt-companion:
    image: nginxproxy/acme-companion
    container_name: letsencrypt-companion
    environment:
      NGINX_PROXY_CONTAINER: nginx-proxy
      ACME_CA_URI: https://acme-v02.api.letsencrypt.org/directory
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./certs:/etc/nginx/certs
```
- Set environment variables like `VIRTUAL_HOST` and `LETSENCRYPT_HOST` in your backend/frontend service definitions.
- See the companion documentation for full details.

---

### Using Docker Compose
A sample `docker-compose.yml` is provided in the `Docker` folder. Edit as needed for your environment.

```
docker-compose -f Docker/docker-compose.yml up -d
```

### Reverse Proxy (Optional)
Sample configs for Nginx, Caddy, Traefik, Apache, HAProxy, and Envoy are available in the `Docker` folder. Use these to route traffic and enable SSL if desired.

## Configuration
- Update environment variables and config files as needed for your deployment.
- Replace IP addresses and certificate paths in reverse proxy configs.

## Application Structure
- `backend/`: Python backend (FastAPI, SQLAlchemy, SMDR ingestion)
- `web/`: React frontend
- `Docker/`: Dockerfile, entrypoint.sh, docker-compose.yml, reverse proxy configs

## Support
For issues or feature requests, open an issue on GitHub or contact the maintainer.

---

**Docker Hub Image:** [`aarondyck/smdr-sleuth:latest`](https://hub.docker.com/r/aarondyck/smdr-sleuth)

**License:** Creative Commons Attribution-NonCommercial (CC BY-NC)

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. You may not use the code or images for commercial purposes.

See the full license text at: https://creativecommons.org/licenses/by-nc/4.0/
