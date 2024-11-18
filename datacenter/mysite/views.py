# Create your views here.

from django.shortcuts import render, redirect
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import teacher,teacher_data , user_rating,syllabus_second,teacher_second, teacher_third, teacher_fourth, teacher_fifth,teacher_sixth,teacher_seventh, teacher_eighth,syllabus
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import sqlite3

from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, AudioMessage ,TextSendMessage, TextMessage, ImageSendMessage, ImageCarouselColumn, URIAction, ImageCarouselTemplate, QuickReply, QuickReplyButton, MessageAction
from linebot.models import *
from linebot.models import TemplateSendMessage, ButtonsTemplate, MessageAction
from linebot.models.events import FollowEvent

import subprocess

# 初始化 LineBotApi 和 WebhookHandler
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META.get('HTTP_X_LINE_SIGNATURE', '')
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            for event in events:
                handler.handle(body, signature)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@handler.add(FollowEvent)  # 用戶剛加入好友就會觸發事件
def handle_follow(event):
    try:
        template_button = TemplateSendMessage(
            alt_text='選擇你的年級',
            template=ButtonsTemplate(
                title='選擇你的年級查詢課程評價',
                text='課程評價',
                actions=[
                    MessageAction(label='一年級', text='我是一年級'),
                    MessageAction(label='二年級', text='我是二年級'),
                    MessageAction(label='三年級', text='我是三年級'),
                    MessageAction(label='四年級', text='我是四年級'),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, template_button)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='按鈕設定有錯誤'))

def send_rating_quick_reply(event): #用戶評分
    message = TextSendMessage(
        text='請為我們評分',
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="⭐", text='一顆星')),
                QuickReplyButton(action=MessageAction(label="⭐⭐", text='兩顆星')),
                QuickReplyButton(action=MessageAction(label="⭐⭐⭐", text='三顆星')),
                QuickReplyButton(action=MessageAction(label="⭐⭐⭐⭐", text='四顆星')),
                QuickReplyButton(action=MessageAction(label="⭐⭐⭐⭐⭐", text='五顆星')),
            ]
        )
    )

    line_bot_api.reply_message(event.reply_token, message)


