# coding: utf-8
from urllib import parse
import requests
import csv
import time
import json
import cv2
import hashlib
path_erweima = r"C:\Users\Administrator\Desktop\erweima.jpg"
# 指定 账户的csv路径
path_user = r"C:\Users\Administrator\Desktop\run\user.csv"
# 指定 内容源的csv路径
path_data = r"C:\Users\Administrator\Desktop\run\data.csv"
# 指定图片链接csv路径
path_img = r"C:\Users\Administrator\Desktop\run\img.csv"
# 设置一共上传几天
f_config = csv.reader(open(r"C:\Users\Administrator\Desktop\run\config.csv"))
config_list = []
for config in f_config:
    # print(config)
    config_list.append(config[0])

begin_user = int(config_list[1])
end_user = int(config_list[2])
num_day = int(config_list[0])
content_info = config_list[3]
# 处理 cookie 和 tooken
def get_url(user, n):
    i = user
    username = i[0]
    username = parse.quote(username)
    passw = i[2]
    m = hashlib.md5()
    b = passw.encode(encoding='utf-8')
    m.update(b)
    a_md5 = m.hexdigest()

    url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin"

    payload = "username={}&pwd={}&imgcode=&f=json&userlang=zh_CN&redirect_url=&token=&lang=zh_CN&ajax=1".format(
        username, a_md5)
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Origin': 'https://mp.weixin.qq.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'https://mp.weixin.qq.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie': 'noticeLoginFlag=1; rewardsn=; wxtokenkey=777; ua_id=KTtQx5LTPMru0MSrAAAAAJVizSrOGRQNwCqVJDvvT0I=; pgv_pvi=5359779840; pgv_si=s9167475712; cert=RPSjZXKEStYjbmA7C1dnL9TVlBwQH57h; noticeLoginFlag=1; mm_lang=zh_CN; tvfe_boss_uuid=31e3bead7132992c; pgv_pvid=9854683648; pgv_info=ssid=s5595119350; uuid=42d90eb28eeea24554c6658befc65406; xid=2a85c7581d6ccb987239a355a4e6084c'
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    cookie = requests.utils.dict_from_cookiejar(response.cookies)
    res = response.text
    res = json.loads(res)
    referer = res['redirect_url']
    # print(cookie)
    bizuin = cookie['bizuin']
    cert = cookie['cert']
    fake_id = cookie['fake_id']
    login_certificate = cookie['login_certificate']
    login_sid_ticket = cookie['login_sid_ticket']
    ticket = cookie['ticket']
    ticket_certificate = cookie['ticket_certificate']
    ticket_id = cookie['ticket_id']
    ticket_uin = cookie['ticket_uin']
    uuid = cookie['uuid']

    a = '''noticeLoginFlag=1; rewardsn=; wxtokenkey=777; ua_id=KTtQx5LTPMru0MSrAAAAAJVizSrOGRQNwCqVJDvvT0I=; pgv_pvi=6856870912; pgv_si=s9167475712; cert={}; noticeLoginFlag=1; mm_lang=zh_CN; tvfe_boss_uuid=31e3bead7132992c; pgv_pvid=9854683648; pgv_info=ssid=s5595119350; xid=1194f32639c6b4b714dc8b47565def4b; uuid={}; bizuin={}; ticket={}; ticket_id={}; ticket_uin={}; login_certificate={}; ticket_certificate={}; fake_id={}; login_sid_ticket={}'''.format(
        cert, uuid, bizuin, ticket, ticket_id, ticket_uin, login_certificate,
        ticket_certificate, fake_id, login_sid_ticket)


    url = "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300&rd=821"

    payload = {}
    headers = {
        'Host': 'mp.weixin.qq.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': 'https://mp.weixin.qq.com{}'.format(referer),
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': a,
    }

    requests.packages.urllib3.disable_warnings()
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    name = path_erweima
    img_file = open(name, 'wb')  # 二进制打开文件
    img_file.write(response.content)  # 把图片内容写入文件
    img_file.close()
    time.sleep(1)
    lena = cv2.imread(path_erweima)
    cv2.imshow('picture', lena)
    # cv2.waitKey(1)
    # cv2.waitKey(1)
    url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login"

    payload = "userlang=zh_CN&redirect_url=&token=&lang=zh_CN&f=json&ajax=1"
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Origin': 'https://mp.weixin.qq.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'https://mp.weixin.qq.com{}'.format(referer),
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': a
    }
    while True:
        requests.packages.urllib3.disable_warnings()
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        # print(response.text)
        res = response.text
        res = json.loads(res)
        err_msg = res["base_resp"]["err_msg"]
        if err_msg == 'default':
            print('请使用{}扫码, 当前是第{}个账号'.format(i[3], n))
            cv2.waitKey(1)

        else:
            print('扫码成功')
            break
    cookie_dict = requests.utils.dict_from_cookiejar(response.cookies)
    # print(cookie)
    # print(cookie_dict)
    slave_sid = cookie_dict['slave_sid']
    uuid = cookie['uuid']
    cert = cookie['cert']
    data_ticket = cookie_dict['data_ticket']
    data_bizuin = cookie_dict['data_bizuin']
    slave_user = cookie_dict['slave_user']
    ticket = cookie['ticket']
    ticket_id = cookie['ticket_id']
    pgv_si = 's9167475712'
    pgv_pvi = '6856870912'
    bizuin = cookie_dict['bizuin']
    xid = cookie_dict['xid']
    ua_id = cookie_dict['ua_id']
    noticeLoginFlag = '1'
    mm_lang = cookie_dict['mm_lang']
    List1 = [slave_sid, uuid, cert, data_ticket, data_bizuin, slave_user, ticket, ticket_id, pgv_si, pgv_pvi, bizuin,
             xid, ua_id, noticeLoginFlag, mm_lang]
    List2 = []
    for a in cookie_dict:
        List2.append(a)
    for i in List2:
        if i not in List1:
            n = cookie_dict[i]

            cookie_tup = '''noticeLoginFlag={}; ua_id={} pgv_pvi={}; pgv_si={}; uuid={}; bizuin={}; ticket={}; ticket_id={}; cert={}; data_bizuin={}; data_ticket={}; slave_sid={}; slave_user={}; xid={}; {}={}; mm_lang={}'''.format(
                noticeLoginFlag, ua_id,
                pgv_pvi, pgv_si, uuid, bizuin, ticket, ticket_id, cert, data_bizuin, data_ticket, slave_sid, slave_user,
                xid,
                i, n, mm_lang)
    # print(response.text)
    # {'bizuin': '3570068731', 'data_bizuin': '3570068731', 'data_ticket': 'n8IXzv+0nivL6t8XrklpVcF7xF3RgJ9eJ7xyR34PWYFHN0ybVu/gM78/zSlno2z3', 'mm_lang': 'zh_CN', 'openid2ticket_o--zK1IfT0JjlLi82c4Ob7NfyJb0': '6K4uMmVEyWjzbWpqy8ZZHP3VH0bzP21mwmR877Zptxo=', 'slave_sid': 'MUJZdVBGUEVjUTRnRlUyWEVXU2hJVENyRnlsWUE1N1NkM1lMb0h5Z2taMzlOZE11bnBkRXlBOVhQTlA1MzNmOXU0ajBPaEwwRndhc0ROMnJ0V3lfV0xJb1RRZU5wVjAwdHd2UElaRjFkT2JUUTNieVpxNzRJVDNKdURWdzNISTJlem8yaXRmMnR0cGUwa3pP', 'slave_user': 'gh_00887795e4c9', 'ua_id': 'KTtQx5LTPMru0MSrAAAAAJVizSrOGRQNwCqVJDvvT0I=', 'xid': '9cc33390660e260e4f82fc13261a4431'}
    res = json.loads(response.text)
    redirect = res['redirect_url']
    tooken_url = redirect.split('=')
    tooken = tooken_url[-1]
    return cookie_tup, tooken


# 处理图片
def get_img_link(cookie, tooken, img_list):
    img_url_list1 = []
    # for img_url in data:
    #     img_link = img_url[2]
        # print(img_link)
    for img_info_list in img_list:
        img_url_list = []
        for img_link in img_info_list:
            url = "https://mp.weixin.qq.com/cgi-bin/uploadimg2cdn"

            querystring = {"lang": "zh_CN", "token": tooken, "t": "0.4831930587453287"}

            payload = "imgurl={}&size=b9999_10000&sec=1574670546221&di=da454c54fe1e3754b5fb2606ead1fbd2&imgtype=0&src=data-imgurl=https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1242753632,604280444&fm=26&gp=0.jpg&t=ajax-editor-upload-img&token={}&lang=zh_CN&f=json&ajax=1".format(
                img_link, tooken)
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
                'Accept': "*/*",
                'Accept-Language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'X-Requested-With': "XMLHttpRequest",
                'Origin': "https://mp.weixin.qq.com",
                'Connection': "keep-alive",
                'Referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN".format(
                    tooken),
                'Cookie': cookie,
                'TE': "Trailers",
                'Cache-Control': "no-cache",
                'Host': "mp.weixin.qq.com",
                'Accept-Encoding': "gzip, deflate",
                'Content-Length': "343",
                'cache-control': "no-cache"
            }

            a = 0
            while True:
                a += 1
                # print(a)
                requests.packages.urllib3.disable_warnings()
                response = requests.request("POST", url, data=payload, headers=headers, params=querystring,
                                            verify=False).json()
                if response['errcode'] != 0:
                    requests.packages.urllib3.disable_warnings()
                    response = requests.request("POST", url, data=payload, headers=headers, params=querystring,
                                                verify=False).json()
                    print(response)
                    if a == 20:
                        print('此图片不能使用')
                        break
                    else:
                        pass

                else:
                    img_url_list.append(response['url'])
                    break
        img_url_list1.append(img_url_list)
    return img_url_list1



'''定义八篇文章的content字段'''


def get_content(data, content_info, img_link_list):
    data1 = data[0]
    data2 = data[1]
    data3 = data[2]
    data4 = data[3]
    data5 = data[4]
    data6 = data[5]
    data7 = data[6]
    data8 = data[7]
    img_link_list1 = img_link_list[0]
    img_link_list2 = img_link_list[1]
    img_link_list3 = img_link_list[2]
    img_link_list4 = img_link_list[3]
    img_link_list5 = img_link_list[4]
    img_link_list6 = img_link_list[5]
    img_link_list7 = img_link_list[6]
    img_link_list8 = img_link_list[7]
    data_num1 = len(data1)
    data_str1 = '<section style=""><span style="font-size: 14px;">' + data1[0] + '</span></section>' + content_info
    info_list1 = []
    for n in range(1, data_num1):
        str1 = '<p style=""><span style="font-size: 14px;">'+data1[n]+'</span></p><p style=""><span style="font-size: 14px;"><br></span></p>' + '<p style="text-align: center;"><img class="rich_pages js_insertlocalimg" data-ratio="1" data-s="300,640" data-src=' + img_link_list1[n-1] + ' data-type="png" data-w="100%" style=""></p>'
        info_list1.append(str1)
    info_str1 = ''.join(info_list1)
    content0 = data_str1 + info_str1

    content0 = parse.quote(content0)

    data_num2 = len(data2)
    data_str2 = '<section style=""><span style="font-size: 14px;">' + data2[0] + '</span></section>' + content_info
    info_list2 = []
    for n in range(1, data_num2):
        str2 = '<p style=""><span style="font-size: 14px;">'+data2[n]+'</span></p><p style=""><span style="font-size: 14px;"><br></span></p>' + '<p style="text-align: center;"><img class="rich_pages js_insertlocalimg" data-ratio="1" data-s="300,640" data-src=' + img_link_list2[n-1] + ' data-type="png" data-w="100%" style=""></p>'
        info_list2.append(str2)
    info_str2 = ''.join(info_list2)
    content2 = data_str2 + info_str2
    # print(content2)

    content2 = parse.quote(content2)

    data_num3 = len(data3)
    data_str3 = '<section style=""><span style="font-size: 14px;">' + data3[0] + '</span></section>' + content_info
    info_list3 = []
    for n in range(1, data_num3):
        str3 = '<p style=""><span style="font-size: 14px;">'+data3[n] + '</span></p><p style=""><span style="font-size: 14px;"><br></span></p>' + '<p style="text-align: center;"><img class="rich_pages js_insertlocalimg" data-ratio="1" data-s="300,640" data-src=' + img_link_list3[n-1] + ' data-type="png" data-w="100%" style=""></p>'
        info_list3.append(str3)
    info_str3 = ''.join(info_list3)
    content3 = data_str3 + info_str3
    content3 = parse.quote(content3)
    # print(content3)

    data_num4 = len(data4)
    data_str4 = '<section style=""><span style="font-size: 14px;">' + data4[0] + '</span></section>' + content_info
    info_list4 = []
    for n in range(1, data_num4):
        str4 = '<p style=""><span style="font-size: 14px;">'+data4[n] + '</span></p><p style=""><span style="font-size: 14px;"><br></span></p>' + '<p style="text-align: center;"><img class="rich_pages js_insertlocalimg" data-ratio="1" data-s="300,640" data-src=' + img_link_list4[n-1] + ' data-type="png" data-w="100%" style=""></p>'
        info_list4.append(str4)
    info_str4 = ''.join(info_list4)
    content4 = data_str4 + info_str4
    # print(content4)
    content4 = parse.quote(content4)

    data_num5 = len(data5)
    data_str5 = '<section style=""><span style="font-size: 14px;">' + data5[0] + '</span></section>' + content_info
    info_list5 = []
    for n in range(1, data_num5):
        str5 = '<p style=""><span style="font-size: 14px;">'+data5[n] + '</span></p><p style=""><span style="font-size: 14px;"><br></span></p>' + '<p style="text-align: center;"><img class="rich_pages js_insertlocalimg" data-ratio="1" data-s="300,640" data-src=' + img_link_list5[n-1] + ' data-type="png" data-w="100%" style=""></p>'
        info_list5.append(str5)
    info_str5 = ''.join(info_list5)
    content5 = data_str5 + info_str5
    # print(content5)
    content5 = parse.quote(content5)

    data_num6 = len(data6)
    data_str6 = '<section style=""><span style="font-size: 14px;">' + data6[0] + '</span></section>' + content_info
    info_list6 = []
    for n in range(1, data_num6):
        str6 = '<p style=""><span style="font-size: 14px;">'+data6[n] + '</span></p><p style=""><span style="font-size: 14px;"><br></span></p>' + '<p style="text-align: center;"><img class="rich_pages js_insertlocalimg" data-ratio="1" data-s="300,640" data-src=' + img_link_list6[n-1] + ' data-type="png" data-w="100%" style=""></p>'
        info_list6.append(str6)
    info_str6 = ''.join(info_list6)
    content6 = data_str6 + info_str6
    # print(content6)

    content6 = parse.quote(content6)

    data_num7 = len(data7)
    data_str7 = '<section style=""><span style="font-size: 14px;">' + data7[0] + '</span></section>' + content_info
    info_list7 = []
    for n in range(1, data_num7):
        str7 = '<p style=""><span style="font-size: 14px;">'+data7[n] + '</span></p><p style=""><span style="font-size: 14px;"><br></span></p>' + '<p style="text-align: center;"><img class="rich_pages js_insertlocalimg" data-ratio="1" data-s="300,640" data-src=' + img_link_list7[n-1] + ' data-type="png" data-w="100%" style=""></p>'
        info_list7.append(str7)
    info_str7 = ''.join(info_list7)
    content7 = data_str7 + info_str7
    # print(content7)

    content7 = parse.quote(content7)

    data_num8 = len(data8)
    data_str8 = '<section style=""><span style="font-size: 14px;">' + data8[0] + '</span></section>' + content_info
    info_list8 = []
    for n in range(1, data_num8):
        str8 = '<p style=""><span style="font-size: 14px;">' + data8[n] + '</span></p><p style=""><span style="font-size: 14px;"><br></span></p>' + '<p style="text-align: center;"><img class="rich_pages js_insertlocalimg" data-ratio="1" data-s="300,640" data-src=' + img_link_list8[n-1] + ' data-type="png" data-w="100%" style=""></p>'
        info_list8.append(str8)
    info_str8 = ''.join(info_list8)
    content8 = data_str8 + info_str8
    # print(content8)
    content8 = parse.quote(content8)

    return content0, content2, content3, content4, content5, content6, content7, content8


