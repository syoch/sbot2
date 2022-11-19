FROM python:3

RUN pip install --upgrade pip
RUN pip install py-cord==1.7.3
RUN pip install matplotlib numpy
RUN pip install timeout-decorator==0.5.0
RUN pip install python-dotenv==0.19.2

CMD ./scripts/run.sh