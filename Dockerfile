FROM python:3.10-alpine3.17
ARG vcs-ref=0
ENV BUILD_ID=$vcs-ref

RUN  pip3 install pipenv  \
    && pipenv requirements > requirements.txt \
    && pip3 install -r requirements.txt

EXPOSE 443
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","443"]