import json
import logging
import os
import random
import re
import sys
import threading
import time
import traceback
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup

import requests
from pypinyin import pinyin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Initialize constants
VERSION = '2.0'
MCQ_CHOICE = ('A', 'B', 'C', 'D')
PASSAGE_TEMPLATE_URL = 'https://www.zbschools.sg/stories-{id}'
QUESTION_TEMPLATE_URL = 'https://www.zbschools.sg/cos/o.x?c=/ca7_zbs/zbs&func=quiz&tid=1&rid={id}&litebox=0&popup=1'

os.environ['WDM_LOG'] = '0'  # Silence webdriver log messages
logging.getLogger(requests.packages.urllib3.__package__).setLevel(logging.ERROR)
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Load from configuration file
with open('config.json', 'r') as fp:
    CONFIG = json.load(fp)

logging.info(f'LAST PROCESSED ARTICLE ID: {CONFIG["lastProcessedArticleID"]}')
logging.info(f'ARTICLES PER SESSION: {CONFIG["articlesPerSession"]}')
logging.info(f'THREADS: {CONFIG["threads"]}')
logging.info(f'HEADLESS: {CONFIG["headless"]}')

# Load cookie file
REQUEST_COOKIES = {}
with open('cookies.json', 'r') as fp:
    COOKIES = json.load(fp)
    for cookie in COOKIES:
        cookie["sameSite"] = "None"  # Overrides null value when exported from CookieEditor
        REQUEST_COOKIES[cookie['name']] = cookie['value']  # Setting cookie dict for requests library

# Global Variables
ARTICLES_SOLVED = 0
TOTAL_SCORE_GAINED = 0
CONFIG_LOCK = threading.Lock()
SERVICE = Service(ChromeDriverManager().install())
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging'])

if CONFIG['headless']:
    OPTIONS.add_argument('--headless')


def save_config():
    """
    Utility function to dump CONFIG data into config.json
    :return:
    """
    CONFIG_LOCK.acquire()
    with open('config.json', 'w') as fp:
        json.dump(CONFIG, fp, indent=4)
    CONFIG_LOCK.release()


def suppress_exception():
    """
    Decorator to suppress any error thrown by a function
    :return:
    """

    def decorate(f):
        def applicator(*args, **kwargs):
            # noinspection PyBroadException
            try:
                return f(*args, **kwargs)
            except Exception:
                return

        return applicator

    return decorate


def show_exception_and_exit(exc_type, exc_value, tb):
    """
    Top level exception handler to keep application on an unhandled exception
    :param exc_type: Exception Type
    :param exc_value: Exception Value
    :param tb: Traceback Type
    :return:
    """
    traceback.print_exception(exc_type, exc_value, tb)
    save_config()
    input("Press Enter to quit")
    sys.exit(-1)


# Overriding exception handler
sys.excepthook = show_exception_and_exit


class Driver:
    def __init__(self):
        # Create a new instance of the Chrome driver
        self.driver = webdriver.Chrome(service=SERVICE, options=OPTIONS)

        # Initialize cookies
        # Enables network tracking to use the Network.setCookie method
        self.driver.execute_cdp_cmd('Network.enable', {})

        for cookie in COOKIES:
            self.driver.execute_cdp_cmd('Network.setCookie', cookie)

        # Disable network tracking to not affect performance
        self.driver.execute_cdp_cmd('Network.disable', {})

    def __del__(self):
        self.driver.quit()


threadLocal = threading.local()


def get_driver():
    """
    Function to get the webdriver from the local thread, creating one if it does not exist
    :return:
    """
    driver = getattr(threadLocal, 'driver', None)
    if driver is None:
        driver = Driver()
        setattr(threadLocal, 'driver', driver)
    return driver.driver


def clean(text: str) -> str:
    """
    Utility function to clean a text, stripping away all punctuation and special characters
    to better facilitate regex parsing
    :param text: Text to clean
    :return:
    """
    special = ('\n', '\t', ' ')
    punctuation = ('“', '”', '。', '，', '、', '：', '？', ';', '！', '(', ')', '[', ']', '{', '}', '《', '》', '…', '·', "'", '　', '／', '（', '）', '—')
    for symbol in special + punctuation:
        text = text.replace(symbol, '')
    return text


