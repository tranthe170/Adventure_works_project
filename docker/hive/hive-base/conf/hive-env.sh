# Set Hive and Hadoop environment variables here.

# Set HADOOP_HOME to point to your Hadoop installation
export HADOOP_HOME=/opt/hadoop

# Set HADOOP_CONF_DIR to point to your Hadoop configuration directory
export HADOOP_CONF_DIR=/etc/hadoop

# Set the Hadoop executable path
export HADOOP=/opt/hadoop/bin/hadoop

# Ensure the correct Hadoop version is identified
export HADOOP_VERSION=$($HADOOP version | grep -i "Hadoop" | head -n 1 | cut -d' ' -f 2)

# Optionally set the Hive configuration directory
# export HIVE_CONF_DIR=/path/to/hive/conf

# Optional: Set Hive heap size (increase if you are processing large data)
# export HADOOP_HEAPSIZE=1024
