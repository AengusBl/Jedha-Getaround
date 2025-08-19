FROM python:3.12

RUN useradd -m -u 1000 user

USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 7860

COPY --chown=user . .
CMD ["streamlit", "run", "app.py", "--server.port=7860"]