FROM python:3.12-alpine

WORKDIR /app

COPY src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/app.py /app/app.py
COPY src/static /app/static
COPY run.sh /run.sh
RUN chmod +x /run.sh

ENV PORT=8091 NAKUPNI_DB=/data/nakupni.db
EXPOSE 8091

HEALTHCHECK --interval=30s --timeout=3s --start-period=8s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8091/healthz || exit 1

CMD ["/run.sh"]
