# %%
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
 
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome(
    executable_path='./chromedriver_win32/chromedriver.exe',options=options)

browser.get('https://stratus.unisa.ac.za/sacdl20/asps/unisa_assignments.asp')

studentNumber = browser.find_element(By.NAME, 'StudNo')
studentNumber.send_keys('REDACTED')

studentPassword = browser.find_element(By.NAME, 'password')
studentPassword.send_keys('REDACTED')

submit = browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
submit.click()

# then redirect to https://stratus.unisa.ac.za/sacdl20/asps/stuasstab.asp?system=SOL
# wait for the page to load
redirectURL = 'https://stratus.unisa.ac.za/sacdl20/asps/stuasstab.asp?system=SOL'

browser.get(redirectURL)

# get the html of the page
html = browser.page_source

browser.quit()

# %%
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')

# find the table
table = soup.find('table')

# %%
textBuffer = ''
for row in table.find_all('tr'):
    for cell in row.find_all('td'):    
        # print if the cell has text
        if cell.text and cell.text != ' ':
            textBuffer += (cell.text  + ' ').replace('\xa0', '')

textBuffer                

# %%
data = []
rows = textBuffer.split('        ')
for row in rows:
    if len(row.split('      ')) > 1:
        data.append(row.split('      ')[0])
        data.append(row.split('      ')[1])
    else:
        data.append(row)
import pandas as pd
df = pd.DataFrame(columns=['Course', 'Term', 'Number', 'Type', 'Status', 'ID', 'Date'])
# iterate over the data and add to the dataframe
subject = ''
term = ''

for row in data:
    try:
        # if first character is a digit
        firstChar = row.split(' ')[0]
        if firstChar[0].isdigit():
            # parse 2 assignment Closed 547562 2023-06-15
            df = df.append({
                'Course': subject,
                'Term': term,
                'Number': row.split(' ')[0],
                'Type': row.split(' ')[1],
                'Status': row.split(' ')[2],
                'ID': row.split(' ')[3],
                'Date': row.split(' ')[4]
            }, ignore_index=True)
            
        else:
            # parse APM2611 2023/0 1 assignment Closed 547463 2023-05-24
            subject = row.split(' ')[0]
            term = row.split(' ')[1]
            df = df.append({
                'Course': row.split(' ')[0],
                'Term': row.split(' ')[1],
                'Number': row.split(' ')[2],
                'Type': row.split(' ')[3],
                'Status': row.split(' ')[4],
                'ID': row.split(' ')[5],
                'Date': row.split(' ')[6]
            }, ignore_index=True)
    except:
        pass

# %%
# sort the dates in ascending order
df = df.sort_values(by=['Date'], ascending=True)
df

# %%
# save all the data to a email calendar format
with open('calendar.ics', 'w') as f:
    f.write('BEGIN:VCALENDAR\n')
    f.write('VERSION:2.0\n')
    f.write('PRODID:-//hacksw/handcal//NONSGML v1.0//EN\n')
    f.write('CALSCALE:GREGORIAN\n')
    f.write('METHOD:PUBLISH\n')
    f.write('X-WR-CALNAME:Unisa Assignments\n')
    f.write('X-WR-TIMEZONE:Europe/Johannesburg\n')
    f.write('X-WR-CALDESC:Unisa Assignments\n')
    f.write('BEGIN:VTIMEZONE\n')
    f.write('TZID:Europe/Johannesburg\n')
    f.write('X-LIC-LOCATION:Europe/Johannesburg\n')
    f.write('BEGIN:STANDARD\n')
    f.write('TZOFFSETFROM:+0200\n')
    f.write('TZOFFSETTO:+0200\n')
    f.write('TZNAME:SAST\n')
    f.write('DTSTART:19700101T000000\n')
    f.write('END:STANDARD\n')
    f.write('END:VTIMEZONE\n')
    for index, row in df.iterrows():
        f.write('BEGIN:VEVENT\n')
        f.write('UID:unisa-assignment-' + row['ID'] + '\n')
        f.write('DTSTAMP:20200315T000000Z\n')
        f.write('DTSTART;TZID=Europe/Johannesburg:' + row['Date'].replace('-', '') + 'T000000\n')
        f.write('DTEND;TZID=Europe/Johannesburg:' + row['Date'].replace('-', '') + 'T000000\n')
        f.write('SUMMARY:' + row['Course'] + ' - ' + row['Type'] + ' - ' + row['Status'] + '\n')
        f.write('DESCRIPTION:' + row['Course'] + ' - ' + row['Type'] + ' - ' + row['Status'] + '\n')
        f.write('END:VEVENT\n')
    f.write('END:VCALENDAR\n')

# save the dataframe to a csv file
df.to_csv('unisa_assignments.csv', index=False)


