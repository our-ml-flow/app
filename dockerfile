FROM python:3.11.4

WORKDIR /home/runner/work/app/app

COPY . .

RUN pip install -r requirement.txt

CMD ["bash", "run.sh"]