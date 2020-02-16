from flask import Flask,render_template,request,redirect,jsonify
import mysql.connector
import datetime
counter=0
app=Flask(__name__)
def search_usr(user:'flask_request',pswd:'flask_request'):
            dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
            var=0
            conn=mysql.connector.connect(**dbconfig)
            cursor=conn.cursor()
            _sql="""select username,password from customer_info"""
            cursor.execute(_sql)
            for row in cursor.fetchall():
                    temp=''.join(row[0])
                    temp1=''.join(row[1])
                    with open("todos.txt","a") as fo:
                       fo.write(temp)
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

def add_custInfo(req:'flask_request')->None:
           dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
            
           conn=mysql.connector.connect(**dbconfig)
           cursor=conn.cursor()
           _sql="""insert into customer_info(username,password,email,phonenum,address,city,state)
                    values
                    (%s,%s,%s,%s,%s,%s,%s)"""
           cursor.execute(_sql,(req.form['usr'],req.form['pwd'],req.form['email'],req.form['phone'],req.form['addr'],req.form['city'],req.form['state'],))
           conn.commit()
           cursor.close()
           conn.close()

def update_prodinfo(prodname:str,usrname:str):
           words=usrname.split(' ',1)
           name=words[1]
           global counter
           with open("todos.txt","a") as fo:
                       fo.write(name)
           dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
           conn=mysql.connector.connect(**dbconfig)
           cursor=conn.cursor(buffered=True)
           cursor1=conn.cursor()
           _sql="""select custid from customer_info where username=%(username)s """
           cursor.execute(_sql,{'username':name})
           
           for item in cursor.fetchall():
                  
                  cust=item[0]
               
                
           
           start_date = datetime.date.today()
           
           _sql1="""insert into products_info(prod_name,purchase_date,cust_id)
                    values
                    (%s,%s,%s)"""
           cursor1.execute(_sql1,(prodname,start_date,cust,))
           counter+=1
           conn.commit()
           cursor.close()
           cursor1.close()
           conn.close()
           return True  

@app.route('/')
def show_welcomepage()-> 'html':
                 return render_template('loginpage.html')
@app.route('/search4',methods=['GET','POST'])
def loginpage()->'html':
       with open("todos.txt","a") as fo:
                       fo.write("im in function")
       usr=request.form['usr1']
       psw=request.form['pwd1']
       with open("todos.txt","a") as fo:
                       fo.write(usr)
       if(request.form['enter']=='login'):
           if(search_usr(usr,psw)):
            
                return render_template('product_list.html',the_custname=usr)
           else:
               return render_template('loginpage.html',the_notfi='user doesnt exist please register or check username and password')
       if(request.form['enter']=='register'):
               return render_template('register.html')
@app.route('/onclick_register')
def onclick()->'html':
    return render_template('register.html')
 
@app.route('/register_user',methods=['POST'])
def add_user()->None:
    add_custInfo(request)       

@app.route('/place_order',methods=['POST'])
def prod_select()->'html':
      with open("todos.txt","a") as fo:
                       fo.write("im in function prod_select")
      global counter
      if(request.form['pls']=='orderpulse'):
                 proid=request.form['prod1']
                 custname=request.form['ref']
                 with open("todos.txt","a") as fo:
                       fo.write("im in function form ")
                 update_prodinfo(proid,custname)
                 if(update_prodinfo(proid,custname)):
                       
                       return render_template('blank.html',the_prod=proid,the_name=custname)
      elif(request.form['pls']=='orderpulsetetra'):
                 var=request.form['prod2']
                 var1=request.form['ref']
                 update_prodinfo(var,var1)
                 if(update_prodinfo(var,var1)):
                       
                       return render_template('blank.html',the_prod=var,the_name=var1)
                 
      elif(request.form['pls']=='orderhexa'):
                 varhexa=request.form['prod3']
                 varcust=request.form['ref']
                 update_prodinfo(varhexa,varcust)
                 if(update_prodinfo(varhexa,varcust)):
                       
                       return render_template('blank.html',the_prod=proid,the_name=custname)
      else:
                        
                        usrname=request.form['ref']
                        words=usrname.split(' ',1)
                        name=words[1]
                        dbconfig={ 'host':'127.0.0.1',
                                    'user':'webapp',
                                    'password':'pswdapp',
                                    'charset':'utf8',
                                    'database':'homeautomation',}
                         
                        conn=mysql.connector.connect(**dbconfig)
                        cursor=conn.cursor()
                        _sql=""" select p.prod_name from customer_info AS ci INNER JOIN products_info AS p ON ci.custid=p.cust_id where ci.username=%(ci.username)s"""
                        cursor.execute(_sql,{'ci.username':name})
                        content=cursor.fetchall()
                        if(all(content)):
                               return render_template('complain.html',the_data=content,the_cust=name)
                        else:
                               return render_template('complainfail.html',the_name='no item purchased so cannot register a complain')
@app.route('/admin')                      
@app.route('/admin')
def show_adminpage()->'html':
     return render_template('adminpage.html')
@app.route('/checkadmin',methods=['POST'])
def check_admin()->'html':
     usr=request.form['usr1']
     pswd=request.form['pwd1']
     if(usr=='admin'):
        if(pswd=='admin'):
              dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
              conn=mysql.connector.connect(**dbconfig)
              cursor=conn.cursor()
              _sql=""" select p.prod_id,ci.username,p.prod_name,ci.email,p.purchase_date from customer_info AS ci INNER JOIN products_info AS p ON ci.custid=p.cust_id"""
              cursor.execute(_sql)
              contents=cursor.fetchall()
              return render_template('profilepage.html',the_data=contents,the_status='check status')
     else:
         return render_template('adminpage.html',the_comment='check the admin login details')
@app.route('/button_click',methods=['post'])
def click_redirect()->'html':
  
     if(request.form['btn']=='survey'):
              custname=request.form['cust']    
              dbconfig={ 'host':'127.0.0.1',
                       'user':'webapp',
                       'password':'pswdapp',
                       'charset':'utf8',
                       'database':'homeautomation',}
              conn=mysql.connector.connect(**dbconfig)
              cursor=conn.cursor()
              _sql=""" select p.prod_id,p.prod_name from customer_info AS ci INNER JOIN products_info AS p ON ci.custid=p.cust_id where ci.username=%(ci.username)s"""
              cursor.execute(_sql,{'ci.username':custname})
              content=cursor.fetchall()
              return render_template('reqsurvey.html',the_data=content,the_cust=custname)
@app.route('/complain_type',methods=['post','get'])
def complain_type()->'html':
              name=request.args.getlist('s.no')
              usr=request.args.get('name')
              res='btn'+name[0]
              if(request.form['btn']==res):
                      return render_template('blank.html',the_cust=name,the_prod=usr)
      
                 
app.run(debug=True)
