all: help

help:
	@printf '\nusuage make ...\n'
	@printf '  build-image  -> builds container using podman and packs .tar.xz\n'
	@printf '  start-server -> build container and start test-server\n'
	@printf '  remove-image -> remove valheim image from local podman archive\n\n'

build-image: SERVER_VERSION = 0-212-9
build-image: build-container.sh Dockerfile
	SERVER_VERSION=${SERVER_VERSION} ./build-container.sh
	podman save localhost/valheim-server:${SERVER_VERSION} -o valheim-server-${SERVER_VERSION}.tar
	pxz -9 valheim-server-${SERVER_VERSION}.tar
	@printf '\nUpload the tar.xz to the target server and than execute:\n'
	@printf '  xz -d -v valheim-server-${SERVER_VERSION}.tar.xz\n'
	@printf '  podman image load -i valheim-server-${SERVER_VERSION}.tar\n'

start-server: SERVER_VERSION = 0-212-9
start-server: docker-start-server.sh build-container.sh Dockerfile
	SERVER_VERSION=${SERVER_VERSION} ./docker-start-server.sh

remove-image: SERVER_VERSION = 0-212-9
remove-image:
	podman rm valheim || true
	podman image rm localhost/valheim-server:${SERVER_VERSION} || true

.dockerignore:
	@printf 'creating .dockerignore\n'
	@printf '\n' > .dockerignore

scripts:
	@printf 'creating scripts/\n'
	@mkdir -p scripts

scripts/start-server.sh: scripts
	@printf 'creating scripts/start-server.sh\n'
	@printf '#\!/bin/bash\n' > scripts/start-server.sh
	@printf 'set -o xtrace\n\n' >> scripts/start-server.sh
	@printf 'if [ "$${CONFIG_PUBLIC}" = "false" -o "$${CONFIG_PUBLIC}" = 0 ]; then\n' >> scripts/start-server.sh
	@printf '  PUBLIC="-public 0"\n' >> scripts/start-server.sh
	@printf 'fi\n\n' >> scripts/start-server.sh
	@printf 'if [ "$${CONFIG_CROSSPLAY}" = "true" -o "$${CONFIG_CROSSPLAY}" = 1 ]; then\n' >> scripts/start-server.sh
	@printf '  CROSSPLAY="-crossplay"\n' >> scripts/start-server.sh
	@printf 'fi\n\n' >> scripts/start-server.sh
	@printf 'if [[ -z "$${CONFIG_SAVEINTERVAL}" ]]; then\n' >> scripts/start-server.sh
	@printf '  SAVEINTERVAL="-saveinterval "$${CONFIG_SAVEINTERVAL}\n' >> scripts/start-server.sh
	@printf 'fi\n\n' >> scripts/start-server.sh
	@printf 'if [[ -z "$${CONFIG_BACKUP_AMOUNT}" ]]; then\n' >> scripts/start-server.sh
	@printf '  BACKUPS="-backups "$${CONFIG_BACKUP_AMOUNT}\n' >> scripts/start-server.sh
	@printf 'fi\n\n' >> scripts/start-server.sh
	@printf 'export SteamAppId=892970\n\n' >> scripts/start-server.sh
	@printf '/irongate/valheim_server.x86_64 -name "$${CONFIG_SERVER_NAME}" -world "$${CONFIG_WORLD_NAME}" -password "$${CONFIG_SERVER_PW}" $${PUBLIC} $${CROSSPLAY} -nographics -batchmode  $${SAVEINTERVAL} $${BACKUPS} -savedir "/config"\n' >> scripts/start-server.sh
	@chmod +x scripts/start-server.sh

Dockerfile: .dockerignore scripts/start-server.sh
	@printf 'creating Dockerfile\n'
	@printf 'FROM ubuntu:22.04\n' > Dockerfile
	@printf 'LABEL vendor=Iron\\ Gate\\ Studio \\\n' >> Dockerfile
	@printf '      se.irongatestudio.last-change="2022-09-29"\n' >> Dockerfile
	@printf 'RUN apt-get update && apt-get install -y \\\n' >> Dockerfile
	@printf '    curl \\\n' >> Dockerfile
	@printf '    libatomic1 \\\n' >> Dockerfile
	@printf '    libpulse-dev \\\n' >> Dockerfile
	@printf '    libpulse0 \\\n' >> Dockerfile
	@printf '    && rm -rf /var/lib/apt/lists/*\n' >> Dockerfile
	@printf 'COPY docker/steamclient.so                /usr/lib\n' >> Dockerfile
	@printf 'COPY valheim_server_Data                  /irongate/valheim_server_Data\n' >> Dockerfile
	@printf 'COPY scripts                              /irongate/scripts\n' >> Dockerfile
	@printf 'COPY valheim_server.x86_64 UnityPlayer.so /irongate/\n' >> Dockerfile
	@printf 'WORKDIR /irongate\n' >> Dockerfile
	@printf 'ENV PATH="/irongate:$${PATH}"\n' >> Dockerfile
	@printf 'CMD ["/bin/bash", "scripts/start-server.sh"]\n' >> Dockerfile

