from bs4 import BeautifulSoup
import requests
import re
import datetime
import random
from fake_useragent import UserAgent

from .models import db

class Updates:

    def parser(self):

        rows = db(db.company).select(orderby=db.company.id)
        last_row = rows.last()
        try:
            last_id = last_row.id
        except AttributeError:
            last_id = 0

        companies_info=[]
        licenses = []
        id = last_id + 1
        headers = {'user-agent': UserAgent().random}
        r = requests.post(
            'https://kis.nfp.gov.ua/?__VIEWSTATE=%2FwEPDwUKMjA0NDA5OTAxN2RkYp6DC6WJ1c7OZ5ZQtR%2FzO%2BgjVTw%3D&p_EDRPOU='
            '&p_REGNO=&p_FULLNAME=&p_IM_ST=%25null%25&p_IRL_FT=3&p_NFS=0&p_SVIDOTSTVO_SERIES=&p_SVIDOTSTVO_NO=&p_ACTDATE'
            '_FROM=&p_ACTDATE_TO=&p_ILD_NUMBER=&search=1&pagenum=-1&__VIEWSTATEGENERATOR=EC5CD28C', headers = headers)

        html = r.text
        soup = BeautifulSoup(html,'lxml')

        table = soup.find('table', class_='grid zebra')
        tr_list = table.find_all('tr')

        for tr in tr_list:
            if tr.find_all('td'):
                td_list=tr.find_all('td')
                dict_company = {'id':id}
                for td in td_list:
                    if td.find('a') and 'Детально' in td.text:
                         abbreviation,position=self.get_details(td.find('a').get('href'))
                         dict_company['abbreviation'] = abbreviation.strip()
                         director = director.replace(abbreviation.lower().strip(), ' ')
                         director_title=director.title()
                         dict_company['K_NAME'] = director_title
                         director=director.strip()
                         position = position.replace(',', ' ')
                         position = position.replace('-', ' ')
                         position = position.lower().replace(director, ' ')
                         dict_company['position'] = position.title()
                    elif td.get('headers')[0]=="K_NAME":
                        td.text.lower()
                        posada=['генеральний директор','виконуючий обов`язки голови правління','в.о. голови правління','директор',
                                'голова правління','гол. правління','президент']
                        director=td.text.lower()
                        for i in posada:
                            if i in director:
                                director=director.replace(i,' ')
                        director = director.replace('-', ' ')
                        director = director.replace(',', ' ')
                        dict_company['K_NAME'] = director
                    elif td.find('a') and 'Ліцензії' in td.text:
                        licenses=self.get_license(td.find('a').get('href'),id,licenses)
                    elif td.get('headers')[0]=="FILIALS":
                        continue
                    else:
                        dict_company[td.get('headers')[0]] = td.text
                companies_info.append(dict_company)
                id += 1
        return (companies_info,licenses,rows)

    def get_details(self,url):
        new_url = 'https://kis.nfp.gov.ua' + url
        headers = {'user-agent': UserAgent().random}

        r = requests.get(new_url,headers=headers)
        html = r.text
        soup = BeautifulSoup(html, 'lxml')

        abbreviation=soup.find(text='Скорочене найменування заявника (з установчих документів, у разі наявності)').parent.findNext('td').contents[0]
        position=soup.find(text="Прізвище, і'мя та по батькові і найменування посади керівника").parent.findNext('td').contents[0]
        return abbreviation,position

    def get_license(self,url,id,table_info):
        names = []
        just_names = []

        new_url = 'https://kis.nfp.gov.ua' + url
        headers = {'user-agent': UserAgent().random}
        r = requests.get(new_url, headers=headers)
        html = r.text
        soup = BeautifulSoup(html, 'lxml')

        table = soup.find('table', class_='grid zebra')
        try:
            tr_list = table.find_all('tr')
            index = 0
            for tr in tr_list:
                if tr.find_all('th'):
                    th_list=tr.find_all('th')
                    for th in th_list:
                        names.append({th.get('id'):th.text})
                        just_names.append(th.get('id'))
                else:
                    td_list=tr.find_all('td')
                    dict_company = {}
                    for td in td_list:
                        if td.get('a'):
                            dict_company[just_names[index]] = td.find('a').get('href')
                        else:
                            dict_company[just_names[index]] = td.text
                        index += 1
                    dict_company['company_id']=id
                    table_info.append(dict_company)
                    index = 0
        except: pass
        return table_info

    def compare(self,rows,companies):
        changes = ''
        for row in rows:
            i=0
            for key in companies[0]:
                if row.IM_NUMIDENT == companies[i]['IM_NUMIDENT']:
                    if row[key] == companies[i][key]:
                        changes+=key+','
                    else:continue
            companies[i]['changes']=changes
            changes = ''
            i+=1
        return changes

    def company_identifier_update(self):
        companies_id=[]
        rows = db(db.company_identifier).select(orderby=db.company_identifier.id)
        last_row = rows.last()
        try:
            last_id = last_row.id
        except AttributeError:
            last_id = 1

        headers = {'user-agent': UserAgent().random}
        r = requests.post(
            'https://kis.nfp.gov.ua/?__VIEWSTATE=%2FwEPDwUKMjA0NDA5OTAxN2RkYp6DC6WJ1c7OZ5ZQtR%2FzO%2BgjVTw%3D&p_EDRPOU='
            '&p_REGNO=&p_FULLNAME=&p_IM_ST=%25null%25&p_IRL_FT=3&p_NFS=0&p_SVIDOTSTVO_SERIES=&p_SVIDOTSTVO_NO=&p_ACTDATE'
            '_FROM=&p_ACTDATE_TO=&p_ILD_NUMBER=&search=1&pagenum=-1&__VIEWSTATEGENERATOR=EC5CD28C', headers=headers)

        html = r.text
        soup = BeautifulSoup(html, 'lxml')

        table = soup.find('table', class_='grid zebra')
        tr_list = table.find_all('tr')
        if last_id!=1:
            for tr in tr_list:
                if tr.find_all('td'):
                    td_list = tr.find_all('td')
                    dict_company = {}
                    for td in td_list:
                        counter=0
                        if td.get('headers')[0] == "IAN_FULL_NAME":
                            for row in rows:
                                if td.text==row.name:
                                    counter=1
                            if counter!=1:
                                dict_company['id']=last_id+1
                                dict_company["name"]=td.text
                        elif td.get('headers')[0] == "IM_NUMIDENT":
                            for row in rows:
                                if td.text==row.code:
                                    counter=1
                            if counter!=1:
                                dict_company["code"]=td.text
                        else: continue
                    if dict_company:
                        companies_id.append(dict_company)
        else:
            for tr in tr_list:
                if tr.find_all('td'):
                    td_list = tr.find_all('td')
                    dict_company = {'id':last_id}
                    for td in td_list:
                        if td.get('headers')[0] == "IAN_FULL_NAME":
                            dict_company["name"] = td.text
                        elif td.get('headers')[0] == "IM_NUMIDENT":
                            dict_company["code"] = td.text
                        else: continue
                    last_id+=1
                    companies_id.append(dict_company)
        return companies_id

    def add_reference(self,companies):
        company_identifiers = db(db.company_identifier).select(orderby=db.company_identifier.id)
        for company in companies:
            for company_identifier in company_identifiers:
                if company['IM_NUMIDENT'] == company_identifier.code:
                    company['company_identifier']=company_identifier.id
