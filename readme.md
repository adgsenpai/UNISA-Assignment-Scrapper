![download](https://user-images.githubusercontent.com/45560312/220770663-f00a2da4-7ded-4ab1-962c-0a75d6831b59.png)

# UNISA Assignment Scrapper

This is a simple script that scrapes the UNISA website for assignment due dates and generates a calendar to the user with the due dates.

## How it works

We use the link https://stratus.unisa.ac.za/sacdl20/asps/unisa_assignments.asp

Authenticate using selenium and visit that page to scrape the HTML Content. From the HTML content we generate a pandas dataframe from the dataframe encode
a calendar file.

![image](https://user-images.githubusercontent.com/45560312/220772071-1d88ea07-751a-4115-8cef-ee881b16fea7.png)


## Usage

- You have to have python installed

### Install Requirements

```
pip3 install -r requirements.txt
```

For the chrome driver if it gives some error. You need to match it to your broswer you got on your system.

You may visit https://chromedriver.chromium.org/downloads

### Running Scrapper

```
python3 scrape.py
```

Enjoy! Study Hard and Work Hard

