# longtou.2024
FROM gcr.io/deeplearning-platform-release/pytorch-cu121.2-3.py310

RUN apt update && apt install -y file # webdataset cache_dir error
WORKDIR /root
ADD Amphion /root/Amphion
WORKDIR /root/Amphion/preprocessors/Emilia
RUN ./setup_anaconda.sh conda amphion 3.10
RUN  . ./activate_python.sh  && . env.sh

CMD ["/bin/bash"]
