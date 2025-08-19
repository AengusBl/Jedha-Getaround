FROM continuumio/miniconda3

RUN apt-get update
RUN apt-get install nano unzip curl -y

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

CMD mlflow server -p 7860 \
    --host 0.0.0.0 \
    --backend-store-uri $BACKEND_STORE_URI \
    --default-artifact-root $ARTIFACT_STORE_URI