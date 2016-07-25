FROM python:2-wheezy

ENV GIT_REFERENCE f7a97a7e1247b493cc8f12f5716bb8da12a64c08 

RUN wget https://github.com/LotharSee/pokemongo-api/archive/$GIT_REFERENCE.tar.gz
RUN tar xzf $GIT_REFERENCE.tar.gz
RUN mv ./pokemongo-api-$GIT_REFERENCE ./pokemongo-api

RUN pip install -r pokemongo-api/requirements.txt
RUN pip install datadog

WORKDIR ./pokemongo-api

COPY main.py main.py

CMD ["python", "main.py"]
