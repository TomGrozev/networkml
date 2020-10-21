import random
from typing import ValuesView

from parsezeeklogs import ParseZeekLogs

import json

import requests

word_site = "https://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(word_site, headers=headers)
WORDS = response.content.decode('utf-8').splitlines()

ATTACK_IP = "10.0.2.6"
CLIENT_IP = "10.0.2.15"


def classify_record(record: str):
    if record['id.orig_h'] == ATTACK_IP:
        return "attack"
    elif record['id.orig_h'] == CLIENT_IP:
        return "normal"
    else:
        return None


def set_label(record: dict, label: str):
    label = label.lower()

    if label != "attack" and label != "normal":
        raise Exception("Not classified")

    record.update(label=label)
    return record


def escape_chars(record: dict):
    for key in record.keys():
        val: str = record[key]
        if isinstance(val, str):
            record[key] = val.translate(str.maketrans({'"': r'\"'}))
    return record


def fake_normal_record():
    cases = ["1", "3"]
    record = ["34406", "80", "/doSQL.php?case=%s&input=%s", "normal"]

    num_words = random.randint(1, 5)
    words = random.choices(WORDS, k=num_words)
    words = ' '.join(words)

    case = random.choice(cases)

    record[2] = record[2] % (case, words)

    return list_to_csv(record)


def dict_to_csv(record: dict):
    return list_to_csv(record.values())


def list_to_csv(list: list or ValuesView):
    return ','.join(['"%s"' % value for value in list])


with open('../data/out.csv', "w") as outfile:
    titles = ["sport", "dport", "uri", "label"]
    outfile.write(list_to_csv(titles) + "\n")
    for log_record in ParseZeekLogs("../data/zeeklogs/http.log", output_format="json", safe_headers=False,
                                    fields=["id.orig_h", "id.orig_p", "id.resp_p", "uri"]):
        if log_record is not None:
            log_record = json.loads(log_record)
            type_label = classify_record(log_record)
            if type_label is None:
                continue

            log_record = set_label(log_record, type_label)

            log_record.pop('id.orig_h', None)

            log_record = escape_chars(log_record)
            log_record = dict_to_csv(log_record)

            outfile.write(log_record + "\n")

    for _ in range(20000):
        outfile.write(fake_normal_record() + "\n")
