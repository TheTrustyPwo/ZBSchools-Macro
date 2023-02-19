import re
import io
import sys
import time
import json
import random
import zipfile
import logging
import requests
import traceback
import subprocess
import selenium.common
from tqdm import tqdm
from pypinyin import pinyin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Initialize constants
VERSION = '1.3'
MCQ_CHOICE = ('A', 'B', 'C', 'D')
PASSAGE_TEMPLATE_URL = 'https://www.zbschools.sg/stories-{id}'
QUESTION_TEMPLATE_URL = 'https://www.zbschools.sg/cos/o.x?c=/ca7_zbs/zbs&func=quiz&tid=1&rid={id}&litebox=0&popup=1'

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Load from configuration file
with open('config.json', 'r') as fp:
    CONFIG = json.load(fp)

logging.info(f'LAST SOLVED ARTICLE ID: {CONFIG["lastSolvedArticleID"]}')
logging.info(f'ARTICLES PER SESSION: {CONFIG["articlesPerSession"]}')
logging.info(f'HEADLESS: {CONFIG["headless"]}')


def save_config():
    """
    Utility function to dump CONFIG data into config.json
    :return:
    """
    with open('config.json', 'w') as fp:
        json.dump(CONFIG, fp)


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


# Create a new instance of the Chrome driver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = CONFIG['headless']
driver = webdriver.Chrome(service=service, options=options)

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
                logging.error(f'Could not locate answer on Article {article_id} - Q{i + 1} with data {prefix} | {suffix}')
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


def accept_available_alert():
    """
    Utility function to accept an alert if available
    :return:
    """
    try:
        Alert(driver).accept()
    except selenium.common.NoAlertPresentException:
        pass


def check_for_updates():
    logging.info('Checking for updates...')
    latest = requests.get('https://raw.githubusercontent.com/TheTrustyPwo/ZBSchools-Macro/master/version.txt').text.partition("\n")[0]
    if VERSION == latest:
        logging.info('No new updates found!')
        return

    logging.info(f'Newer version v{latest} found! Downloading from github now...')
    file_name = f'ZBSchools-Macro-v{latest}-Windows-amd64'
    response = requests.get(f'https://github.com/TheTrustyPwo/ZBSchools-Macro/releases/download/v{latest}/{file_name}', stream=True)
    file_size = int(response.headers.get('Content-Length', 0))

    # Create a progress bar with the total file size
    progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True)

    # Open a file stream to save the file
    with open(file_name, 'wb') as f:
        # Iterate over the response content and write it to the file
        for chunk in response.iter_content(chunk_size=1024):
            # Update the progress bar with the current chunk size
            progress_bar.update(len(chunk))
            f.write(chunk)

    # Close the progress bar
    progress_bar.close()

    # Open the downloaded zip file
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        with open("main.exe", "wb") as f:
            f.write(z.read("main.exe"))

    # Exit current instance and run the updated version
    subprocess.Popen("./main.exe")
    sys.exit(0)


def main():
    check_for_updates()

    time1 = time.perf_counter()

    articles_solved = 0
    score_gained = 0
    while articles_solved < CONFIG['articlesPerSession']:
        # Automatically saves config.json every 10 articles
        if CONFIG['lastSolvedArticleID'] % 10 == 0:
            save_config()
        CONFIG['lastSolvedArticleID'] += 1
        # noinspection PyBroadException
        try:
            score = solve_article(CONFIG['lastSolvedArticleID'])
            articles_solved += score > 0
            score_gained += score
        except Exception:
            logging.error(f'Skipping Article {CONFIG["lastSolvedArticleID"]} due to unexpected error')
            # Reloads the page to clear input and closes the Leave Page Confirmation alert
            driver.refresh()
            accept_available_alert()

    time2 = time.perf_counter()

    save_config()
    print(f'\nPROGRAM FINISHED\n{time2 - time1} seconds have elapsed \n{articles_solved} articles have been solved \n{score_gained} points have been gained\n')
    input('Press Enter to quit')

    driver.quit()


if __name__ == '__main__':
    main()
