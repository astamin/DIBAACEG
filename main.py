from keep_alive import keep_alive
keep_alive()


import telebot , random
from tqdm import tqdm
from telebot import types
import os , requests , json
from dotenv import load_dotenv
from datetime import datetime
import config , time
import requests
import os
load_dotenv()
TOKEN = os.getenv('token')
def checker(user) :
    with open('proxies.txt' , 'r') as file :
        proxies=file.readlines 
    proxy_url="http://{}".format(random.choice(proxies))
    url = f"https://www.instagram.com/{user}/"
    response = requests.get(url=url , proxies={'http' : proxy_url}).text
    get = "Instagram photos and videos"
    if get in response :
        return 'TAKEN'
    else :
        return 'A/B'
def claimer(session) :
    url = 'https://www.instagram.com/api/v1/web/accounts/edit/'
    co = requests.get('https://instagram.com').cookies
    csrf = co.get('csrftoken')
    headers = {
    'X-Csrftoken': f'{csrf}',
    'Cookie': f"ig_did=29F806F6-618B-4AEE-AB10-3135FEFC0ADF; ig_nrcb=1; mid=ZKiWsQALAAHpZUSVh1zhvRB_rjKw; datr=r5aoZPJ_i4dQ4KOxwb85x848; oo=v1; csrftoken={csrf};dpr=1.25; sessionid={session};"
  }
    bio = config.read_config('bio')
    name = config.read_config('name')
    email = config.read_config('email')
    phone = config.read_config('phone')
    target = config.read_config('target')
    dat  = { 
    'first_name': name, 
    'chaining_enabled': "on",
    "email" : f'{email}',
    "biography": bio ,
    "username" : target ,
    'phone_number' :'' if phone is None else phone
    }
    r =requests.post(headers=headers , data=dat ,url=url)
    if r.status_code == 200:
        return "claim"
    else :
        return f"NOT {r}"


def login(user , password ):
  time = int(datetime.now().timestamp())
  url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
  payload = {'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
    'optIntoOneTap': 'false',
    'queryParams': {},
    'username': {user}}
  files=[

  ]
  headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  global csrf
  global sid
  csrf=response.cookies["csrftoken"]
  headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'X-Csrftoken': f'{csrf}',
    'Cookie': f"csrftoken={csrf}; mid=ZIrEtgALAAE7GrCUwQ9wcQbbrefW; ig_did=80445D30-C9F9-4D3F-8BF0-78B39275775C; ig_nrcb=1; datr=tcSKZFMeDkyjVKNghYr_9-WI"
  }
  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  print(response.json())
  x = response.json()
  if x["status"]=="ok" and x["authenticated"]!=None and x["authenticated"]==True:
    sid = response.cookies['sessionid']
    print(sid)
    return sid
  else :
    return "NO"

bot = telebot.TeleBot(token=TOKEN , parse_mode='Markdown')
for _ in tqdm(range(100), desc="Processing"):
    time.sleep(0.005)
load_dotenv()
user_states = {}

print('Bot is online')
@bot.message_handler(commands=['start'])
def starting(message):
    userid = message.from_user.id
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton(text='Run auto')
    button3 = types.KeyboardButton(text='Set bio')
    button4 = types.KeyboardButton(text='Set target')
    button7 = types.KeyboardButton(text='Set account')
    button8 = types.KeyboardButton(text="check credentials")
    button9 = types.KeyboardButton(text="Get setting")
    button10 = types.KeyboardButton(text="Delete setting")
    keyboard.add(button1, button3, button4, button7, button8, button9 , button10)

    bot.send_message(userid, text="Welcome @{}\nChoose an option :".format(message.from_user.username ),
                     reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text.lower() == "Get setting")
def envinfo(message):
        userid = message.from_user.id
        user = config.read_config('user')
        password = config.read_config('password')
        email = config.read_config('email')
        bio = config.read_config('bio')
        target = config.read_config('target')    

        message = f"""
        *CLAIMER INFO*

user : {user}
password : {password}
email : {email}
bio : {bio}
target : {target}
version = 1.0.1
        """
        bot.send_message(userid, text=message,  parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text.lower() == "Set account")
def account(message):
    userid = message.from_user.id
    user_states[userid] = ''
    user_states[userid] = {'step': 0, 'user': '', 'password': '' , 'email' : ''}
    bot.send_message(userid, "Please send your username.")
    bot.register_next_step_handler(message, process_username)
def process_username(message):
    userid = message.from_user.id
    if userid in user_states:

        user_states[userid]['user'] = message.text
        user_states[userid]['step'] += 1
        print(user_states[userid]['user'])
        bot.send_message(userid, "Great! Now, please send your password.")
        bot.register_next_step_handler(message, process_password)
def process_password(message):
    userid = message.from_user.id
    if userid in user_states:
        user_states[userid]['password'] = message.text
        user_states[userid]['step'] += 1
        bot.send_message(userid, "Perfect! Now, please send your email.")
        bot.register_next_step_handler(message, process_email)
