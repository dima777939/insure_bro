FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/insure_bro
WORKDIR /usr/src/insure_bro
COPY requirements.txt /usr/src/insure_bro/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/insure_bro/entrypoint.sh
RUN chmod +x /usr/src/insure_bro/entrypoint.sh
ADD . /usr/src/insure_bro/
ENTRYPOINT ["/usr/src/insure_bro/entrypoint.sh"]