class DataModify:

    def modify_company(self, companies):
        for company in companies:
            for key in company:
                if 'IM_NUMIDENT' in key or 'IAN_RO_CODE' in key:
                    code = company[key]
                    match = re.findall(r'[!()_*&?.,><@]', code)
                    for i in match:
                        code = code.replace(i, '')
                    try:
                        code_len = len(code.strip())
                        int_code = int(code)
                        if 'IM_NUMIDENT' in key and code_len != 8:
                            int_code = None
                    except ValueError:
                        int_code = None
                    company[key] = int_code
                elif 'IAN_RO_DT' in key:
                    date = company['IAN_RO_DT']
                    date_time_obj = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                    company['IAN_RO_DT'] = date_time_obj

    def modify_license(self,licenses):
        for license in licenses:
            for key in license:
                if 'DATE' in key:
                    data = license[key]
                    match = re.findall(r'[!(-)_*&?,><@]', data)
                    for i in match:
                        data = data.replace(i, '')
                    data = data.strip()
                    try:
                        date_time_obj = datetime.datetime.strptime(data, '%d.%m.%Y')
                    except ValueError:
                        date_time_obj = ''
                    license[key] = date_time_obj
                elif 'NFS_CODE' in key:
                    nfs_code=license[key]
                    try:
                        float_nfs_code=float(nfs_code)
                    except ValueError:
                        float_nfs_code=None
                    license[key] = float_nfs_code

    def modify_company_identifier(self, company_identifiers):
        for company_identifier in company_identifiers:
            code = company_identifier['code']
            match = re.findall(r'[!()_*&?.,><@]', code)
            for i in match:
                code = code.replace(i, '')
            try:
                code_len=len(code.strip())
                int_code=int(code)
                if code_len!=8:
                    int_code=None
            except ValueError:
                int_code=None
            company_identifier['code'] = int_code

class DatabaseAccess:

    def get_company_identifiers(self):
        rows = db(db.company_identifier).select()
        return rows

    def get_user(self,id):
        user=db(db.user.auth_user == id).select().first()
        return user

    def get_auth_user(self,id):
        auth_user=db(db.auth_user.id == id).select().first()
        return auth_user

    def add_company_user(self,user,company_identifier):
        db['company_user'].insert(user=user, company_identifier=company_identifier)

    def delete_company_user(self,user_id,company_identifier):
        db(db.company_user.user == user_id and db.company_user.company_identifier == company_identifier).delete()

    def get_codes(self, identifier):
        data=[]
        rows = db(db.company).select()
        for row in rows:
            for key in row.keys():
                if str(identifier) in str(row[key]) and row.IM_NUMIDENT not in data:
                    data.append(row.IM_NUMIDENT)
                    break

        return data

    def get_full_name(self,code):

        rows = db(db.company.IM_NUMIDENT == code).select()
        name = rows[0].IAN_FULL_NAME

        return name

    def get_address(self,code):

        rows = db(db.company.IM_NUMIDENT == code).select()
        address = rows[0].F_ADR

        return address

    def get_director(self,code):

        rows = db(db.company.IM_NUMIDENT == code).select()
        director_name = rows[0].K_NAME

        return director_name

    def get_update_data(self):
        rows = db(db.company).select()
        row = rows.last()
        data = row.update_date
        return data

    def upload_companies(self, company_list):

        for i in range(len(company_list)):
            db['company'].insert(**company_list[i])

        return "OK_company"

    def upload_licenses(self, license_list):

        for i in range(len(license_list)):
            db['license'].insert(**license_list[i])

        return "OK_license"

    def upload_companies_id(self, company_id_list):

        for i in range(len(company_id_list)):
            db['company_identifier'].insert(**company_id_list[i])

        return "OK_company_identifier"

