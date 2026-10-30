FROM nginx:1.27-alpine

COPY app/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8091

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8091/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
