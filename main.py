from os import environ
from logging import Formatter, basicConfig, getLogger, INFO
from telethon import TelegramClient
from telethon.sessions import StringSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from mymodule import customTime

# ~ API things
# Use your own values from my.telegram.org
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']

# https://docs.telethon.dev/en/latest/concepts/sessions.html#string-sessions
STRING_SESSION = environ['STRING_SESSION']

# ~ My things
# Receiver information
USERNAME_RECEIVER = environ['USERNAME_RECEIVER']  # without @, "username"
# use https://t.me/userinfobot to know the id or read telethon doc
ID_RECEIVER = int(environ['ID_RECEIVER'])

# Enable logging
basicConfig(
    # filename='log.txt', filemode='w',
    datefmt="%Y-%m-%d %H:%M:%S",  level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
LOGGER = getLogger(__name__)
Formatter.converter = customTime
LOGGER.info('Log aktif, Hello Sir.')


# ~ START HERE
async def main():
    LOGGER.info('Try get user')
    get_receiver = False
    get_receiver_by = ''
    await client.get_dialogs()
    try:
        receiver = await client.get_input_entity(USERNAME_RECEIVER)
        get_receiver = True
        get_receiver_by = 'username'
    except ValueError as e:
        LOGGER.warning(f'{e}. I am going to try get user with their id')

    if not get_receiver:
        try:
            receiver = await client.get_input_entity(ID_RECEIVER)
            get_receiver = True
            get_receiver_by = 'id'
        except ValueError as e:
            LOGGER.warning(e)

    if get_receiver:
        LOGGER.info(
            f'Sir, I got user by using {get_receiver_by}, let\'s do this')
        await dosomething(receiver)
    else:
        LOGGER.error(
            f'Sorry Sir, I can not get any user with "{USERNAME_RECEIVER}" as their '
            f'username neither "{ID_RECEIVER}" as their id.'
        )


async def dosomething(receiver):
    # send message
    await client.send_message(receiver, 'Hello there, good morning.')
    # # send audio
    # await client.send_file(receiver, 'assets/audio/file_example_MP3.mp3')
    # # send document
    # await client.send_file(receiver, 'assets/document/file_example_PPT.ppt')
    # await client.send_file(receiver, 'assets/document/file_example_XLS.xls')
    # await client.send_file(receiver, 'assets/document/file-example_PDF.pdf')
    # await client.send_file(receiver, 'assets/document/file-sample_DOC.doc')
    # # send photo
    # await client.send_file(receiver, 'assets/photo/file_example_JPG.jpg')
    # # send video
    # await client.send_file(receiver, 'assets/video/file_example_MP4.mp4')


client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
LOGGER.info('Start client')
client.start()
scheduler = AsyncIOScheduler(timezone='Asia/Makassar', event_loop=client.loop)
LOGGER.info('Add scheduler')
scheduler.add_job(
    main,

    # read https://apscheduler.readthedocs.io/en/stable/ for detail on how to
    # schedule your task

    # TL;DR
    # cron, do task when ....
    trigger='cron',
    hour='05',
    minute='00',
    # second='15',

    # # interval, do task with interval ....
    # trigger='interval',
    # minutes=5,

    # run task right now when program run for the first time
    # next_run_time=datetime.now()
)
LOGGER.info('Start scheduler')
scheduler.start()
LOGGER.info('Run client until disconnected')
client.run_until_disconnected()
LOGGER.info('Stop client, good luck Sir!')
