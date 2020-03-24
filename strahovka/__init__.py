from py4web import action, request, Session
from .models import db
from .common import names,tables
from .classes import Updates,DatabaseAccess
from py4web.utils.form import Form, FormStyleBulma

import smtplib
import pandas as pd
import os
from py4web.utils.auth import Auth
import datetime

session=Session(secret='some key')
auth=Auth(session,db)
auth.enable()

@action("index")
@action.uses("company_detail.html", db)
def app_second():
    try:
        rows = db(db.company).select()
    except: rows=[]
    return dict(rows=rows,session=session)

@action("license")
@action.uses("license.html", db)
def app():
    try:
        rows = db(db.company).select()
    except: rows=[]
    return dict(rows=rows,session=session)

@action("access")
@action.uses(db)
def access():
    obj=DatabaseAccess()
    codes=obj.get_codes('0692')
    name = obj.get_full_name('20693867')
    adr = obj.get_address('20693867')
    di = obj.get_director('20693867')
    print(codes)
    print(name)
    print(adr)
    print(di)
    return 'OK'

@action("edit",method=["GET","POST"])
@action.uses("add_company.html", db)
def add():
    # db(db.company.id>0).delete()
    # db(db.license.id>0).delete()
    rows = db(db.company).select()
    user_id = globals().get('session').get('user').get('id')
    user = db(db.auth_user.id==user_id).select().first()
    form = Form(db.auth_user, user_id, deletable=False, formstyle=FormStyleBulma)
    return dict(rows=rows,user=user,session=session,form=form)

@action("update_database",method="GET")
@action.uses(db)
def update_database():
    db_obj = DatabaseAccess()
    obj = Updates()
    try:
        data = db_obj.get_update_data()
        now = datetime.datetime.now()
        if (now - data).seconds > 10000:
            tuple_obj = obj.parser()
            obj.compare(tuple_obj[2], tuple_obj[0])
            obj.modify_data(tuple_obj[0], tuple_obj[1])
            print(db_obj.upload_companies(tuple_obj[0])+'1')
            print(db_obj.upload_licenses(tuple_obj[1])+'1')
    except AttributeError:
        tuple_obj=obj.parser()
        obj.compare(tuple_obj[2],tuple_obj[0])
        obj.modify_data(tuple_obj[0],tuple_obj[1])
        print(db_obj.upload_companies(tuple_obj[0])+'2')
        print(db_obj.upload_licenses(tuple_obj[1])+"2")
    return 'Hello'

@action("static/add_company",method="POST")
@action.uses("add_company.html", db)
def add():
    rows = db(db.company).select()
    choice_id=request.POST.get('choice_id')
    user_name = globals().get('session').get('user').get('id')
    user = db(db.auth_user.id == user_name).select().first()
    db['company_user'].insert(user=user_name,company_id=choice_id)
    form = Form(db.auth_user, user_name, deletable=False, formstyle=FormStyleBulma)
    return dict(rows=rows,user=user, form = form,session=session)

@action("static/delete_company",method="POST")
@action.uses("add_company.html", db)
def add():
    rows = db(db.company).select()
    choice_id=request.POST.get('choice_id')
    user_name = globals().get('session').get('user').get('id')
    user = db(db.auth_user.id == user_name).select().first()
    db(db.company_user.user == user_name and db.company_user.company_id == choice_id).delete()
    form = Form(db.auth_user, user_name, deletable=False, formstyle=FormStyleBulma)
    return dict(rows=rows,user=user, form = form,session=session)

@action("company_users",method="GET")
@action.uses("company_users.html", db)
def add():
    # obj=Updates()
    # tuple_obj = obj.parser()
    # print(tuple_obj[1])
    rows = db(db.auth_user).select()
    rows2 = db(db.company_user).select()
    return dict(rows=rows,rows2=rows2)

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
