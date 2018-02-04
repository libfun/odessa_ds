"""Module for easy telegram reports

Attributes
----------
bot : telepot.Bot
    Instance of bot with key
botid : int
    Dialogue id
response : bot.getUpdates
    Bot responses (unimplemented)
"""
import telepot

bot = telepot.Bot('')
response = bot.getUpdates()
botid = 000


def sendMessage(z):
    """Send message

    Parameters
    ----------
    z : str
        String to send to chat
    """
    try:
        bot.sendMessage(botid, z)
    except Exception as e:
        print('Error sending message', z)


def sendPhoto(f):
    """Send photo

    Parameters
    ----------
    f : file descriptor
        Image file to send
    """
    try:
        bot.sendPhoto(botid, f)
    except Exception as e:
        print('Error sending photo')
