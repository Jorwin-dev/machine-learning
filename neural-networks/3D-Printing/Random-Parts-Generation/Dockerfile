FROM python:latest
RUN apt-get update
RUN apt-get install cmake git libblosc-dev libglfw3-dev libilmbase-dev libjemalloc-dev -y
RUN apt-get install liblog4cplus-dev libopenexr-dev libtbb-dev libz-dev -y
RUN apt-get install parallel patchelf python3-dev python3-numpy python3-pip unzip -y
RUN apt-get install libboost-python-dev -y
RUN apt-get install libopenvdb-tools python3-openvdb -y
#RUN apt-get install python3-matplotlib python3-meshio python3-numpy python3-pillow python3-skimage python3-scipy -y

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Build SDF: https://github.com/fogleman/sdf
RUN git clone https://github.com/fogleman/sdf.git
RUN pip install -e sdf

#RUN git clone https://github.com/AcademySoftwareFoundation/openvdb.git
#WORKDIR /openvdb
#RUN mkdir build
#WORKDIR /openvdb/build
#RUN cmake ..
#RUN make python


