FROM nginx:1.26.1
COPY templates/general_pages/index.html /usr/share/nginx/html/index.html
COPY ./nginx /etc/nginx
COPY ./letsencrypt /etc/letsencrypt
