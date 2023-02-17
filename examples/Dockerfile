FROM ghcr.io/igophper/go-cqhttp:master
FROM python

WORKDIR /app

COPY ./ .

COPY --from=0 /app/cqhttp ./go-cqhttp

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
