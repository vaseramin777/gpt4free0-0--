# Specify the base image for the Dockerfile. In this case, it is the official Selenium Chrome node image.
FROM selenium/node-chrome

# Define build arguments for the Dockerfile. These can be overridden during the build process.
ARG G4F_VERSION
ARG G4F_USER=g4f
ARG G4F_USER_ID=1000
ARG G4F_NO_GUI
ARG G4F_PASS=secret

# Set environment variables using the build arguments.
ENV G4F_VERSION $G4F_VERSION
ENV G4F_USER $G4F_USER
ENV G4F_USER_ID $G4F_USER_ID
ENV G4F_NO_GUI $G4F_NO_GUI

# Set various environment variables required for the Selenium Chrome node and the application.
ENV SE_SCREEN_WIDTH 1850
ENV PYTHONUNBUFFERED 1
ENV G4F_DIR /app
ENV G4F_LOGIN_URL http://localhost:7900/?autoconnect=1&resize=scale&password=$G4F_PASS
ENV HOME /home/$G4F_USER
ENV PATH $PATH:$HOME/.local/bin
ENV SE_DOWNLOAD_DIR $HOME/Downloads
ENV SEL_USER $G4F_USER
ENV SEL_UID $G4F_USER_ID
ENV SEL_GID $G4F_USER_ID

# Switch to the root user for installing packages and making system changes.
USER root

# If the build argument G4F_VERSION is empty, update the package lists and install git.
RUN if [ "$G4F_VERSION" = "" ] ; then \
  apt-get -qqy update && \
  apt-get -qqy install git \
  ; fi

# Install Python3, python-is-python3, and pip.
RUN apt-get -qqy update \
  && apt-get -qqy install \
    python3 \
    python-is-python3 \
    pip

# Remove openjdk-11-jre-headless.
RUN apt-get -qyy remove openjdk-11-jre-headless

# Clean up the apt cache and package lists.
RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
  && apt-get -qyy autoremove \
  && apt-get -qyy clean

# Update the supervisor configuration for the Selenium Chrome node.
COPY docker/supervisor.conf /etc/supervisor/conf.d/selenium.conf

# If the build argument G4F_NO_GUI is set, remove the supervisor-gui.conf file.
RUN if [ "$G4F_NO_GUI" ] ; then \
  rm /etc/supervisor/conf.d/gui.conf \
  ; fi

# Copy the background image for the desktop environment.
COPY docker/background.png /usr/share/images/fluxbox/ubuntu-light.png

# Add a user with the specified user ID and group ID.
RUN groupadd -g $G4F_USER_ID $G4F_USER \
  && useradd -rm -G sudo -u $G4F_USER_ID -g $G4F_USER_ID $G4F_USER \
  && echo "${G4F_USER}:${G4F_PASS}" | chpasswd

# Fix permissions for various directories and files.
RUN mkdir "${SE_DOWNLOAD_DIR}"
RUN chown "${G4F_USER_ID}:${G4F_USER_ID}" $SE_DOWNLOAD_DIR /var/run/supervisor /var/log/supervisor
