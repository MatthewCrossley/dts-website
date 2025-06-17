FROM debian:12
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

COPY . /backend/
RUN chmod -R 755 /backend/

WORKDIR /backend
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY run.sh /run.sh

EXPOSE 3000
EXPOSE 8000

ENTRYPOINT ["python"]
CMD ["-m", "fastapi", "run", "src/main.py"]
