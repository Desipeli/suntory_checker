from suntory_checker import SuntoryChecker
from config import TOKEN_DISCORD
import discord
from discord.ext import commands, tasks
from logger import Logger


URL_LIST = "https://reserve.suntory.co.jp/regist/switch/00051c0001CJe69uI7/courseList?wr=suntory_factory&p=yamazaki_02&k=10601749735d537e6d01474266124076005616670a1540651915275d0410650710476347142002061260001116604247710701176c0a1b423410162456071861041a1568174171533d1761071047324748"
URL = "https://reserve.suntory.co.jp/regist/is?SMPFORM=ngoe-lenetb-550fe19094a7fbbfd41c49a7ce9cc871&courseNo=00422&eventDate="

EVENT_DATES = ["2023年1月15日", "2023年1月16日", "2023年1月17日",
               "2023年1月18日", "2023年1月19日", "2023年1月20日"]


class Bot:
    def __init__(self, logger: "Logger", suntory: "SuntoryChecker") -> None:
        self.logger = logger
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        self.alerting = []
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.suntory = suntory
        self.checking = True

    def run(self):

        @tasks.loop(seconds=30)
        async def printer():
            if not self.checking:
                return

            result = self.suntory.check_tour()
            if result:
                for channel_id in self.alerting:
                    channel = self.bot.get_channel(channel_id)
                    await channel.send(f"@everyone Book Now: {URL}")
                self.checking = False

        @self.bot.event
        async def on_ready():
            self.logger.log("Bot running")
            printer.start()

        @self.bot.command(name="rc")
        async def rc(ctx):
            if not self.checking:
                self.checking = True
                await ctx.channel.send(f"Checking again")
            else:
                await ctx.channel.send(f"Already checking")

        @self.bot.command(name="ref")
        async def ref(ctx):
            result = self.suntory.check_tour()
            if result:
                await ctx.channel.send(f"Book Now! {URL}")
            else:
                await ctx.channel.send("Can't book :(")

        @self.bot.command(name="alert")
        async def alert_me(ctx):
            if ctx.channel.id not in self.alerting:
                self.alerting.append(ctx.channel.id)
                self.logger.log(f"alerting channel {ctx.channel.id}")
                await ctx.channel.send("Alerting this channel")
            else:
                await ctx.channel.send("Already alerting this channel")

        @self.bot.command(name="getdates")
        async def get_dates(ctx):
            try:
                dates = self.suntory.get_dates()
                await ctx.channel.send({str(dates)})
            except Exception as error:
                self.logger.error(error)

        @self.bot.command(name="seteventdates")
        async def set_dates(ctx):
            try:
                msg = ctx.message.content[14:]
                dates_list = msg.strip().split(" ")
                await ctx.channel.send("new dates set. Check with getdates")
            except Exception as error:
                self.logger.error(error)
                await ctx.channel.send("Something went wrong. Check that dates are correctly set and separated by 1 whitespace. example: 2023年1月15日 2023年1月16日")

        self.bot.run(TOKEN_DISCORD)


if __name__ == "__main__":
    logger = Logger()
    suntory = SuntoryChecker(logger, EVENT_DATES.copy(), URL_LIST, URL)
    bot = Bot(logger, suntory)
    bot.run()