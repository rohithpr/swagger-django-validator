FROM python:3.8

COPY entrypoint.sh /entrypoint.sh
COPY controller.py /controller.py

ENTRYPOINT [ "/entrypoint.sh" ]