# 定义标题
def get_title(data):
    data1 = data[0]
    # print(data1)
    data2 = data[1]
    data3 = data[2]
    data4 = data[3]
    data5 = data[4]
    data6 = data[5]
    data7 = data[6]
    data8 = data[7]
    title0 = parse.quote(data1[0])
    title1 = parse.quote(data2[0])
    title2 = parse.quote(data3[0])
    title3 = parse.quote(data4[0])
    title4 = parse.quote(data5[0])
    title5 = parse.quote(data6[0])
    title6 = parse.quote(data7[0])
    title7 = parse.quote(data8[0])
    return title0, title1, title2, title3, title4, title5, title6, title7


# 获取封面图片
def get_img0(cookie, tooken, img_link_list):
    data = img_link_list[0][-1]
    url = "https://mp.weixin.qq.com/cgi-bin/cropimage"

    querystring = {"action": "crop_multi"}

    payload = "token={}&lang=zh_CN&f=json&ajax=1&random=0.6124013898625773&imgurl={}&size_count=2&size0_x1=0&size0_y1=0.048672566371681415&size0_x2=1&size0_y2=0.3518169836189041&size1_x1=0&size1_y1=0.14601769911504425&size1_x2=1&size1_y2=0.8584070796460177".format(
        tooken, data)
    headers = {
        'origin': "https://mp.weixin.qq.com",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'x-requested-with': "XMLHttpRequest",
        'Cookie': cookie,
        'pragma': "no-cache",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'cache-control': "no-cache,no-cache",
        'authority': "mp.weixin.qq.com",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN".format(
            tooken),
        'Postman-Token': "ad75b643-3437-4e1e-890f-93c7b4b21289"
    }
    while True:
        requests.packages.urllib3.disable_warnings()
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False).json()
        # response = json.loads(response)
        # print(response)
        err_msg = response['base_resp']['err_msg']
        # print(err_msg)
        if err_msg == 'ok':
            break
        else:
            print('获取封面图片失败')
    result = response['result']
    cdn_url = result[1]["cdnurl"]
    cdn_url = parse.quote(cdn_url)
    cdn_235_1_url = result[1]["cdnurl"]
    cdn_235_1_url = parse.quote(cdn_235_1_url)
    cdn_1_1_url = result[0]["cdnurl"]
    cdn_1_1_url = parse.quote(cdn_1_1_url)
    cdn_url_back = data  # 原图链接
    cdn_url_back = parse.quote(cdn_url_back)
    return cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back
def get_img1(cookie, tooken, img_link_list):
    data = img_link_list[1][-1]
    url = "https://mp.weixin.qq.com/cgi-bin/cropimage"

    querystring = {"action": "crop_multi"}

    payload = "token={}&lang=zh_CN&f=json&ajax=1&random=0.6124013898625773&imgurl={}&size_count=2&size0_x1=0&size0_y1=0.048672566371681415&size0_x2=1&size0_y2=0.3518169836189041&size1_x1=0&size1_y1=0.14601769911504425&size1_x2=1&size1_y2=0.8584070796460177".format(
        tooken, data)
    headers = {
        'origin': "https://mp.weixin.qq.com",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'x-requested-with': "XMLHttpRequest",
        'Cookie': cookie,
        'pragma': "no-cache",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'cache-control': "no-cache,no-cache",
        'authority': "mp.weixin.qq.com",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN".format(
            tooken),
        'Postman-Token': "ad75b643-3437-4e1e-890f-93c7b4b21289"
    }
    while True:
        requests.packages.urllib3.disable_warnings()
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False).json()
        # response = json.loads(response)
        # print(response)
        err_msg = response['base_resp']['err_msg']
        # print(err_msg)
        if err_msg == 'ok':
            break
        else:
            print('获取封面图片失败')

    result = response['result']
    cdn_url = result[1]["cdnurl"]
    cdn_url = parse.quote(cdn_url)
    cdn_235_1_url = result[1]["cdnurl"]
    cdn_235_1_url = parse.quote(cdn_235_1_url)
    cdn_1_1_url = result[0]["cdnurl"]
    cdn_1_1_url = parse.quote(cdn_1_1_url)
    cdn_url_back = data  # 原图链接
    cdn_url_back = parse.quote(cdn_url_back)
    return cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back
def get_img2(cookie, tooken, img_link_list):
    data = img_link_list[2][-1]
    url = "https://mp.weixin.qq.com/cgi-bin/cropimage"

    querystring = {"action": "crop_multi"}

    payload = "token={}&lang=zh_CN&f=json&ajax=1&random=0.6124013898625773&imgurl={}&size_count=2&size0_x1=0&size0_y1=0.048672566371681415&size0_x2=1&size0_y2=0.3518169836189041&size1_x1=0&size1_y1=0.14601769911504425&size1_x2=1&size1_y2=0.8584070796460177".format(
        tooken, data)
    headers = {
        'origin': "https://mp.weixin.qq.com",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'x-requested-with': "XMLHttpRequest",
        'Cookie': cookie,
        'pragma': "no-cache",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'cache-control': "no-cache,no-cache",
        'authority': "mp.weixin.qq.com",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN".format(
            tooken),
        'Postman-Token': "ad75b643-3437-4e1e-890f-93c7b4b21289"
    }
    while True:
        requests.packages.urllib3.disable_warnings()
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False).json()
        # response = json.loads(response)
        # print(response)
        err_msg = response['base_resp']['err_msg']
        # print(err_msg)
        if err_msg == 'ok':
            break
        else:
            print('获取封面图片失败')
    result = response['result']
    cdn_url = result[1]["cdnurl"]
    cdn_url = parse.quote(cdn_url)
    cdn_235_1_url = result[1]["cdnurl"]
    cdn_235_1_url = parse.quote(cdn_235_1_url)
    cdn_1_1_url = result[0]["cdnurl"]
    cdn_1_1_url = parse.quote(cdn_1_1_url)
    cdn_url_back = data  # 原图链接
    cdn_url_back = parse.quote(cdn_url_back)
    return cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back

def get_img3(cookie, tooken, img_link_list):
    data = img_link_list[3][-1]
    url = "https://mp.weixin.qq.com/cgi-bin/cropimage"

    querystring = {"action": "crop_multi"}

    payload = "token={}&lang=zh_CN&f=json&ajax=1&random=0.6124013898625773&imgurl={}&size_count=2&size0_x1=0&size0_y1=0.048672566371681415&size0_x2=1&size0_y2=0.3518169836189041&size1_x1=0&size1_y1=0.14601769911504425&size1_x2=1&size1_y2=0.8584070796460177".format(
        tooken, data)
    headers = {
        'origin': "https://mp.weixin.qq.com",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'x-requested-with': "XMLHttpRequest",
        'Cookie': cookie,
        'pragma': "no-cache",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'cache-control': "no-cache,no-cache",
        'authority': "mp.weixin.qq.com",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN".format(
            tooken),
        'Postman-Token': "ad75b643-3437-4e1e-890f-93c7b4b21289"
    }
    while True:
        requests.packages.urllib3.disable_warnings()
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False).json()
        # response = json.loads(response)
        # print(response)
        err_msg = response['base_resp']['err_msg']
        # print(err_msg)
        if err_msg == 'ok':
            break
        else:
            print('获取封面图片失败')

    result = response['result']
    cdn_url = result[1]["cdnurl"]
    cdn_url = parse.quote(cdn_url)
    cdn_235_1_url = result[1]["cdnurl"]
    cdn_235_1_url = parse.quote(cdn_235_1_url)
    cdn_1_1_url = result[0]["cdnurl"]
    cdn_1_1_url = parse.quote(cdn_1_1_url)
    cdn_url_back = data  # 原图链接
    cdn_url_back = parse.quote(cdn_url_back)
    return cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back
def get_img4(cookie, tooken, img_link_list):
    data = img_link_list[4][-1]
    url = "https://mp.weixin.qq.com/cgi-bin/cropimage"

    querystring = {"action": "crop_multi"}

    payload = "token={}&lang=zh_CN&f=json&ajax=1&random=0.6124013898625773&imgurl={}&size_count=2&size0_x1=0&size0_y1=0.048672566371681415&size0_x2=1&size0_y2=0.3518169836189041&size1_x1=0&size1_y1=0.14601769911504425&size1_x2=1&size1_y2=0.8584070796460177".format(
        tooken, data)
    headers = {
        'origin': "https://mp.weixin.qq.com",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'x-requested-with': "XMLHttpRequest",
        'Cookie': cookie,
        'pragma': "no-cache",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'cache-control': "no-cache,no-cache",
        'authority': "mp.weixin.qq.com",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN".format(
            tooken),
        'Postman-Token': "ad75b643-3437-4e1e-890f-93c7b4b21289"
    }
    while True:
        requests.packages.urllib3.disable_warnings()
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False).json()
        # response = json.loads(response)
        # print(response)
        err_msg = response['base_resp']['err_msg']
        # print(err_msg)
        if err_msg == 'ok':
            break
        else:
            print('获取封面图片失败')

    result = response['result']
    cdn_url = result[1]["cdnurl"]
    cdn_url = parse.quote(cdn_url)
    cdn_235_1_url = result[1]["cdnurl"]
    cdn_235_1_url = parse.quote(cdn_235_1_url)
    cdn_1_1_url = result[0]["cdnurl"]
    cdn_1_1_url = parse.quote(cdn_1_1_url)
    cdn_url_back = data  # 原图链接
    cdn_url_back = parse.quote(cdn_url_back)
    return cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back

def get_img5(cookie, tooken, img_link_list):
    data = img_link_list[5][-1]
    url = "https://mp.weixin.qq.com/cgi-bin/cropimage"

    querystring = {"action": "crop_multi"}

    payload = "token={}&lang=zh_CN&f=json&ajax=1&random=0.6124013898625773&imgurl={}&size_count=2&size0_x1=0&size0_y1=0.048672566371681415&size0_x2=1&size0_y2=0.3518169836189041&size1_x1=0&size1_y1=0.14601769911504425&size1_x2=1&size1_y2=0.8584070796460177".format(
        tooken, data)
    headers = {
        'origin': "https://mp.weixin.qq.com",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'x-requested-with': "XMLHttpRequest",
        'Cookie': cookie,
        'pragma': "no-cache",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'cache-control': "no-cache,no-cache",
        'authority': "mp.weixin.qq.com",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN".format(
            tooken),
        'Postman-Token': "ad75b643-3437-4e1e-890f-93c7b4b21289"
    }
    while True:
        requests.packages.urllib3.disable_warnings()
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False).json()
        # response = json.loads(response)
        # print(response)
        err_msg = response['base_resp']['err_msg']
        # print(err_msg)
        if err_msg == 'ok':
            break
        else:
            print('获取封面图片失败')

    result = response['result']
    cdn_url = result[1]["cdnurl"]
    cdn_url = parse.quote(cdn_url)
    cdn_235_1_url = result[1]["cdnurl"]
    cdn_235_1_url = parse.quote(cdn_235_1_url)
    cdn_1_1_url = result[0]["cdnurl"]
    cdn_1_1_url = parse.quote(cdn_1_1_url)
    cdn_url_back = data  # 原图链接
    cdn_url_back = parse.quote(cdn_url_back)
    return cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back


def get_img6(cookie, tooken, img_link_list):
    data = img_link_list[6][-1]
    url = "https://mp.weixin.qq.com/cgi-bin/cropimage"

    querystring = {"action": "crop_multi"}

    payload = "token={}&lang=zh_CN&f=json&ajax=1&random=0.6124013898625773&imgurl={}&size_count=2&size0_x1=0&size0_y1=0.048672566371681415&size0_x2=1&size0_y2=0.3518169836189041&size1_x1=0&size1_y1=0.14601769911504425&size1_x2=1&size1_y2=0.8584070796460177".format(
        tooken, data)
    headers = {
        'origin': "https://mp.weixin.qq.com",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'x-requested-with': "XMLHttpRequest",
        'Cookie': cookie,
        'pragma': "no-cache",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'cache-control': "no-cache,no-cache",
        'authority': "mp.weixin.qq.com",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN".format(
            tooken),
        'Postman-Token': "ad75b643-3437-4e1e-890f-93c7b4b21289"
    }
    while True:
        requests.packages.urllib3.disable_warnings()
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False).json()
        # response = json.loads(response)
        # print(response)
        err_msg = response['base_resp']['err_msg']
        # print(err_msg)
        if err_msg == 'ok':
            break
        else:
            print('获取封面图片失败')

    result = response['result']
    cdn_url = result[1]["cdnurl"]
    cdn_url = parse.quote(cdn_url)
    cdn_235_1_url = result[1]["cdnurl"]
    cdn_235_1_url = parse.quote(cdn_235_1_url)
    cdn_1_1_url = result[0]["cdnurl"]
    cdn_1_1_url = parse.quote(cdn_1_1_url)
    cdn_url_back = data  # 原图链接
    cdn_url_back = parse.quote(cdn_url_back)
    return cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back

