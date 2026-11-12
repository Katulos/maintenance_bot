ARG VARIANT="base:trixie"

FROM mcr.microsoft.com/devcontainers/${VARIANT}

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
     apt-transport-https \
     git-flow \
     gpg \
     postgresql-client

RUN apt-get clean

# RUN wget -O $WORKSPACE/Codeium.codeium-1.48.2.vsix https://open-vsx.org/api/Codeium/codeium/1.48.2/file/Codeium.codeium-1.48.2.vsix
