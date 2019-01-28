import time
import random
import requests
import sys

from bs4 import BeautifulSoup
from collections import Counter
from statistics import mode


def get_soup():
    # start_time = time.time()
    # URL for powerball history
    url = "https://wilottery.com/lottogames/powerballAllhistory.aspx"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # print('Get soup takes %s to run' % (time.time() - start_time))
    return soup


def powerball_choices(*args, soup):
    # start_time = time.time()    
    main_table = soup.find(id="ctl00_ContentPlaceHolder1_GridView1")
    table_rows = main_table.find_all('tr')
    table_rows = table_rows[1:]
    lotto_history = []
    power_balls = []
    for table_row in table_rows:
        table_cells = table_row.find_all('td')
        table_cell_list = [cell.get_text() for cell in table_cells]
        updated_list = table_cell_list[1:]
        updated_list = updated_list[:len(updated_list)-2]
        # updated_list is a list of the 6 winning digits - last dig is PB
        lotto_history.append(updated_list)
    # Creates a list of all powerballs drawn and gets 10 most common
    power_ball_list = []
    [power_ball_list.append(inner_list[-1]) for inner_list in lotto_history]
    pb_counts = Counter(power_ball_list)
    most_common_pb = [k for k,v in pb_counts.most_common(10)]
    # Creates a list of all white numbers drawn and gets 15 most common    
    all_number_list = []
    [[all_number_list.append(x) for x in inner_list[0:5]] \
        for inner_list in lotto_history]
    counts = Counter(all_number_list)
    most_common = [k for k,v in counts.most_common(15)]
    winning_list = check_winning_lists(
        lotto_history, 
        most_common, 
        most_common_pb
        )
    # print('Getting our lists takes %s to run' % (time.time() - start_time))        
    return winning_list


def check_winning_lists(lotto_history, most_common, most_common_pb):
    # start_time = time.time()  
    winning_list = []
    i = 0
    while i < 5:
        random_common_number = random.choice(most_common)
        while random_common_number in winning_list:
            random_common_number = random.choice(most_common)
        winning_list.append(random_common_number)
        i += 1
    random_pb_number = random.choice(most_common_pb)
    if 'no-match' in sys.argv:
        while random_pb_number in winning_list:
            random_pb_number=random.choice(most_common_pb)
        winning_list.append(random_pb_number)
    else:
        winning_list.append(random_pb_number)
    for item in lotto_history:
        if item == winning_list:
            check_winning_lists(most_common, most_common_pb)
    # print('Picking winners takes %s to run' % (time.time() - start_time))
    return winning_list   


def generate_winners(*args):
    soup = get_soup()
    print('Generating a combination with all high percentage numbers...')
    print(powerball_choices(*args, soup=soup))


if __name__ == "__main__":
    working = True
    while working == True:
        generate_winners(sys.argv)
        working = False