server {
    listen 80;
    listen [::]:80;

    server_name {site_name} www.{site_name};
    access_log  /home/{project_name}/www/{site_name}/logs/nginx_logs/access_log.log;
    return 301 https://{site_name}.com$request_uri;
}

server {
    listen 443 ssl http2;

    server_name {site_name} www.{site_name}.com;
    access_log  /home/{project_name}/www/{site_name}/logs/nginx_logs/access_log.log;

    ssl on;
    ssl_certificate /home/{project_name}/.ssl/{project_name}.com.crt;
    ssl_certificate_key /home/{project_name}/.ssl/{project_name}.com.key;

    client_max_body_size 32m;

    location /static/ {
        root /home/{project_name}/www/{site_name}.com/www/;
        expires 30d;
    }
    location /media/ {
        root /home/{project_name}/www/{site_name}.com/www/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}