def get_img7(cookie, tooken, img_link_list):
    data = img_link_list[7][-1]
    url = "https://mp.weixin.qq.com/cgi-bin/cropimage"

    querystring = {"action": "crop_multi"}

    payload = "token={}&lang=zh_CN&f=json&ajax=1&random=0.6124013898625773&imgurl={}&size_count=2&size0_x1=0&size0_y1=0.048672566371681415&size0_x2=1&size0_y2=0.3518169836189041&size1_x1=0&size1_y1=0.14601769911504425&size1_x2=1&size1_y2=0.8584070796460177".format(
        tooken, data)
    headers = {
        'origin': "https://mp.weixin.qq.com",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'x-requested-with': "XMLHttpRequest",
        'Cookie': cookie,
        'pragma': "no-cache",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'cache-control': "no-cache,no-cache",
        'authority': "mp.weixin.qq.com",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN".format(
            tooken),
        'Postman-Token': "ad75b643-3437-4e1e-890f-93c7b4b21289"
    }
    while True:
        requests.packages.urllib3.disable_warnings()
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False).json()
        # response = json.loads(response)
        # print(response)
        err_msg = response['base_resp']['err_msg']
        # print(err_msg)
        if err_msg == 'ok':
            break
        else:
            print('获取封面图片失败')

    result = response['result']
    cdn_url = result[1]["cdnurl"]
    cdn_url = parse.quote(cdn_url)
    cdn_235_1_url = result[1]["cdnurl"]
    cdn_235_1_url = parse.quote(cdn_235_1_url)
    cdn_1_1_url = result[0]["cdnurl"]
    cdn_1_1_url = parse.quote(cdn_1_1_url)
    cdn_url_back = data  # 原图链接
    cdn_url_back = parse.quote(cdn_url_back)
    return cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back


'''定义第一篇'''


def get_data1(cookie, tooken, content, user, title, img0):
    content = content[0]
    url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg"
    querystring = {"t": "ajax-response", "sub": "create", "type": "10", "token": tooken, "lang": "zh_CN"}
    # 定义标题
    title0 = title[0]
    # 定义作者
    author = user[1]
    author = parse.quote(author)
    # 关键词字段
    digest = ''
    ori_white_list = '%7b%22white_list%22%3a%5b%5d%7d'
    imageinfo = '%7B%22list%22%3A%5B%5D%7D'
    dot = '%7B%7D'
    section = ''
    compose_info = ''
    '''设置封面需要cdn_url0，cdn_235_1_url0，cdn_1_1_url0，cdn_url_back0，crop_list0字段'''
    cdn_url = img0[0]

    cdn_235_1_url = img0[1]

    cdn_1_1_url = img0[2]

    cdn_url_back = img0[3]

    payload = '''token={}&lang=zh_CN&f=json&ajax=1&random=0.5574217720351184&AppMsgId=&count=1&data_seq=0&operate_from=Chrome&isnew=0&ad_video_transition0=&can_reward0=0&related_video0=&is_video_recommend0=-1&title0='''.format(
        tooken)
    pay2 = '''{}&author0={}&writerid0=0&fileid0=&digest0={}&auto_gen_digest0=1&content0={}&sourceurl0=&need_open_comment0=0&only_fans_can_comment0=0&cdn_url0={}&cdn_235_1_url0={}&cdn_1_1_url0={}&cdn_url_back0={}&crop_list0=&music_id0=&video_id0=&voteid0=&voteismlt0=&supervoteid0=&cardid0=&cardquantity0=&cardlimit0=&vid_type0=&show_cover_pic0=0&shortvideofileid0=&copyright_type0=0&releasefirst0=&platform0=&reprint_permit_type0=&allow_reprint0=0&allow_reprint_modify0=0&original_article_type0=&ori_white_list0=%7b%22white_list%22%3a%5b%5d%7d&free_content0=&fee0=0&ad_id0=&guide_words0=&is_share_copyright0=0&share_copyright_url0=&source_article_type0=&reprint_recommend_title0=&reprint_recommend_content0=&share_page_type0=0&share_imageinfo0={}&share_video_id0=&dot0={}&share_voice_id0=&insert_ad_mode0=&categories_list0=%5B%5D&sections0={}&compose_info0={}'''.format(
        title0, author, digest, content, cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back,
        imageinfo, dot, section,
        compose_info)
    pay4 = payload + pay2
    headers = {
        'Host': "mp.weixin.qq.com",
        'Cookie': cookie,
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "https://mp.weixin.qq.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=1219935374&lang=zh_CN",
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache"
    }
    requests.packages.urllib3.disable_warnings()

    response = requests.request("POST", url, data=pay4, headers=headers, params=querystring, verify=False).json()

    return response


'''第二篇'''