@handler.add(MessageEvent, message=TextMessage)
#取得使用者回傳的文字
def handle_teacher(event):
    
    user_id=event.source.user_id

    mtext = event.message.text #event.message.text是用戶傳送的訊息
    teachers = ['統計學', '微積分', '會計學', '供應鏈概論', '管理軟體概論', '中文閱讀與表達(一)', '體育(一)', '服務教育(一)']
    teacher_se = ['生產與作業管理', '作業研究', '經濟學', '管理學', '中文閱讀與表達(二)', '服務教育(二)', '體育(二)', '程式設計']
    teacher_3=['行銷管理','管理資訊系統','存貨管理','採購管理','電子商務','資料庫應用','流通管理']
    teacher_4=['物流管理總論','金流管理總論','生產端管理','區塊鏈應用','綠色行銷','智慧商務']
    teacher_5=['大數據分析','資訊流管理總論','綠色供應鏈總論','供應端管理','財務管理','產業智慧化']
    teacher_6=['實務專題(一)','緊急運籌總論','需求預測','供應商關係管理','供應鏈資源規劃']
    teacher_7=['實務專題(二)','產業分析','就業講座','永續發展']
    teacher_8=['緊急應變','學期實習']
    scm_teacher=['李勝祥','李穎','林義屏','洪榮耀','徐賢斌','溫源鳳','潘郁仁','鄭玉惠','黃彥登']
    key_words=['高科楠梓校區教室位置','選課日程','如何繳費','教授研究室位置','畢業門檻','行事曆']

    #要定義為字典，非集合
    rating_map = {
        '一顆星': 1,
        '兩顆星': 2,
        '三顆星': 3,
        '四顆星': 4,
        '五顆星': 5,
        }

    if mtext in teachers:
            teacher_info = teacher.objects.get(ccourse=mtext)
            response_text = (
                f"課程名稱: {teacher_info.ccourse}\n"
                f"授課老師: {teacher_info.cName}\n"
                f"學期: {teacher_info.csemester}\n"
                f"開課年級: {teacher_info.cgrade}\n"
                f"性別: {teacher_info.cGender}\n"
                f"Email: {teacher_info.cEmail}\n"
                f" {teacher_info.cdescription}"
            )
            message = TextSendMessage(text=response_text)
            
            #第一組按鈕
            template_button_1= TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        # 在發送完訊息後，再發送按鈕樣板訊息
            #第二組按鈕
            template_button_2=TemplateSendMessage(
                alt_text='請選擇按鈕',
                template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
            messages = [message, template_button_1, template_button_2]
            line_bot_api.reply_message(event.reply_token, messages)
    elif mtext in teacher_se:
            teacher_info = teacher_second.objects.get(acourse=mtext) #從資料庫找資料語法，N_info=資料庫名稱.objects.get(要查找的名稱=mtext)
            response_text = (
                f"課程名稱: {teacher_info.acourse}\n"
                f"授課老師: {teacher_info.aName}\n"
                f"學期: {teacher_info.asemester}\n"
                f"開課年級: {teacher_info.agrade}\n"
                f"性別: {teacher_info.aGender}\n"
                f"Email: {teacher_info.aEmail}\n"
                f" {teacher_info.adescription}"
            )
            
            message = TextSendMessage(text=response_text)

            template_button_1= TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'),
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
            #第二組按鈕
            template_button_2=TemplateSendMessage(
                alt_text='請選擇按鈕',
                template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'),
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
            messages = [message, template_button_1, template_button_2]
            line_bot_api.reply_message(event.reply_token, messages)
    elif mtext in teacher_3:
            teacher_info = teacher_third.objects.get(acourse=mtext)
            response_text = (
                f"課程名稱: {teacher_info.acourse}\n"
                f"授課老師: {teacher_info.aName}\n"
                f"學期: {teacher_info.asemester}\n"
                f"開課年級: {teacher_info.agrade}\n"
                f"性別: {teacher_info.aGender}\n"
                f"Email: {teacher_info.aEmail}\n"
                f" {teacher_info.adescription}"
        )
            message = TextSendMessage(text=response_text)

        # 在發送完訊息後，再發送按鈕樣板訊息
            template_button_1 = TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        # 在發送完訊息後，再發送按鈕樣板訊息
            #第二組按鈕
            template_button_2=TemplateSendMessage(
                alt_text='請選擇按鈕',
                template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
            messages = [message, template_button_1, template_button_2]
            line_bot_api.reply_message(event.reply_token, messages)
    elif mtext in teacher_4:
            teacher_info = teacher_fourth.objects.get(acourse=mtext)
            response_text = (
                f"課程名稱: {teacher_info.acourse}\n"
                f"授課老師: {teacher_info.aName}\n"
                f"學期: {teacher_info.asemester}\n"
                f"開課年級: {teacher_info.agrade}\n"
                f"性別: {teacher_info.aGender}\n"
                f"Email: {teacher_info.aEmail}\n"
                f" {teacher_info.adescription}"
            )
            message = TextSendMessage(text=response_text)

        # 在發送完訊息後，再發送按鈕樣板訊息
            template_button_1 = TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )


        #依次發送這兩組訊息
            messages = [message, template_button_1]
            line_bot_api.reply_message(event.reply_token, messages)

    elif mtext in teacher_5:
            teacher_info = teacher_fifth.objects.get(acourse=mtext)
            response_text = (
                f"課程名稱: {teacher_info.acourse}\n"
                f"授課老師: {teacher_info.aName}\n"
                f"學期: {teacher_info.asemester}\n"
                f"開課年級: {teacher_info.agrade}\n"
                f"性別: {teacher_info.aGender}\n"
                f"Email: {teacher_info.aEmail}\n"
                f" {teacher_info.adescription}"
            )
            message = TextSendMessage(text=response_text)
        # 在發送完訊息後，再發送按鈕樣板訊息
            template_button_1 = TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        # 在發送完訊息後，再發送按鈕樣板訊息
            #第二組按鈕
            template_button_2=TemplateSendMessage(
                alt_text='請選擇按鈕',
                template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
            messages = [message, template_button_1, template_button_2]
            line_bot_api.reply_message(event.reply_token, messages)
    elif mtext in teacher_6:
            teacher_info = teacher_sixth.objects.get(acourse=mtext)
            response_text = (
                f"課程名稱: {teacher_info.acourse}\n"
                f"授課老師: {teacher_info.aName}\n"
                f"學期: {teacher_info.asemester}\n"
                f"開課年級: {teacher_info.agrade}\n"
                f"性別: {teacher_info.aGender}\n"
                f"Email: {teacher_info.aEmail}\n"
                f" {teacher_info.adescription}"
            )
            message = TextSendMessage(text=response_text)

        # 在發送完訊息後，再發送按鈕樣板訊息
            template_button_1 = TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        # 在發送完訊息後，再發送按鈕樣板訊息
            #第二組按鈕
            template_button_2=TemplateSendMessage(
                alt_text='請選擇按鈕',
                template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
            messages = [message, template_button_1, template_button_2]
            line_bot_api.reply_message(event.reply_token, messages)
    elif mtext in teacher_7:
            teacher_info = teacher_seventh.objects.filter(acourse=mtext)
            response_text = (
                f"課程名稱: {teacher_info.acourse}\n"
                f"授課老師: {teacher_info.aName}\n"
                f"學期: {teacher_info.asemester}\n"
                f"開課年級: {teacher_info.agrade}\n"
                f"性別: {teacher_info.aGender}\n"
                f"Email: {teacher_info.aEmail}\n"
                f" {teacher_info.adescription}"
            )
            message = TextSendMessage(text=response_text)
        # 在發送完訊息後，再發送按鈕樣板訊息
            template_button_1 = TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        # 在發送完訊息後，再發送按鈕樣板訊息
            #第二組按鈕
            template_button_2=TemplateSendMessage(
                alt_text='請選擇按鈕',
                template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
            messages = [template_button_1, template_button_2]
            line_bot_api.reply_message(event.reply_token, messages)
    elif mtext in teacher_8:
            teacher_info = teacher_eighth.objects.get(acourse=mtext)
            response_text = (
                f"課程名稱: {teacher_info.acourse}\n"
                f"授課老師: {teacher_info.aName}\n"
                f"學期: {teacher_info.asemester}\n"
                f"開課年級: {teacher_info.agrade}\n"
                f"性別: {teacher_info.aGender}\n"
                f"Email: {teacher_info.aEmail}\n"
                f" {teacher_info.adescription}"
            )
            message = TextSendMessage(text=response_text)
        # 在發送完訊息後，再發送按鈕樣板訊息
            template_button_1 = TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        # 在發送完訊息後，再發送按鈕樣板訊息
            #第二組按鈕
            template_button_2=TemplateSendMessage(
                alt_text='請選擇按鈕',
                template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
            messages = [message, template_button_1, template_button_2]
            line_bot_api.reply_message(event.reply_token, messages)


    elif mtext=='我是一年級':
        template_button = TemplateSendMessage(
            alt_text='選擇學期',
            template=ButtonsTemplate(
                title='你選擇了一年級',
                text='請選擇學期',
                actions=[
                    MessageAction(label='上學期', text='一年級上學期課程評價'),
                    MessageAction(label='下學期', text='一年級下學期課程評價'),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, template_button)   
    elif mtext=='一年級上學期課程評價':
        message=TextSendMessage(text="必修：統計學、微積分、會計學、供應鏈概論、管理軟體概論、中文閱讀與表達(一)、 體育(一)、 服務教育(一)；請輸入課程名稱")
        line_bot_api.reply_message(event.reply_token, message)
    elif mtext=='一年級下學期課程評價':
        message=TextSendMessage(text="必修：生產與作業管理、作業研究、經濟學、管理學、中文閱讀與表達(二)、服務教育(二)、體育(二) 選修：程式設計；請輸入課程名稱")

        line_bot_api.reply_message(event.reply_token, message)

    elif mtext=='我是二年級':
        template_button = TemplateSendMessage(
            alt_text='選擇學期',
            template=ButtonsTemplate(
                title='你選擇了二年級',
                text='請選擇學期',
                actions=[
                    MessageAction(label='上學期', text='二年級上學期課程評價'),
                    MessageAction(label='下學期', text='二年級下學期課程評價'),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, template_button) 
    elif mtext=='二年級上學期課程評價':
        message=TextSendMessage(text="必修：行銷管理、管理資訊系統、存貨管理、採購管理  選修：電子商務、資料庫應用、流通管理；請輸入課程名稱")
        line_bot_api.reply_message(event.reply_token, message)
    elif mtext=='二年級下學期課程評價':
        message=TextSendMessage(text="必修：物流管理總論、金流管理總論、生產端管理  選修：區塊鏈應用、綠色行銷、智慧商務；請輸入課程名稱")
        line_bot_api.reply_message(event.reply_token, message)
   
    elif mtext=='我是三年級':
        template_button = TemplateSendMessage(
            alt_text='選擇學期',
            template=ButtonsTemplate(
                title='你選擇了三年級',
                text='請選擇學期',
                actions=[
                    MessageAction(label='上學期', text='三年級上學期課程評價'),
                    MessageAction(label='下學期', text='三年級下學期課程評價'),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, template_button)
    elif mtext=='三年級上學期課程評價':
        message=TextSendMessage(text="必修：大數據分析、資訊流管理總論、綠色供應鏈總論、供應端管理  選修：財務管理、產業智慧化；請輸入課程名稱")
        line_bot_api.reply_message(event.reply_token, message)
    elif mtext=='三年級下學期課程評價':
        message=TextSendMessage(text="必修：實務專題(一)、 緊急運籌總論、需求預測、  選修：供應商關係管理、供應鏈資源規劃 ；請輸入課程名稱")
        line_bot_api.reply_message(event.reply_token, message)
    
    elif mtext=='我是四年級':
        template_button = TemplateSendMessage(
            alt_text='選擇學期',
            template=ButtonsTemplate(
                title='你選擇了四年級',
                text='請選擇學期',
                actions=[
                    MessageAction(label='上學期', text='四年級上學期課程評價'),
                    MessageAction(label='下學期', text='四年級下學期課程評價'),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, template_button) 
    elif mtext=='四年級上學期課程評價':
        message=TextSendMessage(text="必修：實務專題(二)  選修：產業分析、就業講座、永續發展 ；請輸入課程名稱") 
        line_bot_api.reply_message(event.reply_token, message)
    elif mtext=='四年級下學期課程評價':
        message=TextSendMessage(text="必修：無 選修：緊急應變、學期實習 ；請輸入課程名稱")
        line_bot_api.reply_message(event.reply_token, message)

    elif mtext=='其他資訊':
        template_button_1 = TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'),
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )

        #第二組按鈕
        template_button_2=TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'),
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
        line_bot_api.reply_message(event.reply_token, [template_button_1, template_button_2])     

    elif mtext == '系所辦公室資訊':
        response_text=("電話：07-3617141 #23452、23453，E-mail：uioffice01@nkust.edu.tw")
        message = TextSendMessage(text=response_text)
        # 在發送完訊息後，再發送按鈕樣板訊息
        template_button_1= TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        #第二組按鈕
        template_button_2=TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        # 可以在同一個回應中依次發送兩個訊息
        line_bot_api.reply_message(event.reply_token, [message, template_button_1, template_button_2])
    
    elif mtext == '外語學習資源':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(
                image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTI3sca86q9B6ybp6FWBQC_7xlJL5UcYXgUQ&s',
                action=URIAction(label='Easy Test', uri='https://www.easytest.nkust.edu.tw/index.aspx?A=login')
            ),
            ImageCarouselColumn(
                image_url='https://flec.nkust.edu.tw/var/file/46/1046/pictures/161/m/mczh-tw400x400_small49556_989731529909.png',
                action=URIAction(label='英文泛閱讀平台', uri='https://flec.nkust.edu.tw/p/405-1046-49556,c3536.php?Lang=zh-tw')
            ),
            ImageCarouselColumn(
                image_url='https://dictionary.cambridge.org/external/images/og-image.png',
                action=URIAction(label='劍橋辭典', uri='https://dictionary.cambridge.org/zht/')
            ),
            ImageCarouselColumn(
                image_url='https://yt3.googleusercontent.com/wiqkoOfsuG8x3jXjJiaGUc80FBMhYFMCGHVMBHg5MetnYYps3o0LiZQiWoCHx_Kk33I7Tr_c=s900-c-k-c0x00ffffff-no-rj',
                action=URIAction(label='VOA', uri='https://www.voanews.com/')
            ),

            ImageCarouselColumn(
                image_url='https://s3-eu-west-1.amazonaws.com/tpd/logos/62050d46efdf4ea5fc6026c7/0x0.png',
                action=URIAction(label='Brit Council', uri='https://learnenglish.britishcouncil.org/')
            ),

            ImageCarouselColumn(
                image_url='https://yt3.googleusercontent.com/6pw8YF3c0ZGAYzPfEe6ZoUO0yxoa5_ymOSB1_-dkgvS1WWWM3PmRwHV_JK6dLdpJzypGnh3qeQ=s900-c-k-c0x00ffffff-no-rj',
                action=URIAction(label='BBC English', uri='http://www.bbc.co.uk/learningenglish/')
            ),
            ImageCarouselColumn(
                image_url='https://i.imgur.com/gXa5xiR.png',
                action=URIAction(label='Voicetube', uri='https://tw.voicetube.com/')
            ),

            ImageCarouselColumn(
                image_url='https://agirls.aottercdn.com/media/a512ab8d-a7d9-4827-b5ca-5f9a9364741b.png',
                action=URIAction(label='Youglish', uri='https://youglish.com/')
            ),
            ImageCarouselColumn(
                image_url='https://play-lh.googleusercontent.com/bT4gxDoimrFBp41Djk6Yt3fN1AHUaclTPg2f19sxorRBLssLNJyKUM5ZMQ91H1KsUA',
                action=URIAction(label='Word UP', uri='https://shop.wordup.com.tw/')
            ),
        ])
        message = TemplateSendMessage(alt_text='以下是練習外語的管道', template=image_carousel_template)

               # 在發送完訊息後，再發送按鈕樣板訊息
        template_button_1 = TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        # 在發送完訊息後，再發送按鈕樣板訊息
            #第二組按鈕
        template_button_2=TemplateSendMessage(
                alt_text='請選擇按鈕',
                template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
        messages = [message, template_button_1, template_button_2]
        line_bot_api.reply_message(event.reply_token, messages)

    elif mtext == '老師資訊':
        # 第一組按鈕樣板訊息，因為按鈕一次只能四個
        template_button_1 = TemplateSendMessage(
        alt_text='你想了解哪位老師資訊',
        template=ButtonsTemplate(
            title='請選擇',
            text='請選擇老師',
            actions=[
                MessageAction(label='李勝祥', text='李勝祥'),
                MessageAction(label='李穎', text='李穎'),
                MessageAction(label='林義屏', text='林義屏'),
            ]
        )
    )

        # 第二組按鈕樣板訊息
        template_button_2 = TemplateSendMessage(
        alt_text='你想了解哪位老師資訊',
        template=ButtonsTemplate(
            title='請選擇',
            text='請選擇老師',
            actions=[
                MessageAction(label='徐賢斌', text='徐賢斌'),
                MessageAction(label='溫源鳳', text='溫源鳳'),
                MessageAction(label='洪榮耀', text='洪榮耀'),

            ]
        )
    )
    
        template_button_3 = TemplateSendMessage(
        alt_text='你想了解哪位老師資訊',
        template=ButtonsTemplate(
            title='請選擇',
            text='請選擇老師',
            actions=[
                MessageAction(label='潘郁仁', text='潘郁仁'),
                MessageAction(label='鄭玉惠', text='鄭玉惠'),
                MessageAction(label='黃彥登', text='黃彥登'),

            ]
        )
    )

        #依次發送這兩組訊息
        line_bot_api.reply_message(event.reply_token, [template_button_1, template_button_2,template_button_3])

    elif mtext in scm_teacher:
        try:
            teacher_info = teacher_data.objects.get(name=mtext) 
            response_text = (
            f"老師姓名: {teacher_info.name}\n"
            f"職位: {teacher_info.position}\n"
            f"專長項目: {teacher_info.strengths}\n"
            f"分機: {teacher_info.tel}\n"
            f"Email: {teacher_info.mail}\n"
            f"網站: {teacher_info.website}\n"

        )       
            message = TextSendMessage(text=response_text)
  
        except:
            response_text = "找不到該老師的資訊。"
            message = TextSendMessage(text=response_text)   
       
       # 在發送完訊息後，再發送按鈕樣板訊息
        template_button_1 = TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        # 在發送完訊息後，再發送按鈕樣板訊息
            #第二組按鈕
        template_button_2=TemplateSendMessage(
                alt_text='請選擇按鈕',
                template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
        messages = [message, template_button_1, template_button_2]
        line_bot_api.reply_message(event.reply_token, messages)

    elif mtext=='授課大綱': 
        template_button = TemplateSendMessage(
            alt_text='請選擇年級',
            template=ButtonsTemplate(
                title='先選年級 再輸入學期加上課程名稱',
                text='如:113上+你想查詢的課程',
                actions=[            
                    MessageAction(label='一年級', text='我想了解一年級課程的授課大綱'),
                    MessageAction(label='二年級', text='我想了解二年級課程的授課大綱'),
                    MessageAction(label='三年級', text='我想了解三年級課程的授課大綱'),
                    MessageAction(label='四年級', text='我想了解四年級課程的授課大綱'),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, template_button) 

    elif mtext== '我想了解一年級課程的授課大綱':
        message=TextSendMessage(text="上學期：統計學、微積分、會計學、供應鏈概論、管理軟體概論、中文閱讀與表達(一)、 體育(一)、 服務教育(一)；下學期：生產與作業管理、作業研究、經濟學、管理學、中文閱讀與表達(二)、服務教育(二)、體育(二)、程式設計")
        line_bot_api.reply_message(event.reply_token, message)

    elif mtext== '我想了解二年級課程的授課大綱':
        message=TextSendMessage(text="上學期：行銷管理、管理資訊系統、存貨管理、採購管理、電子商務、資料庫應用、流通管理；下學期：物流管理總論、金流管理總論、生產端管理、區塊鏈應用、綠色行銷、智慧商務")
        line_bot_api.reply_message(event.reply_token, message)

    elif mtext== '我想了解三年級課程的授課大綱':
        message=TextSendMessage(text="上學期：大數據分析、資訊流管理總論、綠色供應鏈總論、供應端管理、財務管理、產業智慧化；下學期：實務專題(一)、 緊急運籌總論、需求預測、供應商關係管理、供應鏈資源規劃")       
        line_bot_api.reply_message(event.reply_token, message)

    elif mtext== '我想了解四年級課程的授課大綱':
        message=TextSendMessage(text="上學期：實務專題(二)、產業分析、就業講座、永續發展；下學期：緊急應變、學期實習")  
        line_bot_api.reply_message(event.reply_token, message)

    elif '113上' in mtext:
        semester='113上'
        course=mtext.split('113上')[1]

        syllabus_info=syllabus.objects.filter(Q(nsemester=semester)&Q(ncourse=course)) #filter條件過濾資料，Q是例如使用 OR、AND、NOT 等邏輯運算。

        if syllabus_info.exists():
            response_text = "\n\n".join([
            f"課程名稱：{info.ncourse}\n"
            f"授課老師：{info.nname}\n"
            f"開課學期：{info.nsemester}\n"
            f"使用書本：{info.nbook}\n"
            f"課程表：{info.nschedule}\n"
            f"評分方式：{info.ngrade}\n" 
            for info in syllabus_info
                ])
        else:
            response_text="找不到資料"
        # 將 response_text 賦值給 message 並發送
        message = TextSendMessage(text=response_text) #要賦予一個messge值，不然系統找不到
            
            
        template_button_1 = TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        # 在發送完訊息後，再發送按鈕樣板訊息
            #第二組按鈕
        template_button_2=TemplateSendMessage(
                alt_text='請選擇按鈕',
                template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
        messages = [message, template_button_1, template_button_2]
        line_bot_api.reply_message(event.reply_token, messages)

    elif '113下' in mtext:
        semester='113下'
        course=mtext.split('113下')[1]

        syllabus_info=syllabus_second.objects.filter(Q(nsemester=semester)&Q(ncourse=course))
        #filter條件過濾資料，Q是例如使用 OR、AND、NOT 等邏輯運算。

        if syllabus_info.exists():
            response_text = "\n\n".join([
            f"課程名稱：{info.ncourse}\n"
            f"授課老師：{info.nname}\n"
            f"開課學期：{info.nsemester}\n"
            f"使用書本： {info.nbook}\n"
            f"課程表：{info.nschedule}\n"
            f"評分方式：{info.ngrade}\n" 
            for info in syllabus_info
                ])
            
        else:
             response_text="找不到資料"

        # 將 response_text 賦值給 message 並發送
        message = TextSendMessage(text=response_text)
        template_button_1 = TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        # 在發送完訊息後，再發送按鈕樣板訊息
            #第二組按鈕
        template_button_2=TemplateSendMessage(
                alt_text='請選擇按鈕',
                template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        #依次發送這兩組訊息
        messages = [message, template_button_1, template_button_2]
        line_bot_api.reply_message(event.reply_token, messages)

    elif mtext=='我要為機器人評分':
         send_rating_quick_reply(event)

    elif mtext in rating_map: 
        #接收評分
        rating_value=rating_map[mtext]

        #儲存至資料庫
        user_rating.objects.create(user_id=user_id, rating=rating_value)

        #將rating_value轉成字串才能和其他文字一起顯示
        response_text ="感謝您的評分，你給了"+str(rating_value)+"顆星！" 
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))

    elif mtext =='課程評價':
        handle_follow(event)

    elif mtext=='語音輸入關鍵字':
        response_text=("其他資訊、系所辦公室資訊、外語學習資源、老師資訊、授課大綱、我要為機器人評分、課程評價；請如實照著上面輸入")
        message = TextSendMessage(text=response_text)
        # 在發送完訊息後，再發送按鈕樣板訊息
        template_button_1= TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )
        #第二組按鈕
        template_button_2=TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        # 可以在同一個回應中依次發送兩個訊息
        line_bot_api.reply_message(event.reply_token, [message, template_button_1, template_button_2])

    elif mtext=='學雜繳費資訊':
    # 在發送完訊息後，再發送按鈕樣板訊息
        template_button_1= TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='外語學習資源', text='外語學習資源'), #授課大綱未完成
                    MessageAction(label='老師資訊', text='老師資訊'),
                    MessageAction(label='授課大綱', text='授課大綱'),
                    MessageAction(label='課程評價', text='課程評價'),
                ]
            )
        )

        #第二組按鈕
        template_button_2=TemplateSendMessage(
            alt_text='請選擇按鈕',
            template=ButtonsTemplate(
                title='你可能感興趣的其他資訊',
                text='請選擇',
                actions=[
                    MessageAction(label='系所辦公室資訊', text='系所辦公室資訊'), #授課大綱未完成
                    MessageAction(label='我要為機器人評分', text='我要為機器人評分'),
                    MessageAction(label='語音輸入關鍵字', text='語音輸入關鍵字'),
                    MessageAction(label='學雜繳費資訊', text='學雜繳費資訊'),
                ]
            )             
        )
        # 可以在同一個回應中依次發送兩個訊息
        line_bot_api.reply_message(event.reply_token, [template_button_1, template_button_2])

    elif mtext in key_words:
        message = TextSendMessage(text=mtext)
        line_bot_api.reply_message(event.reply_token, message)









    else:
         line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請確認你的訊息是否為查詢關鍵字，如想知道有哪些關鍵字，請查找其他資訊中的語音輸入關鍵字，或直接點選其他資訊直接查找'),timeout=10)
        

@handler.add(MessageEvent, message=AudioMessage)  # 取得聲音時做的事情
def handle_message_Audio(event):
    #接收使用者語音訊息並存檔
    UserID = event.source.user_id
    path='./audio/'
    
    #檢查audio資料夾是否存在，沒有就創建
    directory='/tmp/audio'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    
    path = os.path.join(directory, f"{UserID}.wav")
    
    audio_content = line_bot_api.get_message_content(event.message.id)
    
    with open(path, 'wb') as fd:
        for chunk in audio_content.iter_content():
            fd.write(chunk)        
    
    
    #轉檔
    sound = AudioSegment.from_file_using_temporary_files(path) #透過 pydub 讀取剛保存的音訊檔案。
    path = os.path.splitext(path)[0]+'.wav'
    sound.export(path, format="wav") #將音訊檔案轉換成 .wav
    
    #辨識
    r = sr.Recognizer() 
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    text = r.recognize_google(audio,language='zh-Hant')
    
    event.message.text=text
    handle_teacher(event)



def index(request):
    
    html="<h2>你好</h2><hr>"
    return HttpResponse(html)


