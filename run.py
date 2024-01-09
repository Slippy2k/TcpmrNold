# -*- coding: utf-8 -*-

import logging
from colorama import Fore
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Chat import ChatPresence
from TwitchChannelPointsMiner.classes.Discord import Discord
from TwitchChannelPointsMiner.classes.Telegram import Telegram
from TwitchChannelPointsMiner.classes.Matrix import Matrix
from TwitchChannelPointsMiner.classes.Pushover import Pushover
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import Strategy, BetSettings, Condition, OutcomeKeys, FilterCondition, DelayMode
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer, StreamerSettings
from keep_alive import keep_alive
import os

keep_alive()

twitch_miner = TwitchChannelPointsMiner(
    username=os.environ.get('username'),
    password=os.environ.get('password'),           # If no password will be provided, the script will ask interactively
    claim_drops_startup=False,                  # If you want to auto claim all drops from Twitch inventory on the startup
    priority=[                                  # Custom priority in this case for example:
        Priority.STREAK,                        # - We want first of all to catch all watch streak from all streamers
        Priority.DROPS,                         # - When we don't have anymore watch streak to catch, wait until all drops are collected over the streamers
        Priority.ORDER                          # - When we have all of the drops claimed and no watch-streak available, use the order priority (POINTS_ASCENDING, POINTS_DESCEDING)
    ],
    enable_analytics=False,                     # Disables Analytics if False. Disabling it significantly reduces memory consumption
    disable_ssl_cert_verification=False,        # Set to True at your own risk and only to fix SSL: CERTIFICATE_VERIFY_FAILED error
    disable_at_in_nickname=False,               # Set to True if you want to check for your nickname mentions in the chat even without @ sign
    logger_settings=LoggerSettings(
        save=False,                              # If you want to save logs in a file (suggested)
        console_level=logging.INFO,             # Level of logs - use logging.DEBUG for more info
        console_username=False,                 # Adds a username to every console log line if True. Also adds it to Telegram, Discord, etc. Useful when you have several accounts
        auto_clear=True,                        # Create a file rotation handler with interval = 1D and backupCount = 7 if True (default)
        time_zone="",                           # Set a specific time zone for console and file loggers. Use tz database names. Example: "America/Denver"
        file_level=logging.DEBUG,               # Level of logs - If you think the log file it's too big, use logging.INFO
        emoji=True,                             # On Windows, we have a problem printing emoji. Set to false if you have a problem
        less=False,                             # If you think that the logs are too verbose, set this to True
        colored=True,                           # If you want to print colored text
        color_palette=ColorPalette(             # You can also create a custom palette color (for the common message).
            STREAMER_online="GREEN",            # Don't worry about lower/upper case. The script will parse all the values.
            streamer_offline="red",             # Read more in README.md
            BET_wiN=Fore.MAGENTA                # Color allowed are: [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET].
        ),
        telegram=Telegram(                                                          # You can omit or set to None if you don't want to receive updates on Telegram
            chat_id=123456789,                                                      # Chat ID to send messages @getmyid_bot
            token="123456789:shfuihreuifheuifhiu34578347",                          # Telegram API token @BotFather
            events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE,
                    Events.BET_LOSE, Events.CHAT_MENTION],                          # Only these events will be sent to the chat
            disable_notification=True,                                              # Revoke the notification (sound/vibration)
        ),
        discord=Discord(
            webhook_api="https://discord.com/api/webhooks/0123456789/0a1B2c3D4e5F6g7H8i9J",  # Discord Webhook URL
            events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE,
                    Events.BET_LOSE, Events.CHAT_MENTION],                                  # Only these events will be sent to the chat
        ),
    ),
    streamer_settings=StreamerSettings(
        make_predictions=True,                  # If you want to Bet / Make prediction
        follow_raid=True,                      # Follow raid to obtain more points
        claim_drops=True,                       # We can't filter rewards base on stream. Set to False for skip viewing counter increase and you will never obtain a drop reward from this script. Issue #21
        claim_moments=True,                     # If set to True, https://help.twitch.tv/s/article/moments will be claimed when available
        watch_streak=True,                      # If a streamer go online change the priority of streamers array and catch the watch screak. Issue #11
        chat=ChatPresence.NEVER,               # Join irc chat to increase watch-time [ALWAYS, NEVER, ONLINE, OFFLINE]
        bet=BetSettings(
            strategy=Strategy.SMART,            # Choose you strategy!
            percentage=5,                       # Place the x% of your channel points
            percentage_gap=20,                  # Gap difference between outcomesA and outcomesB (for SMART strategy)
            max_points=50000,                   # If the x percentage of your channel points is gt bet_max_points set this value
            stealth_mode=True,                  # If the calculated amount of channel points is GT the highest bet, place the highest value minus 1-2 points Issue #33
            delay_mode=DelayMode.FROM_END,      # When placing a bet, we will wait until `delay` seconds before the end of the timer
            delay=6,
            minimum_points=20000,               # Place the bet only if we have at least 20k points. Issue #113
            filter_condition=FilterCondition(
                by=OutcomeKeys.TOTAL_USERS,     # Where apply the filter. Allowed [PERCENTAGE_USERS, ODDS_PERCENTAGE, ODDS, TOP_POINTS, TOTAL_USERS, TOTAL_POINTS]
                where=Condition.LTE,            # 'by' must be [GT, LT, GTE, LTE] than value
                value=800
            )
        )
    )
)

