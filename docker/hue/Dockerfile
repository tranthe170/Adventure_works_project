FROM gethue/hue:latest

# Switch to root to perform privileged operations
USER root

# Install netcat to use in the wait-for-it function
RUN apt-get update && \
    apt-get install -yqq netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the entrypoint script
COPY ./entrypoint.sh ./

# Ensure entrypoint.sh is executable
RUN chmod +x ./entrypoint.sh

# Switch back to the default user (if necessary)
USER hue

# Set entrypoint to your custom script
ENTRYPOINT [ "./entrypoint.sh" ]

# Ensure the CMD is valid and executable
CMD ["./startup.sh"]
