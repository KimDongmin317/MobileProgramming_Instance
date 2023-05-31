FROM ubuntu:20.04

LABEL maintainer "2gnldud@gmail.com"

RUN apt-get update && \
    apt-get install -y wget nano curl git bzip2 ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh

ENV PATH /opt/conda/bin:$PATH

RUN conda create -y --name my_env

RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate my_env" >> ~/.bashrc

SHELL ["/bin/bash", "--login", "-c"]

RUN conda init bash
#pytorch which is stable, Linux, pip, python and CPU only
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["sh", "-c", "/app/entrypoint.sh & tail -f /dev/null"]

CMD [ "/bin/bash" ]
