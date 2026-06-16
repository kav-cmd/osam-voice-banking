FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8002

ENV PORT=8002
ENV JWT_SECRET=change-this-to-a-secure-random-string
ENV PHONE_ENCRYPT_KEY=change-this-to-a-fernet-key

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
