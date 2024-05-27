FROM python:3.10-alpine3.17
ARG vcs-ref=0
ENV BUILD_ID=$vcs-ref

ENV MONGODB_URI = None
ENV MONGODB_DB = None

WORKDIR /app
COPY Pipfile ./
COPY Pipfile.lock ./
RUN  pip3 install pipenv  \
    && pipenv requirements > requirements.txt \
    && pip3 install -r requirements.txt
COPY . .

EXPOSE 443
CMD ["sh","deploy.sh"]