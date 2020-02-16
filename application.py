from flask import Flask,render_template,request,redirect,jsonify
import mysql.connector
import datetime
import re
app=Flask(__name__)
global point
def add_custInfo(req:'flask_request')->None:
           var=0
           dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
            
           conn=mysql.connector.connect(**dbconfig)
           cursor=conn.cursor()
           _sql="""insert into user_info(username,phonenum,address,city,state,email,status)
                    values
                    (%s,%s,%s,%s,%s,%s,%s)"""
           cursor.execute(_sql,(req.form['usr'],req.form['phone'],req.form['addr'],req.form['city'],req.form['state'],req.form['email'],'REQUESTED'))
           var=1
           conn.commit()
           cursor.close()
           conn.close()
           if(var==1):
               return True
@app.route('/')
def welcome_page()->'html':
           with open("todos7.txt","w") as fo:
                       fo.write('0') 
           return render_template('welcomepage.html')
@app.route('/onclick_welcome',methods=['POST'])
def reg_userdetails()->'html':
            
            if(add_custInfo(request)):
                 usr=request.form['usr']
                 num=request.form['phone']
                 pattern=re.compile("[0-9]{10}")
                 if(pattern.match(num)):
                      return render_template('enquiry.html',the_name=usr)
                 else:
                     return render_template('welcomepage.html',the_comment='invalid phone number')
@app.route('/onsubmit_enquiry',methods=['POST'])
def get_devdetails()->'html':
                    usr=request.form['pid']
                    
                    trooms=request.form['txt']
                    intvar=int(trooms,10)
                    with open("todos1.txt","a") as fo:
                       fo.write(trooms)
                    return render_template('enquiryroom.html',the_count=intvar,the_user=usr)

@app.route('/onsubmit_enquiryroom',methods=['POST'])
def get_finalenquiry()->'html':
                    devtype=[]
                    cust=0
                    rows=request.form['hid']
                    row=int(rows,10)
                    name=request.form['nme']
                    with open("todos2.txt","a") as fo:
                                 fo.write(name) 
                    lst=list(name)
                    lst.remove('/')
                    res=''.join(lst)
  
                    dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
                    conn=mysql.connector.connect(**dbconfig)
                    cursor=conn.cursor(buffered=True)
                    cursor1=conn.cursor()
                    _sql="""select custid from user_info where username=%(username)s """
                    cursor.execute(_sql,{'username':res})
           
                    for item in cursor.fetchall():
                  
                         cust=item[0]
               
                           
                    details=[]
                    for i in range(0,row):
                         id1='room'+str(i)
                         id2='room1'+str(i)
                         room=request.form[id1]
                         tdevices=request.form[id2]                         
                         id3='chk'+str(i)
                         devtype=request.form.getlist(id3)                         
                         print(devtype)
                         for device in devtype:
                             sql1 = "INSERT INTO enquiry (cust_id, room_name, device_name, power, two_way, inverter_connection, last_updated_by) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                             cursor1.execute(sql1,(cust, room, device, 0.0, 0, 0, 'CUSTOMER-'+str(cust)))
                         '''_sql1="""insert into enquiry_info(roomname,devices_count,devices_name,cust_id)
                                  values
                                 (%s,%s,%s,%s)"""
                         cursor1.execute(_sql1,(room,tdevices,st,cust,))'''
                    conn.commit()
                    cursor.close()
                    cursor1.close()
                    conn.close()
                    return render_template('result.html') 
def search_admin(user:'flask_request',pswd:'flask_request'):
                    dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
                    var=0
                    conn=mysql.connector.connect(**dbconfig)
                    cursor=conn.cursor()
                    _sql="""select admin_name,password from admin_info"""
                    cursor.execute(_sql)
                    for row in cursor.fetchall():
                        temp=''.join(row[0])
                        temp1=''.join(row[1])
                   
                        if(temp==user):
                            if(temp1==pswd):
                                    var+=1
                           
                    if(var>0):
                        return True
                    else:
                        return False
                    conn.commit()
                    cursor.close()
                    conn.close()

