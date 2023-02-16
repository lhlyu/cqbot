FROM ghcr.io/igophper/go-cqhttp:master
FROM python

WORKDIR /app

COPY --from=0 /app/cqhttp ./go-cqhttp

COPY ./ .

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
