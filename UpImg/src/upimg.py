try:
    import telegram
    from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, Filters
    import telegram.bot
    from os import path
    import os
    import requests
    import imgurpython
    from imgurpython import ImgurClient
    from time import sleep
except ImportError as e:
    print("Error while trying to import the modules: ", e)

#tokens
BOT_TOKEN="5437923941:AAEjLfSAeDLvY6MdYiXqyCtECA4VScYJW7I"
CLIENT_ID="520869c92028d27"
CLIENT_SECRET="57e90ff7aef397a89b803fa26e38caad3b6635e5"

# functions
def debug(text: str) -> None:
    print("Debug: ", text)

def start(update: Updater, context: CallbackContext) -> None:
    user = update.message.from_user
    debug("called the start() from user {}".format(user['username']))
    update.message.reply_text("Welcome to the UpImg Bot. Send an image so i can send the link")

def _help_(update: Updater, context: CallbackContext) -> None:
    user = update.message.from_user
    debug("called help() from user {}".format(user['username']))
    update.message.reply_text("Hey. welcome to the UpImg Bot, below are the list of commands:\n/start\n/help\n")

def send(update: Updater, context: CallbackContext) -> None:
    user = update.message.from_user
    bot=context.bot
    debug("called send() from user {}".format(user['username']))
    file_id=update.message.photo[-1].file_id
    debug("File ID: " + file_id)
    newFile=bot.get_file(file_id)
    file_name="./imgs_temp/file_id_{}.png".format(file_id)
    newFile.download(file_name)

    client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
    res = client.upload_from_path(file_name)
    if res is not None:
        print("Image uploaded!")
        
        update.message.reply_text("Image Uploaded to Imgur Server. Link: {}".format(res['link']))
        debug("Deleting the temporary image file ")
        delete(file_name)
        return

def delete(path) -> None:
    sleep(1)
    os.remove(path)

def init() -> None:
    debug("called main()")
    debug("main: Initializing updater")
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    debug("main: Configuring handlers")
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help_))
    dp.add_handler(MessageHandler(Filters.photo, send))

    debug("main: Starting idle process")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    init()