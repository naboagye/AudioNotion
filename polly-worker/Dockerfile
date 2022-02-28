FROM python
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./getText.py /getText.py

CMD  python getText.py