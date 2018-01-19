FROM amazonlinux

RUN yum update -y && \
yum install -y shadow-utils \
which \
gcc \
zlib \
zlib-devel \
openssl \
openssl-devel \
#cmake \
#gcc-c++ \
zip \
unzip \
git-all && \
yum clean headers && \
yum clean packages

# RUN yum install -y unzip

#install AWS CLI
RUN mkdir -p /tmp
WORKDIR /tmp
RUN curl -s "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o awscli-bundle.zip &&  \
unzip awscli-bundle.zip && \
./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws && \
rm -fr awscli-bundle && \
rm awscli-bundle.zip

#PIP
RUN curl -s https://bootstrap.pypa.io/get-pip.py | python

#Python 3.6
RUN curl -s https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz -o Python-3.6.3.tgz && \
tar -zxpf Python-3.6.3.tgz && \
cd Python-3.6.3 && \
./configure && \
make && \
make install && \
cd .. && \
rm -fr Python-3.6.3 && \
rm Python-3.6.3.tgz

#Add User
RUN adduser dev
RUN mkdir -p /home/dev && chown -R dev: /home/dev

RUN mkdir /home/dev/Envs
RUN touch /home/dev/Envs/.exist
RUN chown -R dev:dev /home/dev/Envs

#This will hold our virtualenv
VOLUME ["/home/dev/Envs"]

#This is where we should mount our drive with our source code
VOLUME ["/home/dev/code"]

VOLUME /home/dev/.aws

USER dev
WORKDIR /home/dev

USER root
RUN git clone https://github.com/magicmonty/bash-git-prompt.git .bash-git-prompt --depth=1
RUN echo "GIT_PROMPT_ONLY_IN_REPO=1" >> .bashrc
RUN echo "source ~/.bash-git-prompt/gitprompt.sh" >> .bashrc

RUN pip install virtualenvwrapper
ENV HOME /home/dev
ENV PATH /home/dev/.local/bin:/usr/local/bin:${PATH}

#python-lambda works much better with virtualenvwrapper
ENV WORKON_HOME=/home/dev/Envs
ENV VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
RUN mkdir -p ${WORKON_HOME}

RUN chown -R dev: /home/dev
USER dev
ENV LC_ALL en_US.UTF-8
WORKDIR /home/dev
CMD /bin/bash
