FROM nginx:stable-alpine
RUN rm /etc/nginx/conf.d/default.conf

COPY fullchain.pem /etc/letsencrypt/live/www.nanyte.design/fullchain.pem
COPY privkey.pem /etc/letsencrypt/live/www.nanyte.design/privkey.pem

RUN cat /etc/letsencrypt/live/www.nanyte.design/fullchain.pem

COPY nginx.conf /etc/nginx/conf.d

EXPOSE 80
