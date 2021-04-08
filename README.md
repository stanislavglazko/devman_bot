# devman_bot

My bot checks if the teacher has checked your work on https://dvmn.org/ or not. 
When the teacher checks your work, the bot will text you in telegram. 

### How to install
Python3 should be already installed.

1) clone the repo
2) use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
    ```
    pip install -r requirements.txt
    ```
3) you must have devman token, telegram bot token and telegram chat id 
   
4) add .env file in the directory of the tool:
    ```
    DEVMAN_TOKEN=<your_devman_token>
    TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>
    TELEGRAM_CHAT_ID=<your_telegram_chat_id>
    ```
   
### How to use
1) Write: 
    ```
    python3 main.py 
    ```
2) send your work on Devman

3) wait answer in telegram

### How to deploy

1) push the code to your github

2) create an Heroku account

3) create new app on Heroku

4) connect your github to heroku app

5) fill Config Vars in settings of your app 

6) press Deploy Branch in Manual deploy 

7) send you work on Devman

8) wait answer in telegram

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).