@suppress_exception()
def accept_available_alert():
    """
    Utility function to accept an alert if available
    :return:
    """
    Alert(get_driver()).accept()


@suppress_exception()
def solve_article(article_id: int):
    """
    Function to process an article, and solve its questions
    :param article_id: ID of the article, i.e. the number after `stories-`
    :return:
    """
    global ARTICLES_SOLVED, TOTAL_SCORE_GAINED
    driver = get_driver()
    logging.debug(f'Processing Article {article_id}')

    # Update last processed article
    if article_id > CONFIG['lastProcessedArticleID']:
        CONFIG['lastProcessedArticleID'] = article_id
        save_config()

    # Scrap article contents and beautiful soup
    page = requests.get(PASSAGE_TEMPLATE_URL.format(id=article_id), cookies=REQUEST_COOKIES)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Removing pinying text
    for py in soup.find_all('span', class_='term_py'):
        py.decompose()

    paragraphs = soup.find_all('span', class_='zbs_sent')

    # Invalid article as there are no paragraphs
    if not paragraphs:
        logging.warning(f'Skipping Invalid Article {article_id}')
        return

    passage = ''.join(list(map(lambda v: v.text, paragraphs)))
    passage = clean(passage)

    driver.get(QUESTION_TEMPLATE_URL.format(id=article_id))
    accept_available_alert()

    # Finding question elements
    questions = driver.find_elements(By.CLASS_NAME, 'quiz_question')
    for i, question in enumerate(questions):
        # Retrieving question title and MCQ options
        title = question.find_element(By.CLASS_NAME, 'content_plate_inline')
        mcq = list(map(lambda v: v.text, question.find_elements(By.CLASS_NAME, 'mcq_option_text')))

        # 2 types of question: Pinying or Fill in the word
        if '_' in title.text:
            # Solve fill in the word by searching prefix and suffix in the passage
            prefix, suffix = re.search('(.*?)_+(.*)', title.text).groups()
            prefix = clean(prefix)[-3:]
            suffix = clean(suffix)[:3]
            length = len(mcq[0])
            match = re.search(f'{prefix}(.{{{length}}}){suffix}', passage)
            # Handle error cases
            if match is None:
                logging.debug(
                    f'Could not locate answer on Article {article_id} - Q{i + 1} with data {prefix} | {suffix}')
                answer = random.choice(mcq)
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
        if answer in mcq:
            choice = mcq.index(answer)
        else:
            logging.debug(f'Option {answer} does not exist; Choosing a random one')
            choice = random.randint(0, 3)
        question.find_element(By.CSS_SELECTOR, f'[value={MCQ_CHOICE[choice]}]').click()

    # Really funny way to get maximum bonus score
    driver.execute_script('$(".cscore").text(1000);')

    # Submit
    driver.find_element(By.CLASS_NAME, 'btn-submit').click()
    score = int(driver.find_element(By.CLASS_NAME, 'score').find_element(By.TAG_NAME, 'span').text[:-2]) + 100
    logging.info(f'Solved Article {article_id} (+{score} points)')
    ARTICLES_SOLVED += 1
    TOTAL_SCORE_GAINED += score


def check_for_updates():
    """
    Helper function to check for new updates
    :return:
    """
    logging.info('Checking for updates...')
    version_url = 'https://raw.githubusercontent.com/TheTrustyPwo/ZBSchools-Macro/master/version.txt'
    latest = requests.get(version_url).text.partition('\n')[0]
    if VERSION == latest:
        logging.info('No new updates found!')
        return
    logging.info(f'Newer version v{latest} found! It is recommended to download it.')


def main():
    global threadLocal
    check_for_updates()

    time1 = time.perf_counter()
    pool = ThreadPool(CONFIG['threads'])
    start_id = CONFIG['lastProcessedArticleID'] + 1
    amount = CONFIG['articlesPerSession']
    pool.map(solve_article, range(start_id, start_id + amount))
    logging.info('Shutting down subprocesses and closing pool...')
    time2 = time.perf_counter()
    del threadLocal
    pool.close()

    print(f'\nPROGRAM FINISHED\n'
          f'{time2 - time1} seconds have elapsed\n'
          f'{ARTICLES_SOLVED} articles have been solved\n'
          f'{TOTAL_SCORE_GAINED} points have been gained\n')

    save_config()
    input('Press Enter to quit')


if __name__ == '__main__':
    main()
