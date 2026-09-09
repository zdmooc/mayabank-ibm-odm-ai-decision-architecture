FROM registry.access.redhat.com/ubi9/python-312:latest

USER 0
WORKDIR /opt/app-root/src
COPY . .
RUN chown -R 1001:0 /opt/app-root/src && chmod -R g=u /opt/app-root/src
USER 1001

ENV HOST=0.0.0.0 \
    PORT=8080 \
    DECISION_MODE=portable

EXPOSE 8080
CMD ["python", "api/reference_decision_api.py"]
