FROM python
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./pollyUpload.py /pollyUpload.py

CMD  python pollyUpload.py