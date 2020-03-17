from py4web import action, request, response, Field, Session
from .models import db
from py4web.utils.form import Form, FormStyleBulma
from .common import db,names,tables
from .classes import Updates

import requests
from bs4 import BeautifulSoup
import smtplib
import pandas as pd
import csv
import os
from py4web.utils.auth import Auth
import datetime
session=Session(secret='some key')
auth=Auth(session,db)
auth.enable()

@action("index")
@action.uses("company_detail.html", db)
def api():
    try:
        rows = db(db.company).select()
    except: rows=[]
    return dict(rows=rows,session=session)

@action("license")
@action.uses("license.html", db)
def api():
    try:
        rows = db(db.company).select()
    except: rows=[]
    return dict(rows=rows,session=session)

@action("xxx")
@action.uses(db)
def xxx():
    rows = db(db.company).select(orderby=db.company.id)
    last_row = rows.last()
    try:
        last_id = last_row.id
    except AttributeError:
        last_id=0
    finally:
        x=Updates(last_id)
        t=x.parser()
        x.compare(rows,t[0])
        for i in range(len(t[0])):
            db['company'].insert(**t[0][i])
        for i in range(len(t[1])):
            db['license'].insert(**t[1][i])
    return 'Hi'

@action("add_company",method="GET")
@action.uses("add_company.html", db)
def add():
    rows = db(db.company).select()
    return dict(rows=rows,session=session)

@action("static/add_company",method="POST")
@action.uses("add_company.html", db)
def add():
    rows = db(db.company).select()
    choice_id=request.POST.get('choice_id')
    user_name = globals().get('session').get('user').get('id')
    db['company_user'].insert(user=user_name,company_id=choice_id)
    return dict(rows=rows,session=session)

@action("company_users",method="GET")
@action.uses("company_users.html", db)
def add():
    rows = db(db.company_user.user == 2).select()
    return dict(rows=rows)

@action("upload",method="GET")
@action.uses("upload_file.html")
def upload_get():
    return dict(message="",new_data_dict={},session=session)

@action("static/upload",method="POST")
@action.uses("confirm.html", db)
def upload_post():

    f = request.files["neededFile"]
    table_num = request.POST['table']
    quarter=request.POST['quarter']
    table = tables[table_num]

    f.save('apps/strahovka/xls_files/'+f'{f.filename}')
    message='Файл успешно загружен'
    #pandas and excel
    if table=='payout':
        data_xls=pd.read_excel('apps/strahovka/xls_files/'+f'{f.filename}', index_col=None, skiprows=1, dtype=str)
        new_data_dict = data_xls.to_dict(orient='records')
        print(new_data_dict)
    elif table=='type':
        data_xls = pd.read_excel('apps/strahovka/xls_files/' + f'{f.filename}', index_col=1, dtype=str)
        data_xls = data_xls.T
        print(data_xls)
        data_dict = data_xls.to_dict(orient='index')
        print(data_dict)

        new_data_dict = []
        for key,values_dict in data_dict.items():
            if key=='Назва' or key=='Всього:':
                continue
            new_dict = {}
            new_dict['Назва']=key
            for key2,value2 in values_dict.items():
                for key1, value1 in names[table].items():
                    if key2 == value1:
                        new_dict[key2]=value2
            new_data_dict.append(new_dict)
        print(new_data_dict)
    else:
        data_xls = pd.read_excel('apps/strahovka/xls_files/' + f'{f.filename}')
    rows=db(db.company_user.user == globals().get('session').get('user').get('id')).select()
    message = 'Error'
    for row in rows:
        if str(row.company_id)==new_data_dict[0]['Номер компанії']:
            message = 'Thank you'
            break
    if message != 'Error':
        data = {'message':'Файл успешно загружен', 'new_data_dict':new_data_dict, 'table':table,
        'filename':f.filename, 'quarter':quarter, 'session':session}
    else:
        data = {'message': 'Error','session':session}
    return data

@action("static/confirm",method="POST")
@action.uses("confirm_success.html", db)
def confirm_post():
    table=request.POST['tabl_name']
    file_name=request.POST['file_name']
    quarter = request.POST['quarter']
    print(file_name)
    if table=='payout':
        data_xls=pd.read_excel('apps/strahovka/xls_files/'+f'{file_name}', index_col=None, skiprows=1, dtype=str)
        data_dict = data_xls.to_dict(orient='records')
        new_data_dict=[]
        for i in range(len(data_dict)):
            new_dict = {}
            for key2, value2 in data_dict[i].items():
                for key1,value1 in names['payout'].items():
                    if key2 == value1 or key2 in value1:
                        new_dict[key1]=value2
            new_data_dict.append(new_dict)
        for i in range(len(new_data_dict)):
            db['payout'].insert(**new_data_dict[i])
        print(new_data_dict)
    elif table=='type':
        data_xls = pd.read_excel('apps/strahovka/xls_files/' + f'{file_name}', index_col=1, dtype=str)
        data_xls = data_xls.T
        print(data_xls)
        data_dict = data_xls.to_dict(orient='index')
        print(data_dict)

        new_data_dict = []
        for key,values_dict in data_dict.items():
            if key=='Назва' or key=='Всього:':
                continue
            new_dict = {}
            new_dict['name']=key
            for key2,value2 in values_dict.items():
                for key1, value1 in names['type'].items():
                    if key2 == value1:
                        new_dict[key1]=value2
            new_data_dict.append(new_dict)
        for i in range(len(new_data_dict)):
            db['type'].insert(**new_data_dict[i])
        print(new_data_dict)
    today_data=str(datetime.datetime.now())
    company_id=new_data_dict[0]['company_id']
    user_name=globals().get('session').get('user').get('id')
    db['download'].insert(name=table, data=today_data,quarter_num=quarter,user=user_name,company_id=company_id)
    os.remove('apps/strahovka/xls_files/' + f'{file_name}')
    data={'message':'Thank you','session':session}

    fromaddr = 'testvlada222@gmail.com'
    toaddr = db(db.auth_user.id==user_name).select().first().email
    msg = 'Hello'
    # Gmail Login

    username = 'testvlada222@gmail.com'
    password = 'pydal4weBB'

    # Sending the mail

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()
    return data

@action("auth")
@action.uses("auth.html")
def auth():
    message='Hello'
    return dict(message=message)




