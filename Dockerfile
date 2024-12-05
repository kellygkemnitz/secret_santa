FROM python:3.9.21-slim-bookworm

WORKDIR /app

RUN python -m venv /opt/venv

SHELL ["/bin/bash", "-c"]
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
COPY templates templates/
COPY secret_santa.py app.py 

#RUN pip install --upgrade pip
RUN pip install --no-cache-dir -Ur requirements.txt

EXPOSE 8082

CMD ["python3", "app.py"]
