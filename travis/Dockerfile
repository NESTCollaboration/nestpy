FROM quay.io/pypa/manylinux1_x86_64

LABEL maintainer="@nestpy"
ENV PATH=$PATH:/usr/local/bin

RUN yum install -y atlas-devel wget

RUN cd /root && wget http://astroparticle.rice.edu/v2.8.12.tar.gz && tar xfz v2.8.12.tar.gz && cd CMake-2.8.12 && ./bootstrap  && make && make install 


