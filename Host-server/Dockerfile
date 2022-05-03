FROM nvcr.io/nvidia/l4t-ml:r32.7.1-py3

RUN apt-get update
RUN apt install software-properties-common -y
RUN apt install net-tools apt-utils -y
RUN python3 -m pip install --upgrade pip setuptools wheel
ADD sasha/requirements.txt .
RUN python3 -m pip install -r requirements.txt
RUN apt-get update
RUN apt-get install python3-tk -y
COPY . src
CMD ["cd", "/src"]
