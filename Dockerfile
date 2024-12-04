FROM python:3.13-slim

WORKDIR /app

RUN python -m venv /opt/venv

SHELL ["/bin/bash", "-c"]
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app

RUN pip install --no-cache-dir -Ur requirements.txt

EXPOSE 8002

CMD ["python3", "-m", "flask", "run"]