def get_data2(cookie, tooken, content, user, appid1, title, img0, img1):
    appmsgid = appid1['appMsgId']
    data_seq = appid1["data_seq"]
    content1 = content[0]
    content2 = content[1]
    url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg"
    querystring = {"t": "ajax-response", "sub": "update", "type": "10", "token": tooken, "lang": "zh_CN"}
    title0 = title[0]
    # 定义作者
    author = user[1]
    author = parse.quote(author)
    # 定义关键词
    digest = ''
    # 定义内容
    imageinfo = '%7B%22list%22%3A%5B%5D%7D'
    dot = '%7B%7D'
    title1 = title[1]

    # 定义作者
    author1 = user[1]
    author1 = parse.quote(author1)

    # 定义关键词
    # 定义section
    section = ''
    compose_info = ''
    '''设置封面'''
    cdn_url = img0[0]

    cdn_235_1_url = img0[1]

    cdn_1_1_url = img0[2]

    cdn_url_back = img0[3]
    # 第二篇
    cdn_url1 = img1[0]

    cdn_235_1_url1 = img1[1]  # 载入时的截图

    cdn_1_1_url1 = img1[2]  # a  截取后的图片

    cdn_url_back1 = img1[3]  # 原图链接
    # cdn_url_back1 = parse.quote(cdn_url_back1)

    payload = '''token={}&lang=zh_CN&f=json&ajax=1&random=0.3115025122492028&AppMsgId={}&count=2&data_seq={}&operate_from=Chrome&isnew=0&ad_video_transition0=&can_reward0=0&related_video0=&is_video_recommend0=-1&title0='''.format(
        tooken, appmsgid, data_seq)
    pay2 = '''{}&author0={}&writerid0=0&fileid0=&digest0={}&auto_gen_digest0=1&content0={}&sourceurl0=&need_open_comment0=0&only_fans_can_comment0=0&cdn_url0={}&cdn_235_1_url0={}&cdn_1_1_url0={}&cdn_url_back0={}&crop_list0=&music_id0=&video_id0=&voteid0=&voteismlt0=&supervoteid0=&cardid0=&cardquantity0=&cardlimit0=&vid_type0=&show_cover_pic0=0&shortvideofileid0=&copyright_type0=0&releasefirst0=&platform0=&reprint_permit_type0=&allow_reprint0=0&allow_reprint_modify0=0&original_article_type0=&ori_white_list0=%7b%22white_list%22%3a%5b%5d%7d&free_content0=&fee0=0&ad_id0=&guide_words0=&is_share_copyright0=0&share_copyright_url0=&source_article_type0=&reprint_recommend_title0=&reprint_recommend_content0=&share_page_type0=0&share_imageinfo0={}&share_video_id0=&dot0={}&share_voice_id0=&insert_ad_mode0=&categories_list0=%5B%5D&sections0={}&compose_info0={}'''.format(
        title0, author, digest, content1, cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back,
        imageinfo, dot, section,
        compose_info)
    pay3 = '''&ad_video_transition1=&can_reward1=0&related_video1=&is_video_recommend1=-1&title1={}&author1={}&writerid1=0&fileid1=&digest1={}&auto_gen_digest1=1&content1={}&sourceurl1=&need_open_comment1=0&only_fans_can_comment1=0&cdn_url1={}&cdn_235_1_url1={}&cdn_1_1_url1={}&cdn_url_back1={}&crop_list1=&music_id1=&video_id1=&voteid1=&voteismlt1=&supervoteid1=&cardid1=&cardquantity1=&cardlimit1=&vid_type1=&show_cover_pic1=0&shortvideofileid1=&copyright_type1=0&releasefirst1=&platform1=&reprint_permit_type1=&allow_reprint1=0&allow_reprint_modify1=0&original_article_type1=&ori_white_list1=%7b%22white_list%22%3a%5b%5d%7d&free_content1=&fee1=0&ad_id1=&guide_words1=&is_share_copyright1=0&share_copyright_url1=&source_article_type1=&reprint_recommend_title1=&reprint_recommend_content1=&share_page_type1=0&share_imageinfo1={}&share_video_id1=&dot1={}&share_voice_id1=&insert_ad_mode1=&categories_list1=[]&sections1={}&compose_info1={}'''.format(
        title1, author1, digest, content2, cdn_url1, cdn_235_1_url1, cdn_1_1_url1, cdn_url_back1,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = payload + pay2 + pay3
    headers = {
        'Host': "mp.weixin.qq.com",
        'Cookie': cookie,
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "https://mp.weixin.qq.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&appmsgid={}&token={}&lang=zh_CN".format(
            appmsgid, tooken),
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache"
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=pay4, headers=headers, params=querystring, verify=False).json()

    return response


# 第三篇
def get_data3(cookie, tooken, content, user, appid2, title, img0, img1, img2):
    appmsgid = appid2['appMsgId']
    data_seq = appid2["data_seq"]
    content0 = content[0]
    content1 = content[1]
    content2 = content[2]
    url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg"
    querystring = {"t": "ajax-response", "sub": "update", "type": "10", "token": tooken, "lang": "zh_CN"}
    title0 = title[0]
    # 定义作者
    author = user[1]
    author = parse.quote(author)
    # 定义关键词
    digest = ''
    # 定义内容
    imageinfo = '%7B%22list%22%3A%5B%5D%7D'
    dot = '%7B%7D'
    # 定义section
    section = ''
    compose_info = ''

    title1 = title[1]
    # 定义作者
    author1 = user[1]
    author1 = parse.quote(author1)
    # 定义关键词
    # 定义内容

    title2 = title[2]
    # 定义作者
    author2 = user[1]
    author2 = parse.quote(author2)
    # 定义关键词
    # 定义内容
    '''设置封面'''
    cdn_url = img0[0]  # 载入时的截图
    # cdn_url = parse.quote(cdn_url)

    cdn_235_1_url = img0[1]  # 载入时的截图
    # cdn_235_1_url = parse.quote(cdn_235_1_url)

    cdn_1_1_url = img0[2]  # a  截取后的图片
    # cdn_1_1_url = parse.quote(cdn_1_1_url)

    cdn_url_back = img0[3]  # 原图链接
    # cdn_url_back = parse.quote(cdn_url_back)
    # 第二篇
    cdn_url1 = img1[0]  # 载入时的截图
    # cdn_url1 = parse.quote(cdn_url1)

    cdn_235_1_url1 = img1[1]  # 载入时的截图
    # cdn_235_1_url1 = parse.quote(cdn_235_1_url1)

    cdn_1_1_url1 = img1[2]  # a  截取后的图片

    cdn_url_back1 = img1[3]  # 原图链接

    # 第三篇
    cdn_url2 = img2[0]  # 载入时的截图
    # cdn_url2 = parse.quote(cdn_url2)

    cdn_235_1_url2 = img2[1]  # 载入时的截图
    # cdn_235_1_url2 = parse.quote(cdn_235_1_url2)

    cdn_1_1_url2 = img2[2]  # a  截取后的图片
    # cdn_1_1_url2 = parse.quote(cdn_1_1_url2)

    cdn_url_back2 = img2[3]  # 原图链接
    # cdn_url_back2 = parse.quote(cdn_url_back2)
    payload = '''token={}&lang=zh_CN&f=json&ajax=1&random=0.5574217720351184&AppMsgId={}&count=3&data_seq={}&operate_from=Chrome&isnew=0&ad_video_transition0=&can_reward0=0&related_video0=&is_video_recommend0=-1&title0='''.format(
        tooken, appmsgid, data_seq)
    pay2 = '''{}&author0={}&writerid0=0&fileid0=&digest0={}&auto_gen_digest0=1&content0={}&sourceurl0=&need_open_comment0=0&only_fans_can_comment0=0&cdn_url0={}&cdn_235_1_url0={}&cdn_1_1_url0={}&cdn_url_back0={}&crop_list0=&music_id0=&video_id0=&voteid0=&voteismlt0=&supervoteid0=&cardid0=&cardquantity0=&cardlimit0=&vid_type0=&show_cover_pic0=0&shortvideofileid0=&copyright_type0=0&releasefirst0=&platform0=&reprint_permit_type0=&allow_reprint0=0&allow_reprint_modify0=0&original_article_type0=&ori_white_list0=%7b%22white_list%22%3a%5b%5d%7d&free_content0=&fee0=0&ad_id0=&guide_words0=&is_share_copyright0=0&share_copyright_url0=&source_article_type0=&reprint_recommend_title0=&reprint_recommend_content0=&share_page_type0=0&share_imageinfo0={}&share_video_id0=&dot0={}&share_voice_id0=&insert_ad_mode0=&categories_list0=%5B%5D&sections0={}&compose_info0={}'''.format(
        title0, author, digest, content0, cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back,
        imageinfo, dot, section,
        compose_info)
    pay3 = '''&ad_video_transition1=&can_reward1=0&related_video1=&is_video_recommend1=-1&title1={}&author1={}&writerid1=0&fileid1=&digest1={}&auto_gen_digest1=1&content1={}&sourceurl1=&need_open_comment1=0&only_fans_can_comment1=0&cdn_url1={}&cdn_235_1_url1={}&cdn_1_1_url1={}&cdn_url_back1={}&crop_list1=&music_id1=&video_id1=&voteid1=&voteismlt1=&supervoteid1=&cardid1=&cardquantity1=&cardlimit1=&vid_type1=&show_cover_pic1=0&shortvideofileid1=&copyright_type1=0&releasefirst1=&platform1=&reprint_permit_type1=&allow_reprint1=0&allow_reprint_modify1=0&original_article_type1=&ori_white_list1=%7b%22white_list%22%3a%5b%5d%7d&free_content1=&fee1=0&ad_id1=&guide_words1=&is_share_copyright1=0&share_copyright_url1=&source_article_type1=&reprint_recommend_title1=&reprint_recommend_content1=&share_page_type1=0&share_imageinfo1={}&share_video_id1=&dot1={}&share_voice_id1=&insert_ad_mode1=&categories_list1=[]&sections1={}&compose_info1={}'''.format(
        title1, author1, digest, content1, cdn_url1, cdn_235_1_url1, cdn_1_1_url1, cdn_url_back1,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = '''&ad_video_transition2=&can_reward2=0&related_video2=&is_video_recommend2=-1&title2={}&author2={}&writerid2=0&fileid2=&digest2={}&auto_gen_digest2=1&content2={}&sourceurl2=&need_open_comment2=0&only_fans_can_comment2=0&cdn_url2={}&cdn_235_1_url2={}&cdn_1_1_url2={}&cdn_url_back2={}&crop_list2=&music_id2=&video_id2=&voteid2=&voteismlt2=&supervoteid2=&cardid2=&cardquantity2=&cardlimit2=&vid_type2=&show_cover_pic2=0&shortvideofileid2=&copyright_type2=0&releasefirst2=&platform2=&reprint_permit_type2=&allow_reprint2=0&allow_reprint_modify2=0&original_article_type2=&ori_white_list2=%7b%22white_list%22%3a%5b%5d%7d&free_content2=&fee2=0&ad_id2=&guide_words2=&is_share_copyright2=0&share_copyright_url2=&source_article_type2=&reprint_recommend_title2=&reprint_recommend_content2=&share_page_type2=0&share_imageinfo2={}&share_video_id2=&dot2={}&share_voice_id2=&insert_ad_mode2=&categories_list2=[]&sections2={}&compose_info2={}'''.format(
        title2, author2, digest, content2, cdn_url2, cdn_235_1_url2, cdn_1_1_url2, cdn_url_back2,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = payload + pay2 + pay3 + pay4
    headers = {
        'Host': "mp.weixin.qq.com",
        'Cookie': cookie,
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "https://mp.weixin.qq.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&appmsgid={}&token={}&lang=zh_CN".format(
            appmsgid, tooken),
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache"
    }

    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=pay4, headers=headers, params=querystring, verify=False).json()

    return response


# 定义第四篇
def get_data4(cookie, tooken, content, user, appid3, title, img0, img1, img2, img3):
    i = user
    appmsgid = appid3['appMsgId']
    data_seq = appid3["data_seq"]
    content0 = content[0]
    content1 = content[1]
    content2 = content[2]
    content3 = content[3]
    url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg"

    querystring = {"t": "ajax-response", "sub": "update", "type": "10", "token": tooken, "lang": "zh_CN"}

    title0 = title[0]
    # 定义作者
    author = i[1]
    author = parse.quote(author)
    # 定义关键词
    digest = ''
    # 定义内容
    imageinfo = '%7B%22list%22%3A%5B%5D%7D'
    dot = '%7B%7D'
    # 定义section
    section = ''
    compose_info = ''

    title1 = title[1]
    # 定义作者
    author1 = i[1]
    author1 = parse.quote(author1)
    # 定义关键词
    # 定义内容

    title2 = title[2]
    # 定义作者
    author2 = i[1]
    author2 = parse.quote(author2)
    # 定义关键词
    # 定义内容

    title3 = title[3]
    # 定义作者
    author3 = i[1]
    author3 = parse.quote(author3)
    # 定义关键词
    # 定义内容
    '''设置封面'''
    cdn_url = img0[0]  # 载入时的截图
    # cdn_url = parse.quote(cdn_url)

    cdn_235_1_url = img0[1]  # 载入时的截图
    # cdn_235_1_url = parse.quote(cdn_235_1_url)

    cdn_1_1_url = img0[2]  # a  截取后的图片
    # cdn_1_1_url = parse.quote(cdn_1_1_url)

    cdn_url_back = img0[3]  # 原图链接
    # cdn_url_back = parse.quote(cdn_url_back)
    # 第二篇
    cdn_url1 = img1[0]  # 载入时的截图
    # cdn_url1 = parse.quote(cdn_url1)

    cdn_235_1_url1 = img1[1]  # 载入时的截图
    # cdn_235_1_url1 = parse.quote(cdn_235_1_url1)

    cdn_1_1_url1 = img1[2]  # a  截取后的图片
    # cdn_1_1_url1 = parse.quote(cdn_1_1_url1)

    cdn_url_back1 = img1[3]  # 原图链接
    # cdn_url_back1 = parse.quote(cdn_url_back1)

    # 第三篇
    cdn_url2 = img2[0]  # 载入时的截图
    # cdn_url2 = parse.quote(cdn_url2)

    cdn_235_1_url2 = img2[1]  # 载入时的截图
    # cdn_235_1_url2 = parse.quote(cdn_235_1_url2)

    cdn_1_1_url2 = img2[2]  # a  截取后的图片
    # cdn_1_1_url2 = parse.quote(cdn_1_1_url2)

    cdn_url_back2 = img2[3]  # 原图链接
    # cdn_url_back2 = parse.quote(cdn_url_back2)

    # 第四篇
    cdn_url3 = img3[0]  # 载入时的截图
    # cdn_url3 = parse.quote(cdn_url3)

    cdn_235_1_url3 = img3[1]  # 载入时的截图
    # cdn_235_1_url3 = parse.quote(cdn_235_1_url3)

    cdn_1_1_url3 = img3[2]  # a  截取后的图片
    # cdn_1_1_url3 = parse.quote(cdn_1_1_url3)

    cdn_url_back3 = img3[3]  # 原图链接
    # cdn_url_back3 = parse.quote(cdn_url_back3)
    payload = '''token={}&lang=zh_CN&f=json&ajax=1&random=0.5574217720351184&AppMsgId={}&count=4&data_seq={}&operate_from=Chrome&isnew=0&ad_video_transition0=&can_reward0=0&related_video0=&is_video_recommend0=-1&title0='''.format(
        tooken, appmsgid, data_seq)
    pay2 = '''{}&author0={}&writerid0=0&fileid0=&digest0={}&auto_gen_digest0=1&content0={}&sourceurl0=&need_open_comment0=0&only_fans_can_comment0=0&cdn_url0={}&cdn_235_1_url0={}&cdn_1_1_url0={}&cdn_url_back0={}&crop_list0=&music_id0=&video_id0=&voteid0=&voteismlt0=&supervoteid0=&cardid0=&cardquantity0=&cardlimit0=&vid_type0=&show_cover_pic0=0&shortvideofileid0=&copyright_type0=0&releasefirst0=&platform0=&reprint_permit_type0=&allow_reprint0=0&allow_reprint_modify0=0&original_article_type0=&ori_white_list0=%7b%22white_list%22%3a%5b%5d%7d&free_content0=&fee0=0&ad_id0=&guide_words0=&is_share_copyright0=0&share_copyright_url0=&source_article_type0=&reprint_recommend_title0=&reprint_recommend_content0=&share_page_type0=0&share_imageinfo0={}&share_video_id0=&dot0={}&share_voice_id0=&insert_ad_mode0=&categories_list0=%5B%5D&sections0={}&compose_info0={}'''.format(
        title0, author, digest, content0, cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back,
        imageinfo, dot, section,
        compose_info)
    pay3 = '''&ad_video_transition1=&can_reward1=0&related_video1=&is_video_recommend1=-1&title1={}&author1={}&writerid1=0&fileid1=&digest1={}&auto_gen_digest1=1&content1={}&sourceurl1=&need_open_comment1=0&only_fans_can_comment1=0&cdn_url1={}&cdn_235_1_url1={}&cdn_1_1_url1={}&cdn_url_back1={}&crop_list1=&music_id1=&video_id1=&voteid1=&voteismlt1=&supervoteid1=&cardid1=&cardquantity1=&cardlimit1=&vid_type1=&show_cover_pic1=0&shortvideofileid1=&copyright_type1=0&releasefirst1=&platform1=&reprint_permit_type1=&allow_reprint1=0&allow_reprint_modify1=0&original_article_type1=&ori_white_list1=%7b%22white_list%22%3a%5b%5d%7d&free_content1=&fee1=0&ad_id1=&guide_words1=&is_share_copyright1=0&share_copyright_url1=&source_article_type1=&reprint_recommend_title1=&reprint_recommend_content1=&share_page_type1=0&share_imageinfo1={}&share_video_id1=&dot1={}&share_voice_id1=&insert_ad_mode1=&categories_list1=[]&sections1={}&compose_info1={}'''.format(
        title1, author1, digest, content1, cdn_url1, cdn_235_1_url1, cdn_1_1_url1, cdn_url_back1,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = '''&ad_video_transition2=&can_reward2=0&related_video2=&is_video_recommend2=-1&title2={}&author2={}&writerid2=0&fileid2=&digest2={}&auto_gen_digest2=1&content2={}&sourceurl2=&need_open_comment2=0&only_fans_can_comment2=0&cdn_url2={}&cdn_235_1_url2={}&cdn_1_1_url2={}&cdn_url_back2={}&crop_list2=&music_id2=&video_id2=&voteid2=&voteismlt2=&supervoteid2=&cardid2=&cardquantity2=&cardlimit2=&vid_type2=&show_cover_pic2=0&shortvideofileid2=&copyright_type2=0&releasefirst2=&platform2=&reprint_permit_type2=&allow_reprint2=0&allow_reprint_modify2=0&original_article_type2=&ori_white_list2=%7b%22white_list%22%3a%5b%5d%7d&free_content2=&fee2=0&ad_id2=&guide_words2=&is_share_copyright2=0&share_copyright_url2=&source_article_type2=&reprint_recommend_title2=&reprint_recommend_content2=&share_page_type2=0&share_imageinfo2={}&share_video_id2=&dot2={}&share_voice_id2=&insert_ad_mode2=&categories_list2=[]&sections2={}&compose_info2={}'''.format(
        title2, author2, digest, content2, cdn_url2, cdn_235_1_url2, cdn_1_1_url2, cdn_url_back2,
        imageinfo, dot,
        section, compose_info
    )
    pay5 = '''&ad_video_transition3=&can_reward3=0&related_video3=&is_video_recommend3=-1&title3={}&author3={}&writerid3=0&fileid3=&digest3={}&auto_gen_digest3=1&content3={}&sourceurl3=&need_open_comment3=0&only_fans_can_comment3=0&cdn_url3={}&cdn_235_1_url3={}&cdn_1_1_url3={}&cdn_url_back3={}&crop_list3=&music_id3=&video_id3=&voteid3=&voteismlt3=&supervoteid3=&cardid3=&cardquantity3=&cardlimit3=&vid_type3=&show_cover_pic3=0&shortvideofileid3=&copyright_type3=0&releasefirst3=&platform3=&reprint_permit_type3=&allow_reprint3=0&allow_reprint_modify3=0&original_article_type3=&ori_white_list3=%7b%22white_list%22%3a%5b%5d%7d&free_content3=&fee3=0&ad_id3=&guide_words3=&is_share_copyright3=0&share_copyright_url3=&source_article_type3=&reprint_recommend_title3=&reprint_recommend_content3=&share_page_type3=0&share_imageinfo3={}&share_video_id3=&dot3={}&share_voice_id3=&insert_ad_mode3=&categories_list3=[]&sections3={}&compose_info3={}'''.format(
        title3, author3, digest, content3, cdn_url3, cdn_235_1_url3, cdn_1_1_url3, cdn_url_back3,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = payload + pay2 + pay3 + pay4 + pay5
    headers = {
        'Host': "mp.weixin.qq.com",
        'Cookie': cookie,
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "https://mp.weixin.qq.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&appmsgid={}&token={}&lang=zh_CN".format(
            appmsgid, tooken),
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache"
    }

    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=pay4, headers=headers, params=querystring, verify=False).json()

    return response


# 定义第五篇
def get_data5(cookie, tooken, content, user, appid4, title, img0, img1, img2, img3, img4):
    i = user
    appmsgid = appid4['appMsgId']
    data_seq = appid4["data_seq"]
    content0 = content[0]
    content1 = content[1]
    content2 = content[2]
    content3 = content[3]
    content4 = content[4]
    url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg"

    querystring = {"t": "ajax-response", "sub": "update", "type": "10", "token": tooken, "lang": "zh_CN"}
    title0 = title[0]
    # 定义作者
    author = i[1]
    author = parse.quote(author)
    # 定义关键词
    digest = ''
    # 定义内容

    imageinfo = '%7B%22list%22%3A%5B%5D%7D'
    dot = '%7B%7D'
    # 定义section
    section = ''
    compose_info = ''

    title1 = title[1]
    # 定义作者
    author1 = i[1]
    author1 = parse.quote(author1)
    # 定义关键词
    # 定义内容

    title2 = title[2]
    # 定义作者
    author2 = i[1]
    author2 = parse.quote(author2)
    # 定义关键词
    # 定义内容

    title3 = title[3]
    # 定义作者
    author3 = i[1]
    author3 = parse.quote(author3)
    # 定义关键词
    # 定义内容

    title4 = title[4]
    # 定义作者
    author4 = i[1]
    author4 = parse.quote(author4)
    # 定义关键词
    # 定义内容
    '''设置封面'''
    cdn_url = img0[0]  # 载入时的截图
    # cdn_url = parse.quote(cdn_url)

    cdn_235_1_url = img0[1]  # 载入时的截图
    # cdn_235_1_url = parse.quote(cdn_235_1_url)

    cdn_1_1_url = img0[2]  # a  截取后的图片
    # cdn_1_1_url = parse.quote(cdn_1_1_url)

    cdn_url_back = img0[3]  # 原图链接
    # cdn_url_back = parse.quote(cdn_url_back)
    # 第二篇
    cdn_url1 = img1[0]  # 载入时的截图
    # cdn_url1 = parse.quote(cdn_url1)

    cdn_235_1_url1 = img1[1]  # 载入时的截图
    # cdn_235_1_url1 = parse.quote(cdn_235_1_url1)

    cdn_1_1_url1 = img1[2]  # a  截取后的图片
    # cdn_1_1_url1 = parse.quote(cdn_1_1_url1)

    cdn_url_back1 = img1[3]  # 原图链接
    # cdn_url_back1 = parse.quote(cdn_url_back1)

    # 第三篇
    cdn_url2 = img2[0]  # 载入时的截图
    # cdn_url2 = parse.quote(cdn_url2)

    cdn_235_1_url2 = img2[1]  # 载入时的截图
    # cdn_235_1_url2 = parse.quote(cdn_235_1_url2)

    cdn_1_1_url2 = img2[2]  # a  截取后的图片
    # cdn_1_1_url2 = parse.quote(cdn_1_1_url2)

    cdn_url_back2 = img2[3]  # 原图链接
    # cdn_url_back2 = parse.quote(cdn_url_back2)

    # 第四篇
    cdn_url3 = img3[0]  # 载入时的截图
    # cdn_url3 = parse.quote(cdn_url3)

    cdn_235_1_url3 = img3[1]  # 载入时的截图
    # cdn_235_1_url3 = parse.quote(cdn_235_1_url3)

    cdn_1_1_url3 = img3[2]  # a  截取后的图片
    # cdn_1_1_url3 = parse.quote(cdn_1_1_url3)

    cdn_url_back3 = img3[3]  # 原图链接

    # 第五篇
    cdn_url4 = img4[0]  # 载入时的截图
    # cdn_url4 = parse.quote(cdn_url4)

    cdn_235_1_url4 = img4[1]  # 载入时的截图
    # cdn_235_1_url4 = parse.quote(cdn_235_1_url4)

    cdn_1_1_url4 = img4[2]  # a  截取后的图片
    # cdn_1_1_url4 = parse.quote(cdn_1_1_url4)

    cdn_url_back4 = img4[3]  # 原图链接
    # cdn_url_back4 = parse.quote(cdn_url_back4)
    payload = '''token={}&lang=zh_CN&f=json&ajax=1&random=0.5574217720351184&AppMsgId={}&count=5&data_seq={}&operate_from=Chrome&isnew=0&ad_video_transition0=&can_reward0=0&related_video0=&is_video_recommend0=-1&title0='''.format(
        tooken, appmsgid, data_seq)
    pay2 = '''{}&author0={}&writerid0=0&fileid0=&digest0={}&auto_gen_digest0=1&content0={}&sourceurl0=&need_open_comment0=0&only_fans_can_comment0=0&cdn_url0={}&cdn_235_1_url0={}&cdn_1_1_url0={}&cdn_url_back0={}&crop_list0=&music_id0=&video_id0=&voteid0=&voteismlt0=&supervoteid0=&cardid0=&cardquantity0=&cardlimit0=&vid_type0=&show_cover_pic0=0&shortvideofileid0=&copyright_type0=0&releasefirst0=&platform0=&reprint_permit_type0=&allow_reprint0=0&allow_reprint_modify0=0&original_article_type0=&ori_white_list0=%7b%22white_list%22%3a%5b%5d%7d&free_content0=&fee0=0&ad_id0=&guide_words0=&is_share_copyright0=0&share_copyright_url0=&source_article_type0=&reprint_recommend_title0=&reprint_recommend_content0=&share_page_type0=0&share_imageinfo0={}&share_video_id0=&dot0={}&share_voice_id0=&insert_ad_mode0=&categories_list0=%5B%5D&sections0={}&compose_info0={}'''.format(
        title0, author, digest, content0, cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back,
        imageinfo, dot, section,
        compose_info)
    pay3 = '''&ad_video_transition1=&can_reward1=0&related_video1=&is_video_recommend1=-1&title1={}&author1={}&writerid1=0&fileid1=&digest1={}&auto_gen_digest1=1&content1={}&sourceurl1=&need_open_comment1=0&only_fans_can_comment1=0&cdn_url1={}&cdn_235_1_url1={}&cdn_1_1_url1={}&cdn_url_back1={}&crop_list1=&music_id1=&video_id1=&voteid1=&voteismlt1=&supervoteid1=&cardid1=&cardquantity1=&cardlimit1=&vid_type1=&show_cover_pic1=0&shortvideofileid1=&copyright_type1=0&releasefirst1=&platform1=&reprint_permit_type1=&allow_reprint1=0&allow_reprint_modify1=0&original_article_type1=&ori_white_list1=%7b%22white_list%22%3a%5b%5d%7d&free_content1=&fee1=0&ad_id1=&guide_words1=&is_share_copyright1=0&share_copyright_url1=&source_article_type1=&reprint_recommend_title1=&reprint_recommend_content1=&share_page_type1=0&share_imageinfo1={}&share_video_id1=&dot1={}&share_voice_id1=&insert_ad_mode1=&categories_list1=[]&sections1={}&compose_info1={}'''.format(
        title1, author1, digest, content1, cdn_url1, cdn_235_1_url1, cdn_1_1_url1, cdn_url_back1,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = '''&ad_video_transition2=&can_reward2=0&related_video2=&is_video_recommend2=-1&title2={}&author2={}&writerid2=0&fileid2=&digest2={}&auto_gen_digest2=1&content2={}&sourceurl2=&need_open_comment2=0&only_fans_can_comment2=0&cdn_url2={}&cdn_235_1_url2={}&cdn_1_1_url2={}&cdn_url_back2={}&crop_list2=&music_id2=&video_id2=&voteid2=&voteismlt2=&supervoteid2=&cardid2=&cardquantity2=&cardlimit2=&vid_type2=&show_cover_pic2=0&shortvideofileid2=&copyright_type2=0&releasefirst2=&platform2=&reprint_permit_type2=&allow_reprint2=0&allow_reprint_modify2=0&original_article_type2=&ori_white_list2=%7b%22white_list%22%3a%5b%5d%7d&free_content2=&fee2=0&ad_id2=&guide_words2=&is_share_copyright2=0&share_copyright_url2=&source_article_type2=&reprint_recommend_title2=&reprint_recommend_content2=&share_page_type2=0&share_imageinfo2={}&share_video_id2=&dot2={}&share_voice_id2=&insert_ad_mode2=&categories_list2=[]&sections2={}&compose_info2={}'''.format(
        title2, author2, digest, content2, cdn_url2, cdn_235_1_url2, cdn_1_1_url2, cdn_url_back2,
        imageinfo, dot,
        section, compose_info
    )
    pay5 = '''&ad_video_transition3=&can_reward3=0&related_video3=&is_video_recommend3=-1&title3={}&author3={}&writerid3=0&fileid3=&digest3={}&auto_gen_digest3=1&content3={}&sourceurl3=&need_open_comment3=0&only_fans_can_comment3=0&cdn_url3={}&cdn_235_1_url3={}&cdn_1_1_url3={}&cdn_url_back3={}&crop_list3=&music_id3=&video_id3=&voteid3=&voteismlt3=&supervoteid3=&cardid3=&cardquantity3=&cardlimit3=&vid_type3=&show_cover_pic3=0&shortvideofileid3=&copyright_type3=0&releasefirst3=&platform3=&reprint_permit_type3=&allow_reprint3=0&allow_reprint_modify3=0&original_article_type3=&ori_white_list3=%7b%22white_list%22%3a%5b%5d%7d&free_content3=&fee3=0&ad_id3=&guide_words3=&is_share_copyright3=0&share_copyright_url3=&source_article_type3=&reprint_recommend_title3=&reprint_recommend_content3=&share_page_type3=0&share_imageinfo3={}&share_video_id3=&dot3={}&share_voice_id3=&insert_ad_mode3=&categories_list3=[]&sections3={}&compose_info3={}'''.format(
        title3, author3, digest, content3, cdn_url3, cdn_235_1_url3, cdn_1_1_url3, cdn_url_back3,
        imageinfo, dot,
        section, compose_info
    )
    pay6 = '''&ad_video_transition4=&can_reward4=0&related_video4=&is_video_recommend4=-1&title4={}&author4={}&writerid4=0&fileid4=&digest4={}&auto_gen_digest4=1&content4={}&sourceurl4=&need_open_comment4=0&only_fans_can_comment4=0&cdn_url4={}&cdn_235_1_url4={}&cdn_1_1_url4={}&cdn_url_back4={}&crop_list4=&music_id4=&video_id4=&voteid4=&voteismlt4=&supervoteid4=&cardid4=&cardquantity4=&cardlimit4=&vid_type4=&show_cover_pic4=0&shortvideofileid4=&copyright_type4=0&releasefirst4=&platform4=&reprint_permit_type4=&allow_reprint4=0&allow_reprint_modify4=0&original_article_type4=&ori_white_list4=%7b%22white_list%22%3a%5b%5d%7d&free_content4=&fee4=0&ad_id4=&guide_words4=&is_share_copyright4=0&share_copyright_url4=&source_article_type4=&reprint_recommend_title4=&reprint_recommend_content4=&share_page_type4=0&share_imageinfo4={}&share_video_id4=&dot4={}&share_voice_id4=&insert_ad_mode4=&categories_list4=[]&sections4={}&compose_info4={}'''.format(
        title4, author4, digest, content4, cdn_url4, cdn_235_1_url4, cdn_1_1_url4, cdn_url_back4,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = payload + pay2 + pay3 + pay4 + pay5 + pay6
    headers = {
        'Host': "mp.weixin.qq.com",
        'Cookie': cookie,
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "https://mp.weixin.qq.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&appmsgid={}&token={}&lang=zh_CN".format(
            appmsgid, tooken),
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache"
    }

    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=pay4, headers=headers, params=querystring, verify=False).json()

    return response


# 第六篇
def get_data6(cookie, tooken, content, user, appid5, title, img0, img1, img2, img3, img4, img5):
    i = user
    appmsgid = appid5['appMsgId']
    data_seq = appid5["data_seq"]
    content0 = content[0]
    content1 = content[1]
    content2 = content[2]
    content3 = content[3]
    content4 = content[4]
    content5 = content[5]
    url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg"

    querystring = {"t": "ajax-response", "sub": "update", "type": "10", "token": tooken, "lang": "zh_CN"}

    title0 = title[0]
    # 定义作者
    author = i[1]
    author = parse.quote(author)
    # 定义关键词
    digest = ''
    # 定义内容
    imageinfo = '%7B%22list%22%3A%5B%5D%7D'
    dot = '%7B%7D'
    # 定义section
    section = ''
    compose_info = ''

    title1 = title[1]
    # 定义作者
    author1 = i[1]
    author1 = parse.quote(author1)
    # 定义关键词
    # 定义内容

    title2 = title[2]
    # 定义作者
    author2 = i[1]
    author2 = parse.quote(author2)
    # 定义关键词
    # 定义内容

    title3 = title[3]
    # 定义作者
    author3 = i[1]
    author3 = parse.quote(author3)
    # 定义关键词
    # 定义内容

    title4 = title[4]
    # 定义作者
    author4 = i[1]
    author4 = parse.quote(author4)
    # 定义关键词
    # 定义内容

    title5 = title[5]
    # 定义作者
    author5 = i[1]
    author5 = parse.quote(author5)
    # 定义关键词
    # 定义内容
    '''设置封面'''
    cdn_url = img0[0]  # 载入时的截图
    # cdn_url = parse.quote(cdn_url)

    cdn_235_1_url = img0[1]  # 载入时的截图
    # cdn_235_1_url = parse.quote(cdn_235_1_url)

    cdn_1_1_url = img0[2]  # a  截取后的图片
    # cdn_1_1_url = parse.quote(cdn_1_1_url)

    cdn_url_back = img0[3]  # 原图链接
    # cdn_url_back = parse.quote(cdn_url_back)
    # 第二篇
    cdn_url1 = img1[0]  # 载入时的截图
    # cdn_url1 = parse.quote(cdn_url1)

    cdn_235_1_url1 = img1[1]  # 载入时的截图
    # cdn_235_1_url1 = parse.quote(cdn_235_1_url1)

    cdn_1_1_url1 = img1[2]  # a  截取后的图片
    # cdn_1_1_url1 = parse.quote(cdn_1_1_url1)

    cdn_url_back1 = img1[3]  # 原图链接
    # cdn_url_back1 = parse.quote(cdn_url_back1)

    # 第三篇
    cdn_url2 = img2[0]  # 载入时的截图
    # cdn_url2 = parse.quote(cdn_url2)

    cdn_235_1_url2 = img2[1]  # 载入时的截图
    # cdn_235_1_url2 = parse.quote(cdn_235_1_url2)

    cdn_1_1_url2 = img2[2]  # a  截取后的图片
    # cdn_1_1_url2 = parse.quote(cdn_1_1_url2)

    cdn_url_back2 = img2[3]  # 原图链接
    # cdn_url_back2 = parse.quote(cdn_url_back2)

    # 第四篇
    cdn_url3 = img3[0]  # 载入时的截图
    # cdn_url3 = parse.quote(cdn_url3)

    cdn_235_1_url3 = img3[1]  # 载入时的截图
    # cdn_235_1_url3 = parse.quote(cdn_235_1_url3)

    cdn_1_1_url3 = img3[2]  # a  截取后的图片
    # cdn_1_1_url3 = parse.quote(cdn_1_1_url3)

    cdn_url_back3 = img3[3]  # 原图链接

    # 第五篇
    cdn_url4 = img4[0]  # 载入时的截图
    # cdn_url4 = parse.quote(cdn_url4)

    cdn_235_1_url4 = img4[1]  # 载入时的截图
    # cdn_235_1_url4 = parse.quote(cdn_235_1_url4)

    cdn_1_1_url4 = img4[2]  # a  截取后的图片
    # cdn_1_1_url4 = parse.quote(cdn_1_1_url4)

    cdn_url_back4 = img4[3]  # 原图链接
    # cdn_url_back4 = parse.quote(cdn_url_back4)

    # 第六篇
    cdn_url5 = img5[0]  # 载入时的截图
    # cdn_url5 = parse.quote(cdn_url5)

    cdn_235_1_url5 = img5[1]  # 载入时的截图
    # cdn_235_1_url5 = parse.quote(cdn_235_1_url5)

    cdn_1_1_url5 = img5[2]  # a  截取后的图片
    # cdn_1_1_url5 = parse.quote(cdn_1_1_url5)

    cdn_url_back5 = img5[3]  # 原图链接
    # cdn_url_back5 = parse.quote(cdn_url_back5)

    payload = '''token={}&lang=zh_CN&f=json&ajax=1&random=0.5574217720351184&AppMsgId={}&count=6&data_seq={}&operate_from=Chrome&isnew=0&ad_video_transition0=&can_reward0=0&related_video0=&is_video_recommend0=-1&title0='''.format(
        tooken, appmsgid, data_seq)
    pay2 = '''{}&author0={}&writerid0=0&fileid0=&digest0={}&auto_gen_digest0=1&content0={}&sourceurl0=&need_open_comment0=0&only_fans_can_comment0=0&cdn_url0={}&cdn_235_1_url0={}&cdn_1_1_url0={}&cdn_url_back0={}&crop_list0=&music_id0=&video_id0=&voteid0=&voteismlt0=&supervoteid0=&cardid0=&cardquantity0=&cardlimit0=&vid_type0=&show_cover_pic0=0&shortvideofileid0=&copyright_type0=0&releasefirst0=&platform0=&reprint_permit_type0=&allow_reprint0=0&allow_reprint_modify0=0&original_article_type0=&ori_white_list0=%7b%22white_list%22%3a%5b%5d%7d&free_content0=&fee0=0&ad_id0=&guide_words0=&is_share_copyright0=0&share_copyright_url0=&source_article_type0=&reprint_recommend_title0=&reprint_recommend_content0=&share_page_type0=0&share_imageinfo0={}&share_video_id0=&dot0={}&share_voice_id0=&insert_ad_mode0=&categories_list0=%5B%5D&sections0={}&compose_info0={}'''.format(
        title0, author, digest, content0, cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back,
        imageinfo, dot, section,
        compose_info)
    pay3 = '''&ad_video_transition1=&can_reward1=0&related_video1=&is_video_recommend1=-1&title1={}&author1={}&writerid1=0&fileid1=&digest1={}&auto_gen_digest1=1&content1={}&sourceurl1=&need_open_comment1=0&only_fans_can_comment1=0&cdn_url1={}&cdn_235_1_url1={}&cdn_1_1_url1={}&cdn_url_back1={}&crop_list1=&music_id1=&video_id1=&voteid1=&voteismlt1=&supervoteid1=&cardid1=&cardquantity1=&cardlimit1=&vid_type1=&show_cover_pic1=0&shortvideofileid1=&copyright_type1=0&releasefirst1=&platform1=&reprint_permit_type1=&allow_reprint1=0&allow_reprint_modify1=0&original_article_type1=&ori_white_list1=%7b%22white_list%22%3a%5b%5d%7d&free_content1=&fee1=0&ad_id1=&guide_words1=&is_share_copyright1=0&share_copyright_url1=&source_article_type1=&reprint_recommend_title1=&reprint_recommend_content1=&share_page_type1=0&share_imageinfo1={}&share_video_id1=&dot1={}&share_voice_id1=&insert_ad_mode1=&categories_list1=[]&sections1={}&compose_info1={}'''.format(
        title1, author1, digest, content1, cdn_url1, cdn_235_1_url1, cdn_1_1_url1, cdn_url_back1,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = '''&ad_video_transition2=&can_reward2=0&related_video2=&is_video_recommend2=-1&title2={}&author2={}&writerid2=0&fileid2=&digest2={}&auto_gen_digest2=1&content2={}&sourceurl2=&need_open_comment2=0&only_fans_can_comment2=0&cdn_url2={}&cdn_235_1_url2={}&cdn_1_1_url2={}&cdn_url_back2={}&crop_list2=&music_id2=&video_id2=&voteid2=&voteismlt2=&supervoteid2=&cardid2=&cardquantity2=&cardlimit2=&vid_type2=&show_cover_pic2=0&shortvideofileid2=&copyright_type2=0&releasefirst2=&platform2=&reprint_permit_type2=&allow_reprint2=0&allow_reprint_modify2=0&original_article_type2=&ori_white_list2=%7b%22white_list%22%3a%5b%5d%7d&free_content2=&fee2=0&ad_id2=&guide_words2=&is_share_copyright2=0&share_copyright_url2=&source_article_type2=&reprint_recommend_title2=&reprint_recommend_content2=&share_page_type2=0&share_imageinfo2={}&share_video_id2=&dot2={}&share_voice_id2=&insert_ad_mode2=&categories_list2=[]&sections2={}&compose_info2={}'''.format(
        title2, author2, digest, content2, cdn_url2, cdn_235_1_url2, cdn_1_1_url2, cdn_url_back2,
        imageinfo, dot,
        section, compose_info
    )
    pay5 = '''&ad_video_transition3=&can_reward3=0&related_video3=&is_video_recommend3=-1&title3={}&author3={}&writerid3=0&fileid3=&digest3={}&auto_gen_digest3=1&content3={}&sourceurl3=&need_open_comment3=0&only_fans_can_comment3=0&cdn_url3={}&cdn_235_1_url3={}&cdn_1_1_url3={}&cdn_url_back3={}&crop_list3=&music_id3=&video_id3=&voteid3=&voteismlt3=&supervoteid3=&cardid3=&cardquantity3=&cardlimit3=&vid_type3=&show_cover_pic3=0&shortvideofileid3=&copyright_type3=0&releasefirst3=&platform3=&reprint_permit_type3=&allow_reprint3=0&allow_reprint_modify3=0&original_article_type3=&ori_white_list3=%7b%22white_list%22%3a%5b%5d%7d&free_content3=&fee3=0&ad_id3=&guide_words3=&is_share_copyright3=0&share_copyright_url3=&source_article_type3=&reprint_recommend_title3=&reprint_recommend_content3=&share_page_type3=0&share_imageinfo3={}&share_video_id3=&dot3={}&share_voice_id3=&insert_ad_mode3=&categories_list3=[]&sections3={}&compose_info3={}'''.format(
        title3, author3, digest, content3, cdn_url3, cdn_235_1_url3, cdn_1_1_url3, cdn_url_back3,
        imageinfo, dot,
        section, compose_info
    )
    pay6 = '''&ad_video_transition4=&can_reward4=0&related_video4=&is_video_recommend4=-1&title4={}&author4={}&writerid4=0&fileid4=&digest4={}&auto_gen_digest4=1&content4={}&sourceurl4=&need_open_comment4=0&only_fans_can_comment4=0&cdn_url4={}&cdn_235_1_url4={}&cdn_1_1_url4={}&cdn_url_back4={}&crop_list4=&music_id4=&video_id4=&voteid4=&voteismlt4=&supervoteid4=&cardid4=&cardquantity4=&cardlimit4=&vid_type4=&show_cover_pic4=0&shortvideofileid4=&copyright_type4=0&releasefirst4=&platform4=&reprint_permit_type4=&allow_reprint4=0&allow_reprint_modify4=0&original_article_type4=&ori_white_list4=%7b%22white_list%22%3a%5b%5d%7d&free_content4=&fee4=0&ad_id4=&guide_words4=&is_share_copyright4=0&share_copyright_url4=&source_article_type4=&reprint_recommend_title4=&reprint_recommend_content4=&share_page_type4=0&share_imageinfo4={}&share_video_id4=&dot4={}&share_voice_id4=&insert_ad_mode4=&categories_list4=[]&sections4={}&compose_info4={}'''.format(
        title4, author4, digest, content4, cdn_url4, cdn_235_1_url4, cdn_1_1_url4, cdn_url_back4,
        imageinfo, dot,
        section, compose_info
    )
    pay7 = '''&ad_video_transition5=&can_reward5=0&related_video5=&is_video_recommend5=-1&title5={}&author5={}&writerid5=0&fileid5=&digest5={}&auto_gen_digest5=1&content5={}&sourceurl5=&need_open_comment5=0&only_fans_can_comment5=0&cdn_url5={}&cdn_235_1_url5={}&cdn_1_1_url5={}&cdn_url_back5={}&crop_list5=&music_id5=&video_id5=&voteid5=&voteismlt5=&supervoteid5=&cardid5=&cardquantity5=&cardlimit5=&vid_type5=&show_cover_pic5=0&shortvideofileid5=&copyright_type5=0&releasefirst5=&platform5=&reprint_permit_type5=&allow_reprint5=0&allow_reprint_modify5=0&original_article_type5=&ori_white_list5=%7b%22white_list%22%3a%5b%5d%7d&free_content5=&fee5=0&ad_id5=&guide_words5=&is_share_copyright5=0&share_copyright_url5=&source_article_type5=&reprint_recommend_title5=&reprint_recommend_content5=&share_page_type5=0&share_imageinfo5={}&share_video_id5=&dot5={}&share_voice_id5=&insert_ad_mode5=&categories_list5=[]&sections5={}&compose_info5={}'''.format(
        title5, author5, digest, content5, cdn_url5, cdn_235_1_url5, cdn_1_1_url5, cdn_url_back5,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = payload + pay2 + pay3 + pay4 + pay5 + pay6 + pay7
    headers = {
        'Host': "mp.weixin.qq.com",
        'Cookie': cookie,
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "https://mp.weixin.qq.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&appmsgid={}&token={}&lang=zh_CN".format(
            appmsgid, tooken),
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache"
    }

    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=pay4, headers=headers, params=querystring, verify=False).json()

    return response


# 第七篇
def get_data7(cookie, tooken, content, user, appid6, title, img0, img1, img2, img3, img4, img5, img6):
    i = user
    # print(data6)
    appmsgid = appid6['appMsgId']
    data_seq = appid6["data_seq"]
    content0 = content[0]
    content1 = content[1]
    content2 = content[2]
    content3 = content[3]
    content4 = content[4]
    content5 = content[5]
    content6 = content[6]
    url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg"

    querystring = {"t": "ajax-response", "sub": "update", "type": "10", "token": tooken, "lang": "zh_CN"}

    title0 = title[0]
    # 定义作者
    author = i[1]
    author = parse.quote(author)
    # 定义关键词
    digest = ''
    # 定义内容
    imageinfo = '%7B%22list%22%3A%5B%5D%7D'
    dot = '%7B%7D'
    # 定义section
    section = ''
    compose_info = ''

    title1 = title[1]
    # 定义作者
    author1 = i[1]
    author1 = parse.quote(author1)
    # 定义关键词
    # 定义内容

    title2 = title[2]
    # 定义作者
    author2 = i[1]
    author2 = parse.quote(author2)
    # 定义关键词
    # 定义内容

    title3 = title[3]
    # 定义作者
    author3 = i[1]
    author3 = parse.quote(author3)
    # 定义关键词
    # 定义内容

    title4 = title[4]
    # 定义作者
    author4 = i[1]
    author4 = parse.quote(author4)
    # 定义关键词
    # 定义内容

    title5 = title[5]
    # 定义作者
    author5 = i[1]
    author5 = parse.quote(author5)
    # 定义关键词
    # 定义内容
    title6 = title[6]
    # 定义作者
    author6 = i[1]
    author6 = parse.quote(author6)

    '''设置封面'''
    cdn_url = img0[0]  # 载入时的截图
    # cdn_url = parse.quote(cdn_url)

    cdn_235_1_url = img0[1]  # 载入时的截图
    # cdn_235_1_url = parse.quote(cdn_235_1_url)

    cdn_1_1_url = img0[2]  # a  截取后的图片
    # cdn_1_1_url = parse.quote(cdn_1_1_url)

    cdn_url_back = img0[3]  # 原图链接
    # cdn_url_back = parse.quote(cdn_url_back)
    # 第二篇
    cdn_url1 = img1[0]  # 载入时的截图
    # cdn_url1 = parse.quote(cdn_url1)

    cdn_235_1_url1 = img1[1]  # 载入时的截图
    # cdn_235_1_url1 = parse.quote(cdn_235_1_url1)

    cdn_1_1_url1 = img1[2]  # a  截取后的图片
    # cdn_1_1_url1 = parse.quote(cdn_1_1_url1)

    cdn_url_back1 = img1[3]  # 原图链接
    # cdn_url_back1 = parse.quote(cdn_url_back1)

    # 第三篇
    cdn_url2 = img2[0]  # 载入时的截图
    # cdn_url2 = parse.quote(cdn_url2)

    cdn_235_1_url2 = img2[1]  # 载入时的截图
    # cdn_235_1_url2 = parse.quote(cdn_235_1_url2)

    cdn_1_1_url2 = img2[2]  # a  截取后的图片
    # cdn_1_1_url2 = parse.quote(cdn_1_1_url2)

    cdn_url_back2 = img2[3]  # 原图链接
    # cdn_url_back2 = parse.quote(cdn_url_back2)

    # 第四篇
    cdn_url3 = img3[0]  # 载入时的截图
    # cdn_url3 = parse.quote(cdn_url3)

    cdn_235_1_url3 = img3[1]  # 载入时的截图
    # cdn_235_1_url3 = parse.quote(cdn_235_1_url3)

    cdn_1_1_url3 = img3[2]  # a  截取后的图片
    # cdn_1_1_url3 = parse.quote(cdn_1_1_url3)

    cdn_url_back3 = img3[3]  # 原图链接

    # 第五篇
    cdn_url4 = img4[0]  # 载入时的截图
    # cdn_url4 = parse.quote(cdn_url4)

    cdn_235_1_url4 = img4[1]  # 载入时的截图
    # cdn_235_1_url4 = parse.quote(cdn_235_1_url4)

    cdn_1_1_url4 = img4[2]  # a  截取后的图片
    # cdn_1_1_url4 = parse.quote(cdn_1_1_url4)

    cdn_url_back4 = img4[3]  # 原图链接
    # cdn_url_back4 = parse.quote(cdn_url_back4)

    # 第六篇
    cdn_url5 = img5[0]  # 载入时的截图
    # cdn_url5 = parse.quote(cdn_url5)

    cdn_235_1_url5 = img5[1]  # 载入时的截图
    # cdn_235_1_url5 = parse.quote(cdn_235_1_url5)

    cdn_1_1_url5 = img5[2]  # a  截取后的图片
    # cdn_1_1_url5 = parse.quote(cdn_1_1_url5)

    cdn_url_back5 = img5[3]  # 原图链接
    # cdn_url_back5 = parse.quote(cdn_url_back5)

    # 第七篇
    cdn_url6 = img6[0]  # 载入时的截图
    # cdn_url6 = parse.quote(cdn_url6)

    cdn_235_1_url6 = img6[1]  # 载入时的截图
    # cdn_235_1_url6 = parse.quote(cdn_235_1_url6)

    cdn_1_1_url6 = img6[2]  # a  截取后的图片
    # cdn_1_1_url6 = parse.quote(cdn_1_1_url6)

    cdn_url_back6 = img6[3]  # 原图链接
    # cdn_url_back6 = parse.quote(cdn_url_back6)
    payload = '''token={}&lang=zh_CN&f=json&ajax=1&random=0.5574217720351184&AppMsgId={}&count=7&data_seq={}&operate_from=Chrome&isnew=0&ad_video_transition0=&can_reward0=0&related_video0=&is_video_recommend0=-1&title0='''.format(
        tooken, appmsgid, data_seq)
    pay2 = '''{}&author0={}&writerid0=0&fileid0=&digest0={}&auto_gen_digest0=1&content0={}&sourceurl0=&need_open_comment0=0&only_fans_can_comment0=0&cdn_url0={}&cdn_235_1_url0={}&cdn_1_1_url0={}&cdn_url_back0={}&crop_list0=&music_id0=&video_id0=&voteid0=&voteismlt0=&supervoteid0=&cardid0=&cardquantity0=&cardlimit0=&vid_type0=&show_cover_pic0=0&shortvideofileid0=&copyright_type0=0&releasefirst0=&platform0=&reprint_permit_type0=&allow_reprint0=0&allow_reprint_modify0=0&original_article_type0=&ori_white_list0=%7b%22white_list%22%3a%5b%5d%7d&free_content0=&fee0=0&ad_id0=&guide_words0=&is_share_copyright0=0&share_copyright_url0=&source_article_type0=&reprint_recommend_title0=&reprint_recommend_content0=&share_page_type0=0&share_imageinfo0={}&share_video_id0=&dot0={}&share_voice_id0=&insert_ad_mode0=&categories_list0=%5B%5D&sections0={}&compose_info0={}'''.format(
        title0, author, digest, content0, cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back,
        imageinfo, dot, section,
        compose_info)
    pay3 = '''&ad_video_transition1=&can_reward1=0&related_video1=&is_video_recommend1=-1&title1={}&author1={}&writerid1=0&fileid1=&digest1={}&auto_gen_digest1=1&content1={}&sourceurl1=&need_open_comment1=0&only_fans_can_comment1=0&cdn_url1={}&cdn_235_1_url1={}&cdn_1_1_url1={}&cdn_url_back1={}&crop_list1=&music_id1=&video_id1=&voteid1=&voteismlt1=&supervoteid1=&cardid1=&cardquantity1=&cardlimit1=&vid_type1=&show_cover_pic1=0&shortvideofileid1=&copyright_type1=0&releasefirst1=&platform1=&reprint_permit_type1=&allow_reprint1=0&allow_reprint_modify1=0&original_article_type1=&ori_white_list1=%7b%22white_list%22%3a%5b%5d%7d&free_content1=&fee1=0&ad_id1=&guide_words1=&is_share_copyright1=0&share_copyright_url1=&source_article_type1=&reprint_recommend_title1=&reprint_recommend_content1=&share_page_type1=0&share_imageinfo1={}&share_video_id1=&dot1={}&share_voice_id1=&insert_ad_mode1=&categories_list1=[]&sections1={}&compose_info1={}'''.format(
        title1, author1, digest, content1, cdn_url1, cdn_235_1_url1, cdn_1_1_url1, cdn_url_back1,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = '''&ad_video_transition2=&can_reward2=0&related_video2=&is_video_recommend2=-1&title2={}&author2={}&writerid2=0&fileid2=&digest2={}&auto_gen_digest2=1&content2={}&sourceurl2=&need_open_comment2=0&only_fans_can_comment2=0&cdn_url2={}&cdn_235_1_url2={}&cdn_1_1_url2={}&cdn_url_back2={}&crop_list2=&music_id2=&video_id2=&voteid2=&voteismlt2=&supervoteid2=&cardid2=&cardquantity2=&cardlimit2=&vid_type2=&show_cover_pic2=0&shortvideofileid2=&copyright_type2=0&releasefirst2=&platform2=&reprint_permit_type2=&allow_reprint2=0&allow_reprint_modify2=0&original_article_type2=&ori_white_list2=%7b%22white_list%22%3a%5b%5d%7d&free_content2=&fee2=0&ad_id2=&guide_words2=&is_share_copyright2=0&share_copyright_url2=&source_article_type2=&reprint_recommend_title2=&reprint_recommend_content2=&share_page_type2=0&share_imageinfo2={}&share_video_id2=&dot2={}&share_voice_id2=&insert_ad_mode2=&categories_list2=[]&sections2={}&compose_info2={}'''.format(
        title2, author2, digest, content2, cdn_url2, cdn_235_1_url2, cdn_1_1_url2, cdn_url_back2,
        imageinfo, dot,
        section, compose_info
    )
    pay5 = '''&ad_video_transition3=&can_reward3=0&related_video3=&is_video_recommend3=-1&title3={}&author3={}&writerid3=0&fileid3=&digest3={}&auto_gen_digest3=1&content3={}&sourceurl3=&need_open_comment3=0&only_fans_can_comment3=0&cdn_url3={}&cdn_235_1_url3={}&cdn_1_1_url3={}&cdn_url_back3={}&crop_list3=&music_id3=&video_id3=&voteid3=&voteismlt3=&supervoteid3=&cardid3=&cardquantity3=&cardlimit3=&vid_type3=&show_cover_pic3=0&shortvideofileid3=&copyright_type3=0&releasefirst3=&platform3=&reprint_permit_type3=&allow_reprint3=0&allow_reprint_modify3=0&original_article_type3=&ori_white_list3=%7b%22white_list%22%3a%5b%5d%7d&free_content3=&fee3=0&ad_id3=&guide_words3=&is_share_copyright3=0&share_copyright_url3=&source_article_type3=&reprint_recommend_title3=&reprint_recommend_content3=&share_page_type3=0&share_imageinfo3={}&share_video_id3=&dot3={}&share_voice_id3=&insert_ad_mode3=&categories_list3=[]&sections3={}&compose_info3={}'''.format(
        title3, author3, digest, content3, cdn_url3, cdn_235_1_url3, cdn_1_1_url3, cdn_url_back3,
        imageinfo, dot,
        section, compose_info
    )
    pay6 = '''&ad_video_transition4=&can_reward4=0&related_video4=&is_video_recommend4=-1&title4={}&author4={}&writerid4=0&fileid4=&digest4={}&auto_gen_digest4=1&content4={}&sourceurl4=&need_open_comment4=0&only_fans_can_comment4=0&cdn_url4={}&cdn_235_1_url4={}&cdn_1_1_url4={}&cdn_url_back4={}&crop_list4=&music_id4=&video_id4=&voteid4=&voteismlt4=&supervoteid4=&cardid4=&cardquantity4=&cardlimit4=&vid_type4=&show_cover_pic4=0&shortvideofileid4=&copyright_type4=0&releasefirst4=&platform4=&reprint_permit_type4=&allow_reprint4=0&allow_reprint_modify4=0&original_article_type4=&ori_white_list4=%7b%22white_list%22%3a%5b%5d%7d&free_content4=&fee4=0&ad_id4=&guide_words4=&is_share_copyright4=0&share_copyright_url4=&source_article_type4=&reprint_recommend_title4=&reprint_recommend_content4=&share_page_type4=0&share_imageinfo4={}&share_video_id4=&dot4={}&share_voice_id4=&insert_ad_mode4=&categories_list4=[]&sections4={}&compose_info4={}'''.format(
        title4, author4, digest, content4, cdn_url4, cdn_235_1_url4, cdn_1_1_url4, cdn_url_back4,
        imageinfo, dot,
        section, compose_info
    )
    pay7 = '''&ad_video_transition5=&can_reward5=0&related_video5=&is_video_recommend5=-1&title5={}&author5={}&writerid5=0&fileid5=&digest5={}&auto_gen_digest5=1&content5={}&sourceurl5=&need_open_comment5=0&only_fans_can_comment5=0&cdn_url5={}&cdn_235_1_url5={}&cdn_1_1_url5={}&cdn_url_back5={}&crop_list5=&music_id5=&video_id5=&voteid5=&voteismlt5=&supervoteid5=&cardid5=&cardquantity5=&cardlimit5=&vid_type5=&show_cover_pic5=0&shortvideofileid5=&copyright_type5=0&releasefirst5=&platform5=&reprint_permit_type5=&allow_reprint5=0&allow_reprint_modify5=0&original_article_type5=&ori_white_list5=%7b%22white_list%22%3a%5b%5d%7d&free_content5=&fee5=0&ad_id5=&guide_words5=&is_share_copyright5=0&share_copyright_url5=&source_article_type5=&reprint_recommend_title5=&reprint_recommend_content5=&share_page_type5=0&share_imageinfo5={}&share_video_id5=&dot5={}&share_voice_id5=&insert_ad_mode5=&categories_list5=[]&sections5={}&compose_info5={}'''.format(
        title5, author5, digest, content5, cdn_url5, cdn_235_1_url5, cdn_1_1_url5, cdn_url_back5,
        imageinfo, dot,
        section, compose_info
    )
    pay8 = '''&ad_video_transition6=&can_reward6=0&related_video6=&is_video_recommend6=-1&title6={}&author6={}&writerid6=0&fileid6=&digest6={}&auto_gen_digest6=1&content6={}&sourceurl6=&need_open_comment6=0&only_fans_can_comment6=0&cdn_url6={}&cdn_235_1_url6={}&cdn_1_1_url6={}&cdn_url_back6={}&crop_list6=&music_id6=&video_id6=&voteid6=&voteismlt6=&supervoteid6=&cardid6=&cardquantity6=&cardlimit6=&vid_type6=&show_cover_pic6=0&shortvideofileid6=&copyright_type6=0&releasefirst6=&platform6=&reprint_permit_type6=&allow_reprint6=0&allow_reprint_modify6=0&original_article_type6=&ori_white_list6=%7b%22white_list%22%3a%5b%5d%7d&free_content6=&fee6=0&ad_id6=&guide_words6=&is_share_copyright6=0&share_copyright_url6=&source_article_type6=&reprint_recommend_title6=&reprint_recommend_content6=&share_page_type6=0&share_imageinfo6={}&share_video_id6=&dot6={}&share_voice_id6=&insert_ad_mode6=&categories_list6=[]&sections6={}&compose_info6={}'''.format(
        title6, author6, digest, content6, cdn_url6, cdn_235_1_url6, cdn_1_1_url6, cdn_url_back6,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = payload + pay2 + pay3 + pay4 + pay5 + pay6 + pay7 + pay8
    headers = {
        'Host': "mp.weixin.qq.com",
        'Cookie': cookie,
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "https://mp.weixin.qq.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&appmsgid={}&token={}&lang=zh_CN".format(
            appmsgid, tooken),
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache"
    }

    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=pay4, headers=headers, params=querystring, verify=False).json()

    return response


# 第八篇
def get_data8(cookie, tooken, content, user, appid7, title, img0, img1, img2, img3, img4, img5, img6, img7,
              ):
    i = user
    # print(data7)
    appmsgid = appid7['appMsgId']
    data_seq = appid7["data_seq"]
    content0 = content[0]
    content1 = content[1]
    content2 = content[2]
    content3 = content[3]
    content4 = content[4]
    content5 = content[5]
    content6 = content[6]
    content7 = content[7]
    url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg"

    querystring = {"t": "ajax-response", "sub": "update", "type": "10", "token": tooken, "lang": "zh_CN"}

    title0 = title[0]
    # 定义作者
    author = i[1]
    author = parse.quote(author)
    # 定义关键词
    digest = ''
    # 定义内容
    imageinfo = '%7B%22list%22%3A%5B%5D%7D'
    dot = '%7B%7D'
    # 定义section
    section = ''
    compose_info = ''

    title1 = title[1]
    # 定义作者
    author1 = i[1]
    author1 = parse.quote(author1)
    # 定义关键词
    # 定义内容

    title2 = title[2]
    # 定义作者
    author2 = i[1]
    author2 = parse.quote(author2)
    # 定义关键词

    title3 = title[3]
    # 定义作者
    author3 = i[1]
    author3 = parse.quote(author3)
    # 定义关键词
    # 定义内容
    title4 = title[4]
    author4 = i[1]
    author4 = parse.quote(author4)
    # 定义内容

    title5 = title[5]
    # 定义作者
    author5 = i[1]
    author5 = parse.quote(author5)
    # 定义关键词
    # 定义内容

    title6 = title[6]
    # 定义作者
    author6 = i[1]
    author6 = parse.quote(author6)
    # 定义关键词
    # 定义内容

    title7 = title[7]
    # 定义作者
    author7 = i[1]
    author7 = parse.quote(author7)
    # 定义关键词
    # 定义内容

    '''设置封面'''
    cdn_url = img0[0]  # 载入时的截图
    cdn_235_1_url = img0[1]  # 载入时的截图
    cdn_1_1_url = img0[2]  # a  截取后的图片
    cdn_url_back = img0[3]  # 原图链接
    # 第二篇
    cdn_url1 = img1[0]  # 载入时的截图
    cdn_235_1_url1 = img1[1]  # 载入时的截图
    cdn_1_1_url1 = img1[2]  # a  截取后的图片
    cdn_url_back1 = img1[3]  # 原图链接
    # 第三篇
    cdn_url2 = img2[0]  # 载入时的截图
    # cdn_url2 = parse.quote(cdn_url2)

    cdn_235_1_url2 = img2[1]  # 载入时的截图
    # cdn_235_1_url2 = parse.quote(cdn_235_1_url2)

    cdn_1_1_url2 = img2[2]  # a  截取后的图片
    # cdn_1_1_url2 = parse.quote(cdn_1_1_url2)

    cdn_url_back2 = img2[3]  # 原图链接
    # cdn_url_back2 = parse.quote(cdn_url_back2)

    # 第四篇
    cdn_url3 = img3[0]  # 载入时的截图
    # cdn_url3 = parse.quote(cdn_url3)

    cdn_235_1_url3 = img3[1]  # 载入时的截图
    # cdn_235_1_url3 = parse.quote(cdn_235_1_url3)

    cdn_1_1_url3 = img3[2]  # a  截取后的图片
    # cdn_1_1_url3 = parse.quote(cdn_1_1_url3)

    cdn_url_back3 = img3[3]  # 原图链接

    # 第五篇
    cdn_url4 = img4[0]  # 载入时的截图
    # cdn_url4 = parse.quote(cdn_url4)

    cdn_235_1_url4 = img4[1]  # 载入时的截图
    # cdn_235_1_url4 = parse.quote(cdn_235_1_url4)

    cdn_1_1_url4 = img4[2]  # a  截取后的图片
    # cdn_1_1_url4 = parse.quote(cdn_1_1_url4)

    cdn_url_back4 = img4[3]  # 原图链接
    # cdn_url_back4 = parse.quote(cdn_url_back4)

    # 第六篇
    cdn_url5 = img5[0]  # 载入时的截图
    # cdn_url5 = parse.quote(cdn_url5)

    cdn_235_1_url5 = img5[1]  # 载入时的截图
    # cdn_235_1_url5 = parse.quote(cdn_235_1_url5)

    cdn_1_1_url5 = img5[2]  # a  截取后的图片
    # cdn_1_1_url5 = parse.quote(cdn_1_1_url5)

    cdn_url_back5 = img5[3]  # 原图链接
    # cdn_url_back5 = parse.quote(cdn_url_back5)

    # 第七篇
    cdn_url6 = img6[0]  # 载入时的截图
    # cdn_url6 = parse.quote(cdn_url6)

    cdn_235_1_url6 = img6[1]  # 载入时的截图
    # cdn_235_1_url6 = parse.quote(cdn_235_1_url6)

    cdn_1_1_url6 = img6[2]  # a  截取后的图片
    # cdn_1_1_url6 = parse.quote(cdn_1_1_url6)

    cdn_url_back6 = img6[3]  # 原图链接
    # cdn_url_back6 = parse.quote(cdn_url_back6)

    # 第八篇
    cdn_url7 = img7[0]  # 载入时的截图
    # cdn_url7 = parse.quote(cdn_url7)

    cdn_235_1_url7 = img7[1]  # 载入时的截图
    # cdn_235_1_url7 = parse.quote(cdn_235_1_url7)

    cdn_1_1_url7 = img7[2]  # a  截取后的图片
    # cdn_1_1_url7 = parse.quote(cdn_1_1_url7)

    cdn_url_back7 = img7[3]  # 原图链接
    # cdn_url_back7 = parse.quote(cdn_url_back7)

    payload = '''token={}&lang=zh_CN&f=json&ajax=1&random=0.5574217720351184&AppMsgId={}&count=8&data_seq={}&operate_from=Chrome&isnew=0&ad_video_transition0=&can_reward0=0&related_video0=&is_video_recommend0=-1&title0='''.format(
        tooken, appmsgid, data_seq)
    pay2 = '''{}&author0={}&writerid0=0&fileid0=&digest0={}&auto_gen_digest0=1&content0={}&sourceurl0=&need_open_comment0=0&only_fans_can_comment0=0&cdn_url0={}&cdn_235_1_url0={}&cdn_1_1_url0={}&cdn_url_back0={}&crop_list0=&music_id0=&video_id0=&voteid0=&voteismlt0=&supervoteid0=&cardid0=&cardquantity0=&cardlimit0=&vid_type0=&show_cover_pic0=0&shortvideofileid0=&copyright_type0=0&releasefirst0=&platform0=&reprint_permit_type0=&allow_reprint0=0&allow_reprint_modify0=0&original_article_type0=&ori_white_list0=%7b%22white_list%22%3a%5b%5d%7d&free_content0=&fee0=0&ad_id0=&guide_words0=&is_share_copyright0=0&share_copyright_url0=&source_article_type0=&reprint_recommend_title0=&reprint_recommend_content0=&share_page_type0=0&share_imageinfo0={}&share_video_id0=&dot0={}&share_voice_id0=&insert_ad_mode0=&categories_list0=%5B%5D&sections0={}&compose_info0={}'''.format(
        title0, author, digest, content0, cdn_url, cdn_235_1_url, cdn_1_1_url, cdn_url_back,
        imageinfo, dot, section,
        compose_info)
    pay3 = '''&ad_video_transition1=&can_reward1=0&related_video1=&is_video_recommend1=-1&title1={}&author1={}&writerid1=0&fileid1=&digest1={}&auto_gen_digest1=1&content1={}&sourceurl1=&need_open_comment1=0&only_fans_can_comment1=0&cdn_url1={}&cdn_235_1_url1={}&cdn_1_1_url1={}&cdn_url_back1={}&crop_list1=&music_id1=&video_id1=&voteid1=&voteismlt1=&supervoteid1=&cardid1=&cardquantity1=&cardlimit1=&vid_type1=&show_cover_pic1=0&shortvideofileid1=&copyright_type1=0&releasefirst1=&platform1=&reprint_permit_type1=&allow_reprint1=0&allow_reprint_modify1=0&original_article_type1=&ori_white_list1=%7b%22white_list%22%3a%5b%5d%7d&free_content1=&fee1=0&ad_id1=&guide_words1=&is_share_copyright1=0&share_copyright_url1=&source_article_type1=&reprint_recommend_title1=&reprint_recommend_content1=&share_page_type1=0&share_imageinfo1={}&share_video_id1=&dot1={}&share_voice_id1=&insert_ad_mode1=&categories_list1=[]&sections1={}&compose_info1={}'''.format(
        title1, author1, digest, content1, cdn_url1, cdn_235_1_url1, cdn_1_1_url1, cdn_url_back1,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = '''&ad_video_transition2=&can_reward2=0&related_video2=&is_video_recommend2=-1&title2={}&author2={}&writerid2=0&fileid2=&digest2={}&auto_gen_digest2=1&content2={}&sourceurl2=&need_open_comment2=0&only_fans_can_comment2=0&cdn_url2={}&cdn_235_1_url2={}&cdn_1_1_url2={}&cdn_url_back2={}&crop_list2=&music_id2=&video_id2=&voteid2=&voteismlt2=&supervoteid2=&cardid2=&cardquantity2=&cardlimit2=&vid_type2=&show_cover_pic2=0&shortvideofileid2=&copyright_type2=0&releasefirst2=&platform2=&reprint_permit_type2=&allow_reprint2=0&allow_reprint_modify2=0&original_article_type2=&ori_white_list2=%7b%22white_list%22%3a%5b%5d%7d&free_content2=&fee2=0&ad_id2=&guide_words2=&is_share_copyright2=0&share_copyright_url2=&source_article_type2=&reprint_recommend_title2=&reprint_recommend_content2=&share_page_type2=0&share_imageinfo2={}&share_video_id2=&dot2={}&share_voice_id2=&insert_ad_mode2=&categories_list2=[]&sections2={}&compose_info2={}'''.format(
        title2, author2, digest, content2, cdn_url2, cdn_235_1_url2, cdn_1_1_url2, cdn_url_back2,
        imageinfo, dot,
        section, compose_info
    )
    pay5 = '''&ad_video_transition3=&can_reward3=0&related_video3=&is_video_recommend3=-1&title3={}&author3={}&writerid3=0&fileid3=&digest3={}&auto_gen_digest3=1&content3={}&sourceurl3=&need_open_comment3=0&only_fans_can_comment3=0&cdn_url3={}&cdn_235_1_url3={}&cdn_1_1_url3={}&cdn_url_back3={}&crop_list3=&music_id3=&video_id3=&voteid3=&voteismlt3=&supervoteid3=&cardid3=&cardquantity3=&cardlimit3=&vid_type3=&show_cover_pic3=0&shortvideofileid3=&copyright_type3=0&releasefirst3=&platform3=&reprint_permit_type3=&allow_reprint3=0&allow_reprint_modify3=0&original_article_type3=&ori_white_list3=%7b%22white_list%22%3a%5b%5d%7d&free_content3=&fee3=0&ad_id3=&guide_words3=&is_share_copyright3=0&share_copyright_url3=&source_article_type3=&reprint_recommend_title3=&reprint_recommend_content3=&share_page_type3=0&share_imageinfo3={}&share_video_id3=&dot3={}&share_voice_id3=&insert_ad_mode3=&categories_list3=[]&sections3={}&compose_info3={}'''.format(
        title3, author3, digest, content3, cdn_url3, cdn_235_1_url3, cdn_1_1_url3, cdn_url_back3,
        imageinfo, dot,
        section, compose_info
    )
    pay6 = '''&ad_video_transition4=&can_reward4=0&related_video4=&is_video_recommend4=-1&title4={}&author4={}&writerid4=0&fileid4=&digest4={}&auto_gen_digest4=1&content4={}&sourceurl4=&need_open_comment4=0&only_fans_can_comment4=0&cdn_url4={}&cdn_235_1_url4={}&cdn_1_1_url4={}&cdn_url_back4={}&crop_list4=&music_id4=&video_id4=&voteid4=&voteismlt4=&supervoteid4=&cardid4=&cardquantity4=&cardlimit4=&vid_type4=&show_cover_pic4=0&shortvideofileid4=&copyright_type4=0&releasefirst4=&platform4=&reprint_permit_type4=&allow_reprint4=0&allow_reprint_modify4=0&original_article_type4=&ori_white_list4=%7b%22white_list%22%3a%5b%5d%7d&free_content4=&fee4=0&ad_id4=&guide_words4=&is_share_copyright4=0&share_copyright_url4=&source_article_type4=&reprint_recommend_title4=&reprint_recommend_content4=&share_page_type4=0&share_imageinfo4={}&share_video_id4=&dot4={}&share_voice_id4=&insert_ad_mode4=&categories_list4=[]&sections4={}&compose_info4={}'''.format(
        title4, author4, digest, content4, cdn_url4, cdn_235_1_url4, cdn_1_1_url4, cdn_url_back4,
        imageinfo, dot,
        section, compose_info
    )
    pay7 = '''&ad_video_transition5=&can_reward5=0&related_video5=&is_video_recommend5=-1&title5={}&author5={}&writerid5=0&fileid5=&digest5={}&auto_gen_digest5=1&content5={}&sourceurl5=&need_open_comment5=0&only_fans_can_comment5=0&cdn_url5={}&cdn_235_1_url5={}&cdn_1_1_url5={}&cdn_url_back5={}&crop_list5=&music_id5=&video_id5=&voteid5=&voteismlt5=&supervoteid5=&cardid5=&cardquantity5=&cardlimit5=&vid_type5=&show_cover_pic5=0&shortvideofileid5=&copyright_type5=0&releasefirst5=&platform5=&reprint_permit_type5=&allow_reprint5=0&allow_reprint_modify5=0&original_article_type5=&ori_white_list5=%7b%22white_list%22%3a%5b%5d%7d&free_content5=&fee5=0&ad_id5=&guide_words5=&is_share_copyright5=0&share_copyright_url5=&source_article_type5=&reprint_recommend_title5=&reprint_recommend_content5=&share_page_type5=0&share_imageinfo5={}&share_video_id5=&dot5={}&share_voice_id5=&insert_ad_mode5=&categories_list5=[]&sections5={}&compose_info5={}'''.format(
        title5, author5, digest, content5, cdn_url5, cdn_235_1_url5, cdn_1_1_url5, cdn_url_back5,
        imageinfo, dot,
        section, compose_info
    )
    pay8 = '''&ad_video_transition6=&can_reward6=0&related_video6=&is_video_recommend6=-1&title6={}&author6={}&writerid6=0&fileid6=&digest6={}&auto_gen_digest6=1&content6={}&sourceurl6=&need_open_comment6=0&only_fans_can_comment6=0&cdn_url6={}&cdn_235_1_url6={}&cdn_1_1_url6={}&cdn_url_back6={}&crop_list6=&music_id6=&video_id6=&voteid6=&voteismlt6=&supervoteid6=&cardid6=&cardquantity6=&cardlimit6=&vid_type6=&show_cover_pic6=0&shortvideofileid6=&copyright_type6=0&releasefirst6=&platform6=&reprint_permit_type6=&allow_reprint6=0&allow_reprint_modify6=0&original_article_type6=&ori_white_list6=%7b%22white_list%22%3a%5b%5d%7d&free_content6=&fee6=0&ad_id6=&guide_words6=&is_share_copyright6=0&share_copyright_url6=&source_article_type6=&reprint_recommend_title6=&reprint_recommend_content6=&share_page_type6=0&share_imageinfo6={}&share_video_id6=&dot6={}&share_voice_id6=&insert_ad_mode6=&categories_list6=[]&sections6={}&compose_info6={}'''.format(
        title6, author6, digest, content6, cdn_url6, cdn_235_1_url6, cdn_1_1_url6, cdn_url_back6,
        imageinfo, dot,
        section, compose_info
    )
    pay9 = '''&ad_video_transition7=&can_reward7=0&related_video7=&is_video_recommend7=-1&title7={}&author7={}&writerid7=0&fileid7=&digest7={}&auto_gen_digest7=1&content7={}&sourceurl7=&need_open_comment7=0&only_fans_can_comment7=0&cdn_url7={}&cdn_235_1_url7={}&cdn_1_1_url7={}&cdn_url_back7={}&crop_list7=&music_id7=&video_id7=&voteid7=&voteismlt7=&supervoteid7=&cardid7=&cardquantity7=&cardlimit7=&vid_type7=&show_cover_pic7=0&shortvideofileid7=&copyright_type7=0&releasefirst7=&platform7=&reprint_permit_type7=&allow_reprint7=0&allow_reprint_modify7=0&original_article_type7=&ori_white_list7=%7b%22white_list%22%3a%5b%5d%7d&free_content7=&fee7=0&ad_id7=&guide_words7=&is_share_copyright7=0&share_copyright_url7=&source_article_type7=&reprint_recommend_title7=&reprint_recommend_content7=&share_page_type7=0&share_imageinfo7={}&share_video_id7=&dot7={}&share_voice_id7=&insert_ad_mode7=&categories_list7=[]&sections7={}&compose_info7={}'''.format(
        title7, author7, digest, content7, cdn_url7, cdn_235_1_url7, cdn_1_1_url7, cdn_url_back7,
        imageinfo, dot,
        section, compose_info
    )
    pay4 = payload + pay2 + pay3 + pay4 + pay5 + pay6 + pay7 + pay8 + pay9
    headers = {
        'Host': "mp.weixin.qq.com",
        'Cookie': cookie,
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "https://mp.weixin.qq.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'referer': "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&appmsgid={}&token={}&lang=zh_CN".format(
            appmsgid, tooken),
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache"
    }

    requests.packages.urllib3.disable_warnings()
    response = requests.request("POST", url, data=pay4, headers=headers, params=querystring, verify=False).json()
    return response
# 实现逻辑
user_list = csv.reader(open(path_user))
# print(user_list)
user_data_list = []
for user in user_list:
    # print(user)
    user_data_list.append(user)
user_list = user_data_list
for n in range(begin_user, end_user):
    user = user_list[n]
    # print(user)
    # 对得到得COOKIE,TOOKEN进行处理
    cookie_tooken = get_url(user, n)
    cookie = cookie_tooken[0]
    tooken = cookie_tooken[1]
    m = n + 1
    # 读取内容
    f = csv.reader(open(path_data))
    # 读取图片
    L_img = []
    f_img = csv.reader(open(path_img))
    for imges in f_img:
        L_img.append(imges)
    L_img = L_img[n * 8 * num_day:(n+1) * 8 * num_day]
    L2_img = [[y for y in L_img[x * 8:(x + 1) * 8]] for x in range(0, num_day)]
    # a = 0
    L = []
    for strt in f:
        L.append(strt)
    L = L[n * 8 * num_day:(n+1) * 8 * num_day]
    L2 = [[y for y in L[x * 8:(x + 1) * 8]] for x in range(0, num_day)]
    # print(len(L2))
    day_num = 0
    for data in L2:
        # print(data)
        img_list = L2_img[day_num]
        img_link_list = get_img_link(cookie, tooken, img_list)
        content = get_content(data, content_info, img_link_list)
        title = get_title(data)
        img0 = get_img0(cookie, tooken, img_link_list)
        img1 = get_img1(cookie, tooken, img_link_list)
        img2 = get_img2(cookie, tooken, img_link_list)
        img3 = get_img3(cookie, tooken, img_link_list)
        img4 = get_img4(cookie, tooken, img_link_list)
        img5 = get_img5(cookie, tooken, img_link_list)
        img6 = get_img6(cookie, tooken, img_link_list)
        img7 = get_img7(cookie, tooken, img_link_list)

        # print(content)
        # 传入文章
        day_num += 1
        print('第{}天的文章开始上传'.format(day_num))
        '''第一篇'''
        appid1 = get_data1(cookie, tooken, content, user, title, img0)
        # time.sleep(0.5)
        # print(1)
        # print(appid1)
        '''第二篇'''
        appid2 = get_data2(cookie, tooken, content, user, appid1, title, img0, img1)
        # time.sleep(0.5)
        '''第三篇'''
        appid3 = get_data3(cookie, tooken, content, user, appid2, title, img0, img1, img2)
        # time.sleep(0.5)

        '''第四篇'''
        appid4 = get_data4(cookie, tooken, content, user, appid3, title, img0, img1, img2, img3)
        # time.sleep(0.5)

        '''第五篇'''
        appid5 = get_data5(cookie, tooken, content, user, appid4, title, img0, img1, img2, img3, img4)
        # time.sleep(0.5)

        '''第六篇'''
        appid6 = get_data6(cookie, tooken, content, user, appid5, title, img0, img1, img2, img3, img4, img5)
        # time.sleep(0.5)

        '''第七篇'''
        appid7 = get_data7(cookie, tooken, content, user, appid6, title, img0, img1, img2, img3, img4, img5,
                           img6)
        # time.sleep(0.5)

        '''第八篇'''
        get_data8(cookie, tooken, content, user, appid7, title, img0, img1, img2, img3, img4, img5, img6, img7)
