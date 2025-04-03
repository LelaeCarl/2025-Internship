'''
12 - BS4 Module - Double Color Ball Data Statistics and Analysis
https://datachart.500.com/ssq/?expect=100
Requirements:
    1. Scrape 100 periods of data from the lottery website
    2. Store data as: Period number, Red balls - 6, Blue ball - 1
    3. Perform analysis on the stored data
        3.1 Find the most frequent red balls in 100 periods and sort them
        3.2 Find the most frequent blue balls in 100 periods and sort them
        3.3 Randomly assign the top 10 red and blue balls
        3.4 Final result:
            5 sets of lottery numbers
            3,8,10,18,22,31    6
            3,8,10,18,22,31    6
            3,8,10,18,22,31    6
            3,8,10,18,22,31    6
            3,8,10,18,22,31    6
    Notes:
        1. Decode format: gb2312
        2. Sorting and storing of data
            2.1 Store red balls as a 2D list
            2.2 Sort the list
'''

import requests
from bs4 import BeautifulSoup
import random
from collections import Counter


def fetch_lottery_data():
    """Scrape 100 periods of data from the lottery website"""
    url = "https://datachart.500.com/ssq/?expect=100"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'gb2312'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the data table
        table = soup.find('tbody', id='tdata')
        if not table:
            print("Data table not found")
            return None

        trs = table.find_all('tr')
        if not trs:
            print("No data rows found in the table")
            return None

        data = []
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) < 16:  # Ensure enough data columns
                continue

            # Extract the period number
            issue = tds[0].get_text().strip()

            # Extract red balls (6)
            red_balls = [td.get_text().strip() for td in tds[1:7]]

            # Extract blue ball (1)
            blue_ball = tds[7].get_text().strip()

            data.append({
                'issue': issue,
                'red_balls': red_balls,
                'blue_ball': blue_ball
            })

        return data

    except Exception as e:
        print(f"Error scraping data: {e}")
        return None


def analyze_data(data):
    """Analyze the data and return statistical results"""
    if not data:
        return None

    # Count the frequency of red balls
    red_counter = Counter()
    for item in data:
        red_counter.update(item['red_balls'])

    # Count the frequency of blue balls
    blue_counter = Counter()
    for item in data:
        blue_counter.update([item['blue_ball']])

    # Get top 10 red balls
    red_top10 = [ball for ball, count in red_counter.most_common(10)]

    #
