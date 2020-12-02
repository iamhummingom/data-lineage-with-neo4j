FROM continuumio/miniconda3

ENV ACCEPT_EULA=Y
# apt-get update
RUN apt-get update -y

ADD environment.yml /environment.yml
RUN conda env update -n base -f environment.yml --prune
COPY . /data_lineage/
WORKDIR /data_lineage
RUN chmod a+x main.py

CMD ["python", "main.py"]
