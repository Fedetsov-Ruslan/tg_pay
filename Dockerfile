FROM python:3.12.2-slim-bullseye
WORKDIR /
EXPOSE 55582
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh", "-c", "python app/run.py"]