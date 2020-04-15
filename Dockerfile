FROM python:3.8
RUN apt-get update && apt-get -y install pandoc r-base
RUN R -e 'install.packages("reticulate")'
RUN R -e 'install.packages("rmarkdown")'

ENV VIRTUAL_ENV=venv DOCS=/docs
VOLUME ${DOCS}

ENV SETUP setup
ENV ENTRY render.py

COPY ${ENTRY} ${SETUP} /
ENTRYPOINT bash -c "source ./${SETUP} && ./${ENTRY}"
