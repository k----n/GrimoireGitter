FROM jupyter/scipy-notebook
USER root
RUN apt-get update && apt-get install gcc libmariadb3 libmariadb-dev -y
USER $NB_UID
RUN pip install --quiet --no-cache-dir mariadb python-Levenshtein elasticsearch