build-container.sh: Dockerfile
	@printf 'creating build-container.sh\n'
	@printf '#\!/bin/bash\n' > build-container.sh
	@printf 'CONTAINER_TAG_NAME=valheim-server\n' >> build-container.sh
	@printf 'CONTAINER_TAG_VERSION=$${SERVER_VERSION}\n\n' >> build-container.sh
	@printf 'set -e\n\n' >> build-container.sh
	@printf 'if ! /usr/bin/podman inspect "$${CONTAINER_TAG_NAME}:$${CONTAINER_TAG_VERSION}" > /dev/null 2>&1\n' >> build-container.sh
	@printf 'then\n' >> build-container.sh
	@printf '    printf "Building Container Image: $${CONTAINER_TAG_NAME}:$${CONTAINER_TAG_VERSION} ...\\n"\n' >> build-container.sh
	@printf '    /usr/bin/podman build . -t "$${CONTAINER_TAG_NAME}:$${CONTAINER_TAG_VERSION}"\n' >> build-container.sh
	@printf '    printf "container created\\n"\n' >> build-container.sh
	@printf 'else\n' >> build-container.sh
	@printf '    printf "Container Image: $${CONTAINER_TAG_NAME}:$${CONTAINER_TAG_VERSION} already exists! \\n"\n' >> build-container.sh
	@printf 'fi\n' >> build-container.sh
	@chmod +x build-container.sh

docker-start-server.sh: build-container.sh
	@printf 'creating docker-start-server.sh\n'
	@printf '#\!/bin/sh\n' > docker-start-server.sh
	@printf 'CONTAINER_TAG_NAME=valheim-server\n' >> docker-start-server.sh
	@printf 'CONTAINER_TAG_VERSION=$${SERVER_VERSION}\n' >> docker-start-server.sh
	@printf 'CONTAINER_CONFIG_VOLUME=config\n\n' >> docker-start-server.sh
	@printf 'export CONFIG_SERVER_NAME="Test Server"\n' >> docker-start-server.sh
	@printf 'export CONFIG_WORLD_NAME="test_world"\n' >> docker-start-server.sh
	@printf 'export CONFIG_SERVER_PW="Test1234"\n' >> docker-start-server.sh
	@printf 'export CONFIG_PUBLIC=true\n' >> docker-start-server.sh
	@printf 'export CONFIG_CROSSPLAY=true\n' >> docker-start-server.sh
	@printf 'export CONFIG_SAVEINTERVAL=300\n' >> docker-start-server.sh
	@printf 'export CONFIG_BACKUP_AMOUNT=10\n\n' >> docker-start-server.sh
	@printf 'set -e\n\n' >> docker-start-server.sh
	@printf 'if ! podman ps > /dev/null 2>&1\n' >> docker-start-server.sh
	@printf 'then\n' >> docker-start-server.sh
	@printf '    echo "Is podman installed and is your user a member of the "docker" group?"\n' >> docker-start-server.sh
	@printf '    exit 1\n' >> docker-start-server.sh
	@printf 'fi\n\n' >> docker-start-server.sh
	@printf 'SERVER_VERSION=$${SERVER_VERSION} ./build-container.sh\n\n' >> docker-start-server.sh
	@printf 'mkdir -p $${CONTAINER_CONFIG_VOLUME}\n\n' >> docker-start-server.sh
	@printf 'podman rm valheim || true\n' >> docker-start-server.sh
	@printf 'podman run -it --name valheim \\\n' >> docker-start-server.sh
	@printf '  -v "$$PWD/$${CONTAINER_CONFIG_VOLUME}:/config:z" \\\n' >> docker-start-server.sh
	@printf '  -e CONFIG_SERVER_NAME -e CONFIG_WORLD_NAME -e CONFIG_SERVER_PW \\\n' >> docker-start-server.sh
	@printf '  -e CONFIG_PUBLIC -e CONFIG_CROSSPLAY -e CONFIG_SAVEINTERVAL \\\n' >> docker-start-server.sh
	@printf '  -e CONFIG_BACKUP_AMOUNT \\\n' >> docker-start-server.sh
	@printf '  "localhost/$${CONTAINER_TAG_NAME}:$${CONTAINER_TAG_VERSION}" "$$@"\n' >> docker-start-server.sh
	@chmod +x docker-start-server.sh

