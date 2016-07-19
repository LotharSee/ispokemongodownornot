FROM python:2-wheezy

ENV GIT_REFERENCE 874c48b1daef5221409c47de74478bbba13240b6

RUN wget https://github.com/rubenvereecken/pokemongo-api/archive/$GIT_REFERENCE.tar.gz
RUN tar xzf $GIT_REFERENCE.tar.gz
RUN mv ./pokemongo-api-$GIT_REFERENCE ./pokemongo-api

RUN pip install -r pokemongo-api/requirements.txt
RUN pip install datadog

WORKDIR ./pokemongo-api

COPY main.py main.py

CMD ["python", "main.py"]
