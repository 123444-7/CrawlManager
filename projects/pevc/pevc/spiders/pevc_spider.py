import datetime
import hashlib

import scrapy
from scrapy.http import FormRequest

# scrapy crawl pevc_spider
from pevc.items import PevcItem


class PevcSpiderSpider(scrapy.Spider):
    name = "pevc_spider"
    url = "https://aic.co/AIC/AIC/Membership/Member-Directory.aspx"

    def start_requests(self):
        url = "https://aic.co/AIC/AIC/Membership/Member-Directory.aspx?WebsiteKey=cabac208-5371-45e7-b5cb-6d0d81afccd6"
        cookies = {
            'AnonymousCartId': '00000000-0000-0000-0000-000000000000',
            '_gid': 'GA1.2.725146638.1696595819',
            'ASP.NET_SessionId': 'yglarbfxzcjn0lbkvxfrel3l',
            '__RequestVerificationToken': 'KOT_jNb7JylDC7KhK8zrURBGyGkp-HdcjzB8OGIx4cYCaUYUemUt2dSMq5P9ptl1wzu6mfDir2mQ_PGo_HwO8Dp2jkYNnyB_ILJbKcrNlNo1',
            'ln_or': 'eyI5MTYzMDciOiJkIn0%3D',
            '_gat_gtag_UA_135276466_1': '1',
            '_ga': 'GA1.1.89876718.1696595764',
            '_ga_63GHMNLX30': 'GS1.1.1696773914.9.0.1696773925.49.0.0',
        }

        headers = {
            'authority': 'aic.co',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': 'AnonymousCartId=00000000-0000-0000-0000-000000000000; _gid=GA1.2.725146638.1696595819; ASP.NET_SessionId=yglarbfxzcjn0lbkvxfrel3l; __RequestVerificationToken=KOT_jNb7JylDC7KhK8zrURBGyGkp-HdcjzB8OGIx4cYCaUYUemUt2dSMq5P9ptl1wzu6mfDir2mQ_PGo_HwO8Dp2jkYNnyB_ILJbKcrNlNo1; ln_or=eyI5MTYzMDciOiJkIn0%3D; _gat_gtag_UA_135276466_1=1; _ga=GA1.1.89876718.1696595764; _ga_63GHMNLX30=GS1.1.1696773914.9.0.1696773925.49.0.0',
            'origin': 'https://aic.co',
            'referer': 'https://aic.co/AIC/AIC/Membership/Member-Directory.aspx',
            'request-id': '|afddcd92667d004d95f6020bf5a588b3.08ef8590fb9d411f',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'traceparent': '00-afddcd92667d004d95f6020bf5a588b3-08ef8590fb9d411f-01',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'x-microsoftajax': 'Delta=true',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = 'ctl01%24ScriptManager1=ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ListerPanel%7Cctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Grid1%24ctl00%24ctl03%24ctl01%24ShowAll&__WPPS=s&__CTRLKEY=&__SHIFTKEY=&ctl01_ScriptManager1_TSM=%3B%3BAjaxControlToolkit%3Aen-US%3A0c8c847b-b611-49a7-8e75-2196aa6e72fa%3Aea597d4b%3Ab25378d2%3BTelerik.Web.UI%2C%20Version%3D2023.1.117.45%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D121fae78165ba3d4%3Aen-US%3Aba768a1f-3205-4bbb-b2c9-b540445080b3%3A16e4e7cd%3A33715776%3Af7645509%3A24ee1bba%3Ae330518b%3A2003d0b8%3Ac128760b%3A88144a7a%3A1e771326%3Ac8618e41%3A1a73651d%3A333f8d94%3Af46195d3%3Ae524c98b%3A58366029%3Aed16cbdc%3Ab2e06756%3A92fe8ea0%3Afa31b949%3A4877f69a%3A19620875%3A874f8ea2%3A490a9d4e%3Abd8f85e4%3B%3BTelerik.Web.UI%2C%20Version%3D2023.1.117.45%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D121fae78165ba3d4%3Aen-GB%3Aba768a1f-3205-4bbb-b2c9-b540445080b3%3Aaa288e2d%3Ab092aa46&NavMenuClientID=ctl01_ciPrimaryNavigation_NavControl_NavMenu&ctl01%24lastClickedElementId=id-ctl01_TemplateBody_WebPartManager1_gwpciMemberDirectoryIQA_ciMemberDirectoryIQA_ResultsGrid_Grid1_ctl00_ctl03_ctl01_ShowAll&ctl01%24ciUtilityNavigation%24ctl09%24SearchTerms=Keyword%20search&ctl01%24ciUtilityNavigation%24ctl12%24SearchTerms=Keyword%20search&ctl01_ciPrimaryNavigation_NavControl_NavMenu_ClientState=&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Sheet0%24ctl03=20d62863-cef6-4038-82f5-e6e47472e326.FS1.FL5&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Sheet0%24Input0%24TextBox1=&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Sheet0%24ctl07=20d62863-cef6-4038-82f5-e6e47472e326.FS1.FL8&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Sheet0%24Input1%24DropDown1=&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Sheet0%24ctl11=20d62863-cef6-4038-82f5-e6e47472e326.FS1.FL7&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Sheet0%24Input2%24TextBox1=&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Sheet0%24ctl16=20d62863-cef6-4038-82f5-e6e47472e326.FS1.FL1&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Sheet0%24Input3%24TextBox1=&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Sheet0%24ctl20=20d62863-cef6-4038-82f5-e6e47472e326.FS1.FL11&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Sheet0%24Input4%24DropDown1=&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Sheet0%24ctl24=20d62863-cef6-4038-82f5-e6e47472e326.FS1.FL13&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24HiddenKeyField1=code_Key&ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Grid1%24ctl00%24ctl03%24ctl01%24PageSizeComboBox=20&ctl01_TemplateBody_WebPartManager1_gwpciMemberDirectoryIQA_ciMemberDirectoryIQA_ResultsGrid_Grid1_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState=&ctl01_TemplateBody_WebPartManager1_gwpciMemberDirectoryIQA_ciMemberDirectoryIQA_ResultsGrid_Grid1_ClientState=&ctl01%24TemplateBody%24ContentPage1%24HiddenDownloadPathField=&ctl01_ciSecondary_SubNavControl_SubNavigationTree_ClientState=%7B%22expandedNodes%22%3A%5B%223%22%5D%2C%22collapsedNodes%22%3A%5B%5D%2C%22logEntries%22%3A%5B%5D%2C%22selectedNodes%22%3A%5B%223%22%5D%2C%22checkedNodes%22%3A%5B%5D%2C%22scrollPosition%22%3A0%7D&ctl01_ciProfilePic_ResultsGrid_Grid1_ClientState=&ctl01%24TemplateScripts%24timeoutsoonmsg=PGgyPllvdSBhcmUgYWJvdXQgdG8gYmUgc2lnbmVkIG91dDwvaDI%2BDQo8cD5Zb3Ugd2lsbCBiZSBzaWduZWQgb3V0IGluIDxzdHJvbmc%2BW1NlY29uZHNSZW1haW5pbmddPC9zdHJvbmc%2BIHNlY29uZHMgZHVlIHRvIGluYWN0aXZpdHkuIFlvdXIgY2hhbmdlcyB3aWxsIG5vdCBiZSBzYXZlZC4gVG8gY29udGludWUgd29ya2luZyBvbiB0aGUgd2Vic2l0ZSwgY2xpY2sgIlN0YXkgU2lnbmVkIEluIiBiZWxvdy48L3A%2B&ctl01%24TemplateScripts%24timeoutsoonstaysignintxt=U3RheSBTaWduZWQgSW4%3D&ctl01%24TemplateScripts%24timeoutsoonlogouttxt=U2lnbiBPdXQ%3D&ctl01%24TemplateScripts%24stayLoggedInURL=&ctl01%24TemplateScripts%24logoutUrl=aHR0cHM6Ly9haWMuY28vYXNpY29tbW9uL2NvbnRyb2xzL3NoYXJlZC9mb3Jtc2F1dGhlbnRpY2F0aW9uL2xvZ2luLmFzcHg%2FU2Vzc2lvblRpbWVvdXQ9MSZSZXR1cm5Vcmw9JTJmQUlDJTJmQUlDJTJmTWVtYmVyc2hpcCUyZk1lbWJlci1EaXJlY3RvcnkuYXNweCUzZg%3D%3D&ctl01_GenericWindow_ClientState=&ctl01_ObjectBrowser_ClientState=&ctl01_ObjectBrowserDialog_ClientState=&ctl01_WindowManager1_ClientState=&__EVENTTARGET=ctl01%24TemplateBody%24WebPartManager1%24gwpciMemberDirectoryIQA%24ciMemberDirectoryIQA%24ResultsGrid%24Grid1%24ctl00%24ctl03%24ctl01%24ShowAll&__EVENTARGUMENT=&__VIEWSTATE=ewfMYrVVRGEbysBgOZb7ypCNqQtFEMP0V3kt59KPR3CApxo%2BX75V5MjdicLpZPmRq0JEUqiqaVxRaZPzYpfQomMhYBgLFjiKWqRDLwm8zwQH%2BUR5TJgRGgm78bOGfUcsAtt208ycP3vQqzFhOjIioUJUQmD%2FhJ%2F8rALQnRw%2Fup6XOJYh%2BL9SJP896de2Pv5gJYm%2Fv%2BlkdBCzTaVThwOoMlVYtvH06Ttr%2BfS5CcU%2FUzhAUNkkuKYQ3bD%2BVAAhtGcwWbtxhA1TDWTkSG2nReFFXQh9p2pyrt6Tqv%2BDQNzzH%2BRdAGP7AgUIGz%2FsWug3YCrh6YKLSv9IsSTBDheDmdjUIMvsqXEcsNR8yHE%2FhCgwBs0hDA%2BR%2Fp2ecnkXnO1EoH79jVz4Ch4beR3FDDHZ6mJ4qwouv7R3yxsD77jYkuAxv3x7HvutHBq4w0N7bXrm4alIUNeYkw9AOLHHFsExMs1Km9qmlqv%2FR4Tldru7a7Zib2xXeTZTxFbFKxt3nw0nFqxfyQ2f5QhYgJQUF%2FRHuMH4UfWNFWCfH7w49sj7KCaj4ipocY3YBhjhwMIWlPTzlXuqPBzq17v88ozfBJuHmlVN1HQDQT0%2BeoSAlQPy55PY2QT1StK%2BKl6AR5nSdlPAs8eky9liNugs4kkrUhZoSngYTCF6jc7acXVw7ebURwFHrTcU7eqbtrg%2F8NVLtU6KPVqrZPmuWQIkwzodIX9NzE4cDVxIfN%2B4d8PAOBaUAtpGerThwsSuIuIkISIcVd20R1hRX%2F28aYUUONHXa6sqFCTTYxzUvReQlgwibWjpEqZxhKvw%2FLtNlPyLjj3rFu4m2bzX%2F%2FRxHUTshQa%2FeL8FQU1B8fDF6gdVr7mlNkoZBsbUdtqHoICCrxHOpBa0npYk%2B%2FILRa7pqshYTHLdmE6gqbYZPNQR09W7Pa263QqX9A0CUKwzRMwd2Y4W%2FSv%2FWUgCQr5KrrGqVLaUrwj8REckmR4%2BkpDV0OW9zZ4QS5xNwRbx%2FtHwa4O%2F3%2BdArVwaUBoWo9mOkheX3jpWYgxy2nHEQEwMLx6qrxBw7JWXxGLIv0WOCypcJsO6M1SnU2Z5dyHo7vSWm52IQyJkRrHdA%2FZjf4U4lzyyFD%2BAw%2Bwl10dwFhA8TUG9hCL7SUEgrqrSooAGV%2BQzz6TrNDGafsnx4syy0BrGKGCEtdO0lWDPHG6yfCj4jzQczDdi3dSnBOAyBordUgOJv%2BZMUh5VGTZ%2FF1T%2B6548wfqxqitvZKvBiyJCV5N4kxstvtlk66ng0ViiQWJrMDD8kIPFgjT4HpKcdGexElQ2nz%2Bk1ttpx8BEEEg8OS7jQsv%2FkQBRk30Exmx%2BZ6CfZ%2FokOUbS7BQfjizNnC6jyhbRbIDePs9HBxyqXapx%2For6ojy1puyhwczCh4N1NNJQRIUsfd60%2BPcrQsxXSkgWWKF0F4mrhfcjtTsnVE1h5NyOgURQeoyJIVrwgVHdg6KjVb52IFD9nZTshJiZ7xDHHV%2FxWCrEhPED8ByB2f1YIR702rXQDnHWtGkpckvOkcGg1C7wLgXOAStJITlhGfcyfFvdXkHKjnpnqDqo%2F48ZGm5hPM7l9dT90Cmi23EJBjeaL8leLSF9nMJeUW0vHdSZTEr%2FqAl9hAZ5CUmseT9IU24roBtopuVvMFxTiy2LJku2uaVhvHa%2FIUyEdtN%2FBAevTx1zvyYuqEHrD68bhnAnI9G0E%2FM9PTVVWoK6tSGDmvOjpv5sHNyVqc2eHaWVawSwnQRhtzhOY7%2Bm6WvRC%2BG4GkStM9WaaQnQfILim%2F4Mea%2BfMbjYRKyw95rrlMI0J6Z%2Bt5YKCTL8zIW2VZNZ9mV2dqTcq1v3%2BrdPredaRmglIWC%2B3j18&__VIEWSTATEGENERATOR=54AC90C5&PageInstanceKey=c025266f-e40a-496c-ac4e-7d21478aabf3&__RequestVerificationToken=0GA45ncPnJqWkXEwlpmXj3HHpDEszNhvZfUb91zx1akIwKkfJLtTa5CaK3ooT86bWjlQUV0Is83a8cqdChllK4k1H0BYEliynJ_mjVDoDK81&TemplateUserMessagesID=ctl01_TemplateUserMessages_ctl00_Messages&PageIsDirty=false&IsControlPostBack=1&__ASYNCPOST=true&'
        yield scrapy.Request(url=url, method='POST', cookies=cookies, headers=headers, body=data, callback=self.parse)

    def parse(self, response):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'referer': ''
        }
        tr_elements = response.xpath('(//table)[2]/tbody/tr')
        print(tr_elements)

        for tr in tr_elements:
            name = tr.xpath('.//td[1]/a/text()').get()
            href = tr.xpath('.//td[1]/a/@href').get()
            data_type = tr.xpath('.//td[2]/text()').get()
            suburb = tr.xpath('.//td[3]/text()').get()
            state = tr.xpath('.//td[4]/text()').get()
            postcode = tr.xpath('.//td[5]/text()').get()
            next_url = "https://aic.co" + str(href)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_details,
                headers=headers,
                meta={
                    'name': name,
                    'type': data_type,
                    'suburb': suburb,
                    'state': state,
                    'postcode': postcode,
                    'url': next_url,
                }
            )

    def parse_details(self, response):
        name = response.meta['name']
        data_type = response.meta['type']
        suburb = response.meta['suburb']
        state = response.meta['state']
        postcode = response.meta['postcode']
        url = response.meta['url']

        img_src = response.xpath('//div[@class="profile-picture-container"]/img/@src').extract_first().replace(
            '../../../', 'https://aic.co/')

        preferred_mailing = ""
        preferred_mailing_span = response.xpath('//span[text()="Preferred Mailing"]')
        if preferred_mailing_span:
            parent_element = preferred_mailing_span.xpath('..')
            sibling_span = parent_element.xpath('following-sibling::div/span')
            if sibling_span:
                preferred_mailing_list = sibling_span.extract()
                preferred_mailing = ''.join(preferred_mailing_list).replace('<br>', ',').replace('\n', ',').replace(
                    '<span id="ctl01_TemplateBody_WebPartManager1_gwpciMiniProfile_ciMiniProfile_contactAddress__address">',
                    '').replace('</span>', '')

        phone = ""
        tel_starting_links = response.xpath('//a[starts-with(@href, "tel")]')
        if tel_starting_links:
            for link in tel_starting_links:
                phone = link.xpath('@href').get().replace('tel:', '')
        else:
            phone = ""

        member_type = ""
        member_type_span = response.xpath('//span[text()="Member Type"]')
        if member_type_span:
            parent_element = member_type_span.xpath('..')
            sibling_span = parent_element.xpath('following-sibling::div/span')
            if sibling_span:
                member_type = sibling_span.xpath('text()').get()

        category = ""
        category_span = response.xpath('//span[text()="Category"]')
        if category_span:
            parent_element = category_span.xpath('..')
            sibling_span = parent_element.xpath('following-sibling::div/span')
            if sibling_span:
                category = sibling_span.xpath('text()').get()

        website = ""
        website_span = response.xpath('//span[text()="Website"]')
        if website_span:
            parent_element = website_span.xpath('..')
            sibling_span = parent_element.xpath('following-sibling::div/span')
            if sibling_span:
                website = sibling_span.xpath('text()').get()

        services_provided = ""
        services_provided_span = response.xpath('//span[text()="Services Provided"]')
        if services_provided_span:
            parent_element = services_provided_span.xpath('..')
            sibling_span = parent_element.xpath('following-sibling::div/span')
            if sibling_span:
                services_provided = sibling_span.xpath('text()').get()

        social_profiles = []
        h2_social_profiles = response.xpath('//h2[text()="Social profiles"]')
        if h2_social_profiles:
            grandparent_div = h2_social_profiles[0].xpath('../..')
            social_links = grandparent_div.xpath('.//a')
            for link in social_links:
                href_value = link.xpath('@href').get()
                social_profiles.append(href_value)

        url_and_title = url + name
        md5_hash = hashlib.md5()
        md5_hash.update(url_and_title.encode('utf-8'))
        hashstr = md5_hash.hexdigest()

        current_date = datetime.datetime.now()
        retrieval_data = current_date.strftime("%Y-%m-%d")

        item = PevcItem()
        item['name'] = name
        item['data_type'] = data_type
        item['suburb'] = suburb
        item['state'] = state
        item['postcode'] = postcode
        item['img_src'] = img_src
        item['preferred_mailing'] = preferred_mailing
        item['phone'] = phone
        item['member_type'] = member_type
        item['category'] = category
        item['website'] = website
        item['services_provided'] = services_provided
        item['social_profiles'] = social_profiles
        item['hashstr'] = hashstr
        item['retrieval_data'] = retrieval_data
        yield item