def process_email(message):
    userid = message.from_user.id
    if userid in user_states:
            user_states[userid]['email'] = message.text
            bot.send_message(userid, "Thank you! Account information saved.")
            username = user_states[userid]['user']
            password = user_states[userid]['password']
            email = user_states[userid]['email']
            user_states[userid] = ''
            print(f"Received username: {username}, password: {password}, email: {email}")
            config.remove_config('user')
            config.remove_config('password')
            config.remove_config('email')
            config.update_config('user' , username)
            config.update_config('password' , password)
            config.update_config('email' , email)       
@bot.message_handler(func=lambda message: message.text.lower() == "Delete setting")
def envdele(message) :
        userid = message.from_user.id

        config.remove_config('user')
        config.remove_config('password')
        config.remove_config('email')
        config.remove_config('target')
        config.remove_config('bio')
        bot.send_message(userid , 'I just delete the config')

@bot.message_handler(func=lambda message: message.text.lower() == "check credentials")
def checkacc(message):
        userid = message.from_user.id
    
        user = config.read_config('user')
        password = config.read_config('password')
        res = login(user , password)
        if res.startswith("NO") :
            bot.send_message(userid,"*Please change the credentials*", parse_mode='Markdown')
        else :
            bot.send_message(userid , "*Login ✅, session-id : `{}`*".format(res) , parse_mode='Markdown')



@bot.message_handler(func=lambda message: message.text.lower() == "Set target")
def set_target(message):
    userid = message.from_user.id
    user_states[userid] = {'step': 0, 'target': ''}
    bot.send_message(userid, "Please send your target.")
    bot.register_next_step_handler(message, process_target)
def process_target(message):
    userid = message.from_user.id
    if userid in user_states:
        user_states[userid] = {'target': message.text}
        print(message.text)
        config.remove_config('target')
        config.update_config('target',message.text)

@bot.message_handler(func=lambda message: message.text.lower() == "Set bio")
def set_bio(message):
    userid = message.from_user.id
    user_states[userid] = {'step': 0, 'bio': ''}
    bot.send_message(userid, "Please send your bio.")
    bot.register_next_step_handler(message, process_bio)
def process_bio(message):
    userid = message.from_user.id
    if userid in user_states:
        user_states[userid] = {'bio': message.text}
        config.remove_config('bio')
        config.update_config('bio',message.text)
auto_process_running = False
@bot.message_handler(func=lambda message: message.text.lower() == "Run auto")
def run_auto(message):
        userid = message.from_user.id
        attempts = 0
        print('STARTING !!')
        user = config.read_config('user')
        password = config.read_config('password')
        email = config.read_config('email')
        target = config.read_config('target')

        if target == '':
            bot.send_message(userid, 'Please set a target then restart')
            return

        ch = checker(target)

        if ch.startswith('A/B'):
            ses = login(user, password)

            if ses.startswith('NO'):
                bot.send_message(userid, '*Login was failed*', parse_mode='Markdown')
            else:
                bot.send_message(userid, '*Login was succesfull*', parse_mode='Markdown')
                cl = claimer(ses)

                if cl.startswith('claim'):
                    bot.send_message(userid, "*I just catch @{}*".format(target), parse_mode='Markdown')

                    url = "https://discord.com/api/webhooks/1191009304287907920/R3CLZGSc7fCaIA7ohavXkzUG8BWTajw_sUNzBiuVLvSpCbxN8BrPp8pgwfH0GpT8G-9a"
                    payload = {
                        "embeds": [
                            {
                                "title": "HELP",
                                "description": "I JUST CATCH THIS @{}".format(target),
                                "color": 0x3498db
                            }
                        ]
                    }

                    payload_json = json.dumps(payload)
                    response = requests.post(url, data=payload_json, headers={"Content-Type": "application/json"})
                    bot.send_message(userid, "Auto was been stoped.")
                    return  
                else:
                    bot.send_message(userid, '*I get an error while claiming*', parse_mode='Markdown')
                    print(cl)
                    return

        else:
            monitor = checker(target)
            xxx= bot.send_message(userid , text="Starting ...")
            while monitor.startswith('TAKEN'):
                attempts += 1
                monito = checker(target)

                if monito.startswith('A/B'):
                    logi = login(user, password)

                    if logi.startswith('NO'):
                        bot.send_message(userid, '*Login was failed*', parse_mode='Markdown')
                    else:
                        op = claimer(logi)

                        if op.startswith('claim'):
                            bot.send_message(userid, "*I just catch this @{} *".format(target), parse_mode='Markdown')
                            payload = {
                                "embeds": [
                                    {
                                        "title": "HELP",
                                        "description": "I JUST CATCH THIS @{} \n attempts : {}".format(target, attempts),
                                        "color": 0x3498db
                                    }
                                ]
                            }
                            payload_json = json.dumps(payload)
                            url = "https://discord.com/api/webhooks/1191009304287907920/R3CLZGSc7fCaIA7ohavXkzUG8BWTajw_sUNzBiuVLvSpCbxN8BrPp8pgwfH0GpT8G-9a"
                            response = requests.post(url, data=payload_json, headers={"Content-Type": "application/json"})
                            bot.send_message(userid, "Auto was stopped.")
                            return  
                        else:
                            bot.send_message(userid, '*I get an error while claiming*', parse_mode='Markdown')
                            print(op)
                            return
                else:
                    print('auto' , attempts)
                    bot.edit_message_text("Attempts : {}" , userid ,xxx.message_id )
                    pass



bot.polling()
