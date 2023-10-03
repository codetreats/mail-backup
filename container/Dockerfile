FROM codetreats/simple-pipeline:0.7.2
RUN apt-get update && apt-get install -q -y python3 python3-pip  python3-usb usbutils pipx imagemagick gsfonts
RUN pip install six
RUN pip install chardet
RUN pip install pdfkit
COPY src /src
COPY src/job.sh /job/
RUN chmod +x /src/*.sh
RUN echo "35 * * * * root /trigger.sh" > /etc/cron.d/cronjob
CMD ["/start.sh"]
