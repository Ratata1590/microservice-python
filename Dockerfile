FROM alpine:latest as build-stage

WORKDIR /workspace
COPY docker-build/setup.sh /workspace/setup.sh
COPY requirements.txt /workspace/requirements.txt
RUN sh /workspace/setup.sh
COPY scripts/executor.py /workspace/executor.py
COPY docker-build/entrypoint.sh /entrypoint.sh

FROM scratch
COPY --from=build-stage / /
WORKDIR /workspace
ENTRYPOINT ["sh", "/entrypoint.sh"]