# You can customize the settings for each streamer. If not settings were provided, the script would use the streamer_settings from TwitchChannelPointsMiner.
# If no streamer_settings are provided in TwitchChannelPointsMiner the script will use default settings.
# The streamers array can be a String -> username or Streamer instance.

# The settings priority are: settings in mine function, settings in TwitchChannelPointsMiner instance, default settings.
# For example, if in the mine function you don't provide any value for 'make_prediction' but you have set it on TwitchChannelPointsMiner instance, the script will take the value from here.
# If you haven't set any value even in the instance the default one will be used

#twitch_miner.analytics(host="127.0.0.1", port=5000, refresh=5, days_ago=7)   # Start the Analytics web-server

twitch_miner.mine(
    [
      Streamer("easportsfc"),
# Rainbow 6
        Streamer("ubisoft"),
        Streamer("rainbow6"),
        Streamer("rainbow6de"),
        Streamer("rainbow6jp"),
        Streamer("rainbow6kr"),
        Streamer("rainbow6bravo"),
        Streamer("rainbow6br"),
#        Streamer(""varsitygaming"),
#        Streamer(""maciejay"),
# Rainbow 6 END

# Call of Duty
        Streamer("callofduty"),
# Call of Duty END

# Rocketleague
      Streamer("RocketLeague"),
      Streamer("rocketstreetlive"),
      Streamer("firstkiller"),
      Streamer("unirocketeers"),
      #Streamer("jamaicancoconut"),
      #Streamer("garrettg"),
      #Streamer("rizzo"),
# Rocketleague END

# Halo
       Streamer("LVTHalo"),
       Streamer("europeanhalo"),
       Streamer("twitchgaming"),
       Streamer("Halo"),
       Streamer("HCS"),
       Streamer("hcs_red"),
       Streamer("hcs_blue"),
       Streamer("reallifespartan"),
      Streamer("atlasgg1"),
      Streamer("stresss"),
      #Streamer("reclximer"),
      #Streamer("rangercali"),
      #Streamer("europahalo"),
      #Streamer("nmsggoficial"),
      #Streamer("rangercali"),
      #Streamer("complexity"),
      #Streamer("luciid_tw"),
      #Streamer("eli_x"),
      #Streamer("elamite"),
      #Streamer("hunter_jjx"),
#Halo END

# Call of Duty
      #Streamer("symfuhny"),
      #Streamer("aydan"),
      #Streamer("mrbluwu"),
      #Streamer("riskin"),
      #Streamer("iddqd"),
# Call of Duty END
      # VARIO
       Streamer("m0ann"),
       Streamer("britva_games"),
       Streamer("trisarahtops91"),
      #Streamer("jambo"),
      #Streamer("lyric"),
      #Streamer("mixwell"),
      #Streamer("noko"),
      #Streamer("gigz"),
      # VARIO
# overwatchcontenders
      Streamer("playoverwatch"),
      Streamer("ml7support"),
      Streamer("emongg"),
      Streamer("nektagg"),
      Streamer("overwatchcontenders"),
      Streamer("playoverwatchjp"),
      Streamer("overwatchesportskr"),
      # Streamer("evalangwin"),
      # Streamer("august"),
      # Streamer("iddqd"),
# overwatchcontenders ENDE

# VARIO
       Streamer("beardageddon"),
      #Streamer("streamerhouse"),
      Streamer("drooooooooooopy"),
      #Streamer("edi4ttv"),
      #Streamer("neevee_o7"),
      #Streamer("movementbuff"),
     Streamer("paydaythegame"),
        Streamer("forhonorgame"),
      #Streamer("evalangwin"),
      #Streamer("somnus"),
      #Streamer("iddqd"),
      # Streamer("reneesky"),
      # Streamer("copeylius"),
      # Streamer("2dkiri"),
       Streamer("gothicsnowangel"),
      #Streamer("lopes_gaming"),
      # Streamer("laranity"),
      # Streamer("schneeschnuffelhase"),
      # Streamer("anniefuchsia"),
      #Streamer("pubg_battlegrounds"),
      # Streamer("pubgthailandofficial"),
      # Streamer("pubg_br"),
      # Streamer("ovidiuz94"),
      # Streamer("mdee14"),
      # Streamer("pepp3rpotts"),
      # Streamer("daijoburu"),
      # Streamer("neevee_o7"),
      # Streamer("rifas"),
      # Streamer("introjuegos"),
      # Streamer("zara"),
      # Streamer("pirolino1966"),
      # Streamer("scorpio"),
      # Streamer("simuverserden"),
# VARIO END

# The Elder Scrolls Online
        Streamer("bethesda_de"),
        Streamer("bethesda_nl"),
        Streamer("bethesda"),
      #Streamer("backyardis"),
# The Elder Scrolls Online ENDE

# NUR Punkten   
        Streamer("hitsquadgodfather"),
        Streamer("lenovolegion"),
        Streamer("redrewards"),
        Streamer("alienware"),
        Streamer("xboxon"),
        Streamer("cohhcarnage"),
        Streamer("tygerladi"),
        Streamer("staggerrilla"),
        Streamer("nuclearqueso"),
        Streamer("homiedrew")
# NUR Punkten END

    ],                                  # Array of streamers (order = priority)
    followers=False,                    # Automatic download the list of your followers
    followers_order=FollowersOrder.ASC  # Sort the followers list by follow date. ASC or DESC
)
