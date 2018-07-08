# Script By @Adi
# Please Don’t Edit If You Doesn’t Have A Permission.
# © Adi, 2018 All Rights Reserved.

from gtts import gTTS
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from googletrans import Translator
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from humanfriendly import format_timespan, format_size, format_number, format_length

from flask import Flask, request, make_response

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *

import time, random, sys, json, codecs, threading, glob, re, string, os, requests, six, ast, pytz, urllib3, urllib.parse, traceback, atexit, html5lib, wikipedia, goslate

app = Flask(__name__)

line_bot_api = LineBotApi('HjEZRNk3czUVKof7ZLxIO3Bv8zdkeW1UBTPl9HNMmYgVHtQapRJr2ZyVB8qOMVrdmkTDfZ7nRjnavXF8xgO9qeBVd47MSgfP3k0J+oPWjw8+8dli+crm5VKHcFi+xidY2razYmls+0EC9CxIYnbOYwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a4ce4df86f3b49ce0ab0a91f1f4fec16')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = (event.message.text).lower()
    msg = text.split()
    groupId = event.source.group_id
    userId = event.source.user_id
    profile = line_bot_api.get_profile(userId)
    profile_name = profile.display_name
    profile_picture = profile.picture_url
    profile_sm = profile.status_message


    if text == '.toramnews':
        target = 'https://en.toram.jp/information/?type_code=all'
        req = requests.get(target)
        bs = BeautifulSoup(req.content, "html.parser")
        dataa = bs.find_all("div",{"class":"useBox"})
        dataaa = dataa[0].find_all("li")
        content = "~ Toram Online Official News ~\n\n\n"
        num = 0
        i = 0

        for data in dataaa:
            num += 1
            if i <= 9:
                pass

            data = dataaa[i].find('a')
            news = data.text
            link = data["href"]
            tx = "✓ Total ada {} berita.\n\n\n✓ Info selengkapnya, klik:\n➡ https://en.toram.jp/information/?type_code=all".format(len(dataaa))
            i = i + 1

            content += "{}). News: {}\n      More info: https://en.toram.jp{}\n\n".format(num, news, link)

        line_bot_api.reply_message(
            event.reply_token, [
            TextSendMessage(text="[ R E S U L T ]\n\nBot using by [ "+profile_name+" ] on Toram News:\n\n"+content+tx)])

        return

    elif text == '.pic':
        target_url = 'https://www.ptt.cc/bbs/Beauty/index.html'
        res = requests.get(target_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        pic_urls = []

        while (len(pic_urls) < 1):
            for data in soup.select('.r-ent'):
                pushes = data.select_one('.nrec').text
                if pushes == '爆' or (pushes != '' and 'X' not in pushes and int(pushes) > 50):
                    title = data.find('a', href=True)
                    heading = title.text
                    link = 'https://www.ptt.cc' + title['href']

                    if '公告' in heading:
                        continue

                    res2 = requests.get(link)
                    soup2 = BeautifulSoup(res2.text, 'html.parser')

                    for data2 in soup2.select_one('#main-content').find_all('a', href=True):
                        if 'https://i.imgur.com' in data2['href']:
                            pic_urls.append(data2['href'])

                    break

            last_page_url = 'https://www.ptt.cc' + soup.select('.btn.wide')[1]['href']
            res = requests.get(last_page_url)
            soup = BeautifulSoup(res.text, 'html.parser')

        image_message = ImageSendMessage(
            original_content_url=random.choice(pic_urls),
            preview_image_url=random.choice(pic_urls)
        )

        line_bot_api.reply_message(
            event.reply_token,
            image_message
        )
        return


    elif text == '.samehadaku':
        target = 'https://samehadaku.tv'
        req = requests.get(target)
        bs = BeautifulSoup(req.content, "html5lib")
        dataa = bs.find_all("ul",{"class":"posts-items posts-list-container"})
        dataaa = dataa[0].find_all("li",{"class":"post-item tie-standard"})
        content = "~ Last Update Anime: Samehadaku ~\n\n[ R E S U L T ]\n\n\n"
        num = 0
        i = 0
        j = 0

        for data in dataaa:
            num += 1
            if i <= 13:
                pass

            data = dataaa[i].find('a')
            date = dataaa[j].find('span').text
            name = data["title"]
            link = data["href"]
            time = date
            content += "{}).  Judul: {}".format(num, name)
            content += "\n     Link: {}".format(link)
            content += "\n     Tanggal Rilis: {}\n\n".format(time)
            te = "✓ Total ada {} update anime.\n\n\n✓ Info update anime selengkapnya, klik:\n➡ https://www.samehadaku.tv/".format(len(dataaa))
            i = i + 1
            j = j + 1

        line_bot_api.reply_message(
            event.reply_token, [
            TextSendMessage(text="Bot using by [ "+profile_name+" ] on Samehadaku:\n\n"+content)])

        return


    elif text == '.joke':
        url_req = requests.get('https://raw.githubusercontent.com/abhishtagatya/dlearn-res/master/dotPython/interact/bot_interact.json')
        reply_mes = url_req.json()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(reply_mes["joke"])))


    elif text == '.bye':
        if (userId != 'U45a70016f56dbfc99e6a66673002ecbe'):
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="Akses Ditolak! Hanya owner yang bisa menggunakan command ini."))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Sayounara, "+profile_name+"........................"))
            line_bot_api.leave_group(groupId)


    elif text == '.userid':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hai "+profile_name+", ini adalah id kamu: "+userId))


    elif text == '.myprofile':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="~ [ R E S U L T ] ~\n\n👉 Nama: "+profile_name+"\n👉 Foto Profil: "+profile_picture+"\n👉 Pesan Status: "+profile_sm))


    if '.apakah ' in text:
        rep = text.replace(".apakah ","")
        txt = ["Ya","Tidak","Bisa Jadi","Mungkin","Hoax","Coba tanya lagi"]

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(txt)))


    elif '.carigambar' in text:
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        r = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(search))
        data = r.text
        data = json.loads(data)

        if data["result"] != []:
            items = data["result"]
            path = random.choice(items)
            a = items.index(path)
            b = len(items)

        image_message = ImageSendMessage(
            original_content_url=path,
            preview_image_url=path
        )

        line_bot_api.reply_message(
            event.reply_token,
            image_message
        )


    elif '.zodiak ' in text:
        tanggal = text.replace(".zodiak ","")
        r = requests.get('https://script.google.com/macros/exec?service=AKfycbw7gKzP-WYV2F5mc9RaR7yE3Ve1yN91Tjs91hp_jHSE02dSv9w&nama=siapa&tanggal='+tanggal)
        data = r.text
        data = json.loads(data)
        lahir = data["data"]["lahir"]
        usia = data["data"]["usia"]
        ultah = data["data"]["ultah"]
        zodiak = data["data"]["zodiak"]

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="== I N F O R M A S I ==\n"+"Date Of Birth : "+lahir+"\nAge : "+usia+"\nUltah : "+ultah+"\nZodiak : "+zodiak+"\n== I N F O R M A S I =="))


    elif '.wiki ' in text:
        try:
            wiki = text.replace(".wiki ","")
            wikipedia.set_lang("id")
            results = wiki.find("search")
            pesan = "~ [ R E S U L T ] ~\n\nBot using by [ "+profile_name+"  ] in Wikipedia Search Engine.\n\n\n👉 Nama: "
            pesan += wikipedia.page(wiki).title
            pesan += "\n\n👉 Deskripsi: "
            pesan += wikipedia.summary(wiki, sentences=1)
            pesan += "\n\n👉 Baca Selengkapnya: "
            pesan += wikipedia.page(wiki).url
            pesan += "\n\n\n✓ Baca wikipedia lainnya klik:\n➡ https://id.wikipedia.org/"

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=pesan))

        except:
                try:
                    pesan="Over Text Limit! Please Click link\n"
                    pesan+=wikipedia.page(wiki).url
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=pesan))
                except Exception as e:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=e))


    elif '.lokasi' in text:
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        req = requests.get("https://time.siswadi.com/pray/{}".format(search))
        data = req.text
        data = json.loads(data)
        add = data['location']['address']
        lat = data['location']['latitude']
        lon = data['location']['longitude']

        location_message = LocationSendMessage(
            title='Lokasi',
            address=add,
            latitude=lat,
            longitude=lon
        )

        line_bot_api.reply_message(
            event.reply_token,
            location_message
        )


    if 'meet?' in text:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message
        )


    elif '.calculate' in text:
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        if search == None:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Untuk cara menggunakan kalkulator, ketik .calculate 'nominal'\n\nContoh: .calculate (3e+2i)*(2e-3i)\n\nSelamat mencoba (((o(*ﾟ▽ﾟ*)o)))"))
        else:
            result = requests.get("http://api.mathjs.org/v4/?expr={}".format(search))
            if result == None:
                content = 'Nominal tidak terdefinisi'
            else:
                content = content
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))


    elif '.speed' in text:
        start = time.time()
        elapsed_time = time.time() - start
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="{} detik".format(elapsed_time)))


    elif '.carivideo ' in text:
        query = text.replace(".carivideo ","")
        with requests.session() as s:
            s.headers['user-agent'] = 'Mozilla/5.0'
            url = 'http://www.youtube.com/results'
            params = {'search_query': query}
            r = s.get(url, params=params)
            soup = BeautifulSoup(r.content, 'html5lib')
            num = 0
            hasil = ""
            for a in soup.select('.yt-lockup-title > a[title]'):
                num += 1
                if '&list=' not in a['href']:
                    hasil += "".join((a["title"],"\nhttps://www.youtube.com" + a["href"],"\n\n"))
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=hasil))


    elif '.carilagu ' in text:
        query = text.replace(".carilagu ","")
        cond = query.split("|")
        search = cond[0]
        result = requests.get("http://api.ntcorp.us/joox/search?q={}".format(search))
        data = result.text
        data = json.loads(data)
        if len(cond) == 1:
            num = 0
            ret_ = "╔══[ Result Music ]"
            for music in data["result"]:
                num += 1
                ret_ += "\n╠ {}. {}".format(num, music["single"])
            ret_ += "\n╚══[ Total {} Music ]".format(len(data["result"]))
            ret_ += "\n\nUntuk Melihat Details Music, silahkan gunakan command .carilagu {}|「number」".format(search)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=ret_))
        elif len(cond) == 2:
            num = int(cond[1])
            if num <= len(data["result"]):
                music = data["result"][num - 1]
                result = requests.get("http://api.ntcorp.us/joox/song_info?sid={}".format(music["sid"]))
                data = result.text
                data = json.loads(data)
                if data["result"] != []:
                    ret_ = "╔══[ Music ]"
                    ret_ += "\n╠ Title : {}".format(data["result"]["song"])
                    ret_ += "\n╠ Album : {}".format(data["result"]["album"])
                    ret_ += "\n╠ Size : {}".format(data["result"]["size"])
                    ret_ += "\n╠ Link : {}".format(data["result"]["mp3"][0])
                    ret_ += "\n╚══[ Finish ]"
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=ret_))
                    return

                    image_message = ImageSendMessage(
                        original_content_url=data["result"]["img"],
                        preview_image_url=data["result"]["img"]
                    )

                    line_bot_api.reply_message(
                        event.reply_token,
                        image_message
                    )
                    return


if __name__ == "__main__":
    app.run()
