#!/usr/local/bin/python3
# coding: utf-8

# ytdlbot - constant.py
# 8/16/21 16:59
#

__author__ = "Peyman"

import os

from config import (
    AFD_LINK,
    COFFEE_LINK,
    ENABLE_CELERY,
    FREE_DOWNLOAD,
    REQUIRED_MEMBERSHIP,
    TOKEN_PRICE,
)
from database import InfluxDB
from utils import get_func_queue


class BotText:
    start ="welcome send /help for help"
    help = f"""bot is working correctly please wait

coded by @l3lackvpn

💢 دستورات
/start
/help
/settings
/about
    """


    private = "This bot is for private use"

    settings = """
لطفاً فرمت و کیفیت مورد نظر برای ویدیوی خود را انتخاب کنید. توجه داشته باشید که این تنظیمات فقط برای ویدیوهای یوتیوب اعمال می‌شوند.

کیفیت بالا توصیه می‌شود. کیفیت متوسط معادل 720P است، در حالی که کیفیت پایین معادل 480P می‌باشد.

لطفاً به یاد داشته باشید که اگر انتخاب کنید ویدیو را به عنوان یک سند ارسال کنید، امکان استریم آن وجود ندارد.

تنظیمات فعلی شما:
کیفیت ویدیو: {0}
فرمت ارسال: {1}
"""
    custom_text = os.getenv("CUSTOM_TEXT", "")

    @staticmethod
    def get_receive_link_text() -> str:
        reserved = get_func_queue("reserved")
        if ENABLE_CELERY and reserved:
            text = f"more request than you can please wait {reserved}."
        else:
            text = "Your request has been added please wait"

        return text

    @staticmethod
    def ping_worker() -> str:
        from tasks import app as celery_app

        workers = InfluxDB().extract_dashboard_data()
        # [{'celery@BennyのMBP': 'abc'}, {'celery@BennyのMBP': 'abc'}]
        response = celery_app.control.broadcast("ping_revision", reply=True)
        revision = {}
        for item in response:
            revision.update(item)

        text = ""
        for worker in workers:
            fields = worker["fields"]
            hostname = worker["tags"]["hostname"]
            status = {True: "✅"}.get(fields["status"], "❌")
            active = fields["active"]
            load = "{},{},{}".format(fields["load1"], fields["load5"], fields["load15"])
            rev = revision.get(hostname, "")
            text += f"{status}{hostname} **{active}** {load} {rev}\n"

        return text
