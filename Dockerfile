FROM python:3.8
RUN apt-get update && apt-get -y install pandoc r-base
RUN R -e 'install.packages("reticulate")'
RUN R -e 'install.packages("rmarkdown")'

ENV DOCS /docs
ENV REQUIREMENTS requirements.txt
ENV ENTRY render.py

COPY ${ENTRY} ${REQUIREMENTS}* ./
ENTRYPOINT ./${ENTRY}
