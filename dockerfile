FROM ubuntu:12.04
MAINTAINER Dhash Shrivathsa dhash@outlook.com
RUN apt-get update
RUN apt-get install ansible 
RUN git clone https://github.com/Aeolus0/Flask-apps.git
RUN ansible-playbook /home/Flask-apps/sys_deps/ansible/server_local.yaml >> /home/package.log
RUN pip install -r /home/Flask-apps/requirements.txt
RUN python /home/Flask-apps/run.py
EXPOSE 5000