FROM alpine:3.24
LABEL image.authors="{{ cookiecutter.author }}"
WORKDIR /home/{{ cookiecutter.project_slug }}/
COPY pyproject.toml pyproject.toml
COPY main.py main.py
COPY policy.yaml policy.yaml
COPY skills/ skills/
COPY tools/ tools/
COPY uv.lock uv.lock
ENV UV_PYTHON_INSTALL_DIR=/home/{{ cookiecutter.project_slug }}/.uv-python
RUN apk add --no-cache python3=3.14.7-r1 uv=0.11.19-r0 && \
    apk upgrade --no-cache libcrypto3 libssl3 &&\
    uv sync --frozen --python /usr/bin/python3 && \
    addgroup -g 1000 {{ cookiecutter.project_slug }} &&\
    adduser -D -G {{ cookiecutter.project_slug }} -u 1000 {{ cookiecutter.project_slug }} -h /home/{{ cookiecutter.project_slug }}/ &&\
    mkdir -p /home/{{ cookiecutter.project_slug }}/workspace &&\
    chmod ug+rwx,o+rx,g+s /home/{{ cookiecutter.project_slug }}/workspace &&\
    chown -R {{ cookiecutter.project_slug }}:{{ cookiecutter.project_slug }} /home/{{ cookiecutter.project_slug }}/
ENV PATH="/home/{{ cookiecutter.project_slug }}/.venv/bin:$PATH"
USER 1000
EXPOSE {{ cookiecutter.port }}
CMD [ "python", "-m", "main" ]
