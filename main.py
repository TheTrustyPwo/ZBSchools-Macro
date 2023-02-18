import re
import time
import json
import logging
import random
import selenium.common
from pypinyin import pinyin
from selenium import webdriver
from selenium.webdriver.common.by import By


# Initialize constants
MCQ_CHOICE = ('A', 'B', 'C', 'D')
PASSAGE_TEMPLATE_URL = 'https://www.zbschools.sg/stories-{id}'
QUESTION_TEMPLATE_URL = 'https://www.zbschools.sg/cos/o.x?c=/ca7_zbs/zbs&func=quiz&tid=1&rid={id}&litebox=0&popup=1'

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Load from configuration file
with open('config.json', 'r') as fp:
    CONFIG = json.load(fp)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path='chromedriver.exe')

# Initialize cookies
# Enables network tracking to use the Network.setCookie method
driver.execute_cdp_cmd('Network.enable', {})

with open('cookies.json', 'r') as fp:
    data = json.load(fp)
    for cookie in data:
        cookie["sameSite"] = "None"  # Overrides null value when exported from CookieEditor
        driver.execute_cdp_cmd('Network.setCookie', cookie)  # Actually set the cookie

# Disable network tracking to not affect performance
driver.execute_cdp_cmd('Network.disable', {})


def clean(text: str) -> str:
    """
    Utility function to clean a text, stripping away all punctuation and special characters
    to better facilitate regex parsing
    :param text: Text to clean
    :return:
    """
    special = ('\n', '\t', ' ')
    punctuation = ('“', '”', '。', '，', '、', '：', '？', ';', '！', '(', ')', '[', ']', '{', '}', '《', '》', '…', '·', "'")
    for symbol in special + punctuation:
        text = text.replace(symbol, '')
    return text


def solve_article(article_id: int):
    """
    Function to process an article, and solve its questions
    :param article_id: ID of the article, i.e. the number after `story-`
    :return:
    """
    logging.info(f'Processing Article {article_id}')
    driver.get(PASSAGE_TEMPLATE_URL.format(id=article_id))

    # Process passage text to be used to answer questions later on
    paragraphs = driver.find_elements(By.CLASS_NAME, 'zbs_sent')

    # Invalid article as there are no paragraphs
    if not paragraphs:
        logging.warning('Skipping as invalid ID')
        return 0

    # Process and clean paragraphs into passage variable
    passage = ''.join(list(map(lambda v: v.text, paragraphs)))
    passage = clean(passage)

    driver.get(QUESTION_TEMPLATE_URL.format(id=article_id))

    # Finding question elements
    questions = driver.find_elements(By.CLASS_NAME, 'quiz_question')
    for i, question in enumerate(questions):
        # Retrieving question title and MCQ options
        title = question.find_element(By.CLASS_NAME, 'content_plate_inline')
        options = list(map(lambda v: v.text, question.find_elements(By.CLASS_NAME, 'mcq_option_text')))

        # 2 types of question: Pinying or Fill in the word
        if '_' in title.text:
            # Solve fill in the word by searching prefix and suffix in the passage
            prefix, suffix = re.search('(.*?)_+(.*)', title.text).groups()
            prefix = clean(prefix)[-3:]
            suffix = clean(suffix)[:3]
            match = re.search(f'{prefix}(.{{0,4}}){suffix}', passage)
            # Handle error cases
            if match is None:
                logging.error(f'Solving failed on Article {article_id} - Q{i} with data {prefix} | {suffix}')
                answer = random.choice(options)
            else:
                answer = match.group(1).strip()
            logging.debug(f'{prefix} | {suffix} | {answer}')
        else:
            # Solve pinying with pypinyin library
            keyword = title.find_element(By.TAG_NAME, 'u').text
            answer = ' '.join(list(map(lambda v: v[0], pinyin(keyword))))
            # Handle the strange formatting zaobao does for lv
            answer = answer.replace('ǘ', 'u:2').replace('ǚ', 'u:3').replace('ǜ', 'u:4')
            logging.debug(f'{keyword} | {answer}')

        # Find the option number and click the corresponding radio button
        if answer in options:
            choice = options.index(answer)
        elif answer[-len(options[0]):] in options:
            logging.warning(f'Adjusting answer from {answer} to {answer[-len(options[0]):]}')
            choice = options.index(answer[-len(options[0]):])
        else:
            logging.warning(f'Option does not exist; Choosing a random one')
            choice = random.randint(0, 3)
        question.find_element(By.CSS_SELECTOR, f'[value={MCQ_CHOICE[choice]}]').click()

    # Really funny way to get maximum bonus score
    driver.execute_script('$(".cscore").text(1000);')

    # Submit
    try:
        driver.find_element(By.CLASS_NAME, 'btn-submit').click()
        score = int(driver.find_element(By.CLASS_NAME, 'score').find_element(By.TAG_NAME, 'span').text[:-2]) + 100
        logging.info(f'Solved successfully (+{score} points)')
        return score
    except selenium.common.NoSuchElementException:
        # May happen occasionally
        return 0


def main():
    time1 = time.time()
    score_gained = 0
    for _ in range(1):
        CONFIG['lastSolvedArticleID'] += 1
        score_gained += solve_article(CONFIG['lastSolvedArticleID'])
    time2 = time.time()
    print(f'Took {time2 - time1} seconds for {score_gained} score')
    with open('config.json', 'w') as fp:
        json.dump(CONFIG, fp)
    time.sleep(20)
    driver.quit()


if __name__ == '__main__':
    main()
