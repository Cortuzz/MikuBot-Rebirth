from bot import Bot

api_data = open("api_data.txt")

group_id = int(api_data.readline())
token = api_data.readline()
debug_mode = False

bot = Bot(group_id, token, debug_mode)

if __name__ == "__main__":
    bot.run()
