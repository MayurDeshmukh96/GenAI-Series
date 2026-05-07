# base image
FROM python:3.11

# working dir
WORKDIR /app

# copy command
COPY . /app

# run command
RUN pip install -r requirements.txt

# port
EXPOSE 5000

# command

CMD ["python","./study_buddy.py"]

# CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=5000", "--no-browser", "--allow-root"] for notebook