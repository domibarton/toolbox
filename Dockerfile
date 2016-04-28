FROM python:2.7-slim

MAINTAINER dbarton

#
# Add user.
#

RUN \
    groupadd -g 666 toolbox && \
    useradd -u 666 -g 666 -d /toolbox -c "Toolbox User" toolbox

#
# Install start script.
#

COPY docker/toolbox.init /toolbox.init
RUN chmod 755 /toolbox.init

#
# Install Toolbox.
#

COPY toolbox /toolbox

#
# Install required packages.
#

COPY requirements.txt /requirements.txt
RUN \
    apt-get -y update && \
    apt-get -y install sudo gcc && \
    pip install --no-cache-dir -r /requirements.txt && \
    apt-get -y remove gcc && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt/lists/* \
    rm -rf /tmp/*

#
# Configure sudo.
#

COPY docker/sudoers /etc/sudoers
RUN chmod 440 /etc/sudoers

#
# Set container settings.
#

VOLUME /toolbox/static /toolbox/db.sqlite3 /toolbox/toolbox/settings_custom.py
EXPOSE 8080

#
# Start process.
#

WORKDIR /toolbox
CMD ["/toolbox.init"]
