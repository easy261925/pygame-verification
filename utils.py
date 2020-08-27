import re

# 过滤掉所有标点符号


def removePunctuation(text):
    result = re.sub(r'[^\w\s]', '', text)
    return result.strip()
