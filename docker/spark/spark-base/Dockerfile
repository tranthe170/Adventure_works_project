FROM hive-base:latest
LABEL maintainer="GiaThe"

# Defining useful environment variables
ENV SPARK_VERSION=3.4.0  
ENV HADOOP_VERSION=3.3.2
ENV SCALA_VERSION=2.12.15  
ENV SCALA_HOME=/usr/share/scala
ENV SPARK_HOME=/usr/local/spark
ENV SBT_VERSION=1.5.5 
ENV PYTHONHASHSEED=1
ENV SPARK_EXECUTOR_MEMORY=2g
ENV SPARK_DRIVER_MEMORY=2g
ENV PATH=$SPARK_HOME/bin/:$PATH

# Upgrade and install some tools and dependencies
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \
    netcat \
    apt-utils \
    curl \
    vim \
    ssh \
    net-tools \
    ca-certificates \
    jq \
    wget \
    software-properties-common \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libnss3-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    liblzma-dev \
    tk-dev \
    libgmp-dev && \
    apt-get autoremove -yqq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installing Scala
WORKDIR /tmp

RUN wget --no-verbose "https://downloads.lightbend.com/scala/${SCALA_VERSION}/scala-${SCALA_VERSION}.tgz" && \
    tar zxf scala-${SCALA_VERSION}.tgz && \
    mkdir -p ${SCALA_HOME} && \
    mv "scala-${SCALA_VERSION}/bin" "scala-${SCALA_VERSION}/lib" "${SCALA_HOME}" && \
    ln -s "${SCALA_HOME}/bin/scala" "/usr/bin/scala" && \
    ln -s "${SCALA_HOME}/bin/scalac" "/usr/bin/scalac" && \
    ln -s "${SCALA_HOME}/bin/scaladoc" "/usr/bin/scaladoc" && \
    ln -s "${SCALA_HOME}/bin/scalap" "/usr/bin/scalap" && \
    rm -rf scala-${SCALA_VERSION}.tgz scala-${SCALA_VERSION}

# Installing SBT
RUN apt-get install -yqq ca-certificates wget tar && \
    mkdir -p "/usr/local/sbt" && \
    wget -qO - --no-check-certificate "https://github.com/sbt/sbt/releases/download/v${SBT_VERSION}/sbt-${SBT_VERSION}.tgz" | tar xz -C /usr/local/sbt --strip-components=1 && \
    export PATH="/usr/local/sbt/bin:$PATH" && \
    sbt sbtVersion

# Install Python 3.9 from official binaries (optimized for performance)
RUN wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz && \
    tar -xf Python-3.9.7.tgz && \
    cd Python-3.9.7 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall

# Set Python 3.9 as the default version
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.9 1

# Install pip and required Python packages
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.9 && \
    pip install numpy matplotlib scipy pandas simpy

# Installing Spark
WORKDIR ${SPARK_HOME}

RUN wget --no-verbose https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    tar zxf spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop3/* . && \
    rm -rf spark-${SPARK_VERSION}-bin-hadoop3.tgz spark-${SPARK_VERSION}-bin-hadoop3

# Use Spark with Hive (assuming HIVE_HOME is set properly in base image)
RUN cp ${HIVE_HOME}/conf/hive-site.xml $SPARK_HOME/conf

# Final cleanup to minimize image size
RUN apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /tmp/* /var/tmp/*

# Copy entrypoint script and set as executable
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

# Define entrypoint
ENTRYPOINT ["/entrypoint.sh"]