def add_adminInfo(req:'flask_request')->None:
                    dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
            
                    conn=mysql.connector.connect(**dbconfig)
                    cursor=conn.cursor()
                    _sql="""insert into admin_info(admin_name,password,email,phonenum)
                            values
                            (%s,%s,%s,%s)"""
                    cursor.execute(_sql,(req.form['usr'],req.form['pwd'],req.form['email'],req.form['phone'],))
                    conn.commit()
                    cursor.close()
                    conn.close()

@app.route('/admin')
def show_adminpage()->'html':
      with open("todos7.txt","r") as fo:
                counter= fo.read()
      print(counter)
      return render_template('adminpage.html')  

@app.route('/checkadmin',methods=['POST'])
def check_admin()->'html':
     with open("todos7.txt","r") as fo:
                counter= fo.read()
     usr=request.form['usr']
     pswd=request.form['pwd']
     if(request.form['enter']=='login'):
           if(search_admin(usr,pswd)):
                dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
                conn=mysql.connector.connect(**dbconfig)
                cursor=conn.cursor()
                _sql=""" select custid,username,email,phonenum from user_info"""
                cursor.execute(_sql)
                contents=cursor.fetchall()
                lenth=len(contents)
                conn.commit()
                cursor.close()
                conn.close()
                return render_template('profile_page.html',the_data=contents,the_status='requested',the_len=lenth)
           else:
               return render_template('adminpage.html',the_comment='user doesnt exist please register or check username and password')
     if(request.form['enter']=='register'):  
           return render_template('adminregister.html')

@app.route('/register_admin',methods=['POST'])
def add_admin()->None:
    add_adminInfo(request)
 
@app.route('/redirect_survey',methods=['post'])
def view_surveyform()->'html':
          rows=request.form['hid']
          with open("todos4.txt","a") as fo:
                       fo.write(rows)
          row=int(rows,10)
          buttons=[]
          for i in range(0,row):
              var='btn'+str(i)
              buttons.append(var)
          btn=request.form['btn']
          with open("todos5.txt","a") as fo:
                       fo.write(btn)
          if(btn in buttons):
                   temp=buttons.index(btn)
                   id='hid'+str(temp)
                   with open("todos3.txt","a") as fo:
                       fo.write(id)
                   usrid=request.form[id]
                   with open("todos3.txt","a") as fo:
                       fo.write(usrid)
                   fid=int(usrid,10)
                   dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
                   conn=mysql.connector.connect(**dbconfig)
                   cursor=conn.cursor()
                   _sql="""select enquiry_id, room_name, device_name, last_updated_by, created_on from enquiry where cust_id=%(cust_id)s"""
                   cursor.execute(_sql,{'cust_id':fid})
                   contents=cursor.fetchall()
                   return render_template('surveyroom.html',the_data=contents,the_cust=fid)

@app.route('/onsubmit_surveyroom',methods=['post'])
def onsubmit_surveyroom()->'html':
          lst=[]
          lst1=[]
          dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
          conn=mysql.connector.connect(**dbconfig)
          cursor=conn.cursor()
          cursor1=conn.cursor()
          cust=request.form['cust']
          custname=int(cust,10)
          print(cust)
          sql="""select enquiry_id from enquiry where cust_id=%(cust_id)s"""
          cursor.execute(sql,{'cust_id':custname})
          contents=cursor.fetchall()
          print(contents)
          lth=len(contents)
          for content in contents:
              for item in content:
                  lst.append(item)
                          
          print(lst)        
          for i in range(0,lth):
             
              id2='way'+str(i)
              twoway=request.form[id2]
              print(twoway)
              id3='power'+str(i)
              pwr=request.form[id3]
              print(pwr)
              id4='devtoinv'+str(i)
              inv=request.form[id4]
              print(inv)
              print(lst[i])
              enqid=lst[i]
              _sql1=""" update enquiry set two_way=%s,power=%s,inverter_connection=%s where enquiry_id=%s """
              cursor1.execute(_sql1,(twoway,pwr,inv,enqid))
              _sql2 = "UPDATE user_info SET status = 'SUREVEYED' WHERE custid = %(custid)s";
              cursor1.execute(_sql2, {'custid': custname})
          conn.commit()
          cursor.close()
          cursor1.close()
          conn.close()
          return render_template('result1.html')
app.run(debug=True)
