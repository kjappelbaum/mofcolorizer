# We install openbabel from conda as everything else would be a complete pain
FROM  continuumio/miniconda3:4.8.2

# JRE is needed for MOFid. We should drop this dependency as it makes the code slow and is unnecessary.
COPY install_packages.sh .
RUN ./install_packages.sh

COPY requirements.txt .
RUN pip install  --no-cache-dir -r requirements.txt

RUN git clone https://github.com/snurr-group/mofid.git && cd mofid && make init && python set_paths.py && pip install .
RUN conda install --yes --freeze-installed -c openbabel openbabel==2.4.1  && conda install --yes --freeze-installed lightgbm && conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

COPY ./mofcolorizer  ./mofcolorizer
COPY run_app.py .
COPY Procfile .
COPY logging.conf .
COPY gunicorn_conf.py .

EXPOSE 8091
CMD ["gunicorn", "-b", "0.0.0.0:8091", "-c", "gunicorn_conf.py", "--log-config", "logging.conf", "run_app:server"]
