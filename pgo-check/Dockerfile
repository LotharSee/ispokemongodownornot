FROM python:2-wheezy

ENV GIT_REFERENCE a226795373da955752356e48e215a269473ead65

RUN wget https://github.com/LotharSee/pokemongo-api/archive/$GIT_REFERENCE.tar.gz
RUN tar xzf $GIT_REFERENCE.tar.gz
RUN mv ./pokemongo-api-$GIT_REFERENCE ./pokemongo-api

RUN pip install -r pokemongo-api/requirements.txt
RUN pip install datadog

WORKDIR ./pokemongo-api

COPY main.py main.py

CMD ["python", "main.py"]
