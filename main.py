from operator import imod
from flask import Flask,request,render_template,redirect,abort
from flask_mysqldb import MySQL
import json
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy

from flask.globals import session
from flask.helpers import make_response, url_for
from datetime import datetime as dt

app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']=   'mysql+mysqldb://root:''@127.0.0.1/new_db.sql'
# db = SQLAlchemy(app)

app.config['MYSQL_HOST']='localhost' 
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='new_db'
app.config['UPLOAD_FOLDER']='./static/images/product'
app.secret_key="8eu1209808"
mysql=MySQL(app)





@app.route('/BataBhai12345')
def index():
    return render_template('dashboard.html')

@app.route('/BataBhai12345/productadd',methods=['GET','POST'])
def handler():
    if request.method=='POST':
        p_name=request.form['p_name']
        p_price=int(request.form['p_price'])

        c_id=int(request.form['c_id'])
        p_description=request.form['p_description']
        p_img=request.form['p_img']
        p_quantity=request.form['p_quantity']
        conn=mysql.connect
        cur = conn.cursor()
        if request.form['action']=='add':
            cur.execute(f"insert into product_table (p_name,p_price,c_id,p_description,p_img,p_quantity) values('{p_name}','{p_price}','{c_id}','{p_description}','{p_img}','{p_quantity}');")
           
        elif request.form['action']=='edit':
            p_id=request.form['p_id']
            cur.execute(f"update product_table SET p_price='{p_price}',p_name='{p_name}',c_id='{c_id}',p_description='{p_description}',p_img='{p_img}',p_quantity='{p_quantity}' where p_id='{p_id}';")
        conn.commit()
        
        return "inserted "

def dict_product(data):
    
    lst=list()
    for i in data:
        map=dict()
        map["p_id"]=i[0]
        map["p_name"]=i[1]
        map["p_img"]=i[2]
        map["c_id"]=i[3]
        map["p_price"]=i[4]
        map["p_description"]=i[5]
        map["p_quantity"]=i[6]
        lst.append(map)
    return lst


@app.route('/BataBhai12345/product',methods=['GET','POST'])
def get_product_for_admin():
    conn=mysql.connect
    cur = conn.cursor()
    cur.execute(f"select * from product_table where p_status=1")
    data=cur.fetchall()
    data=dict_product(data)
    cur.execute(f"select c_id,c_name from category_table where c_status=1")
    data2=cur.fetchall()
    cur.close()

    return render_template('product.html',data=data,data2=data2)

@app.route('/BaZtaBhai12345/delete_product',methods=['GET','POST'])
def delete_product_for_admin():
    if request.method=='POST':
        p_id=int(request.form['p_id'])
        conn=mysql.connect
        cur = conn.cursor()
        cur.execute(f"select * from product_table where p_id='{p_id}' and p_status=1;")
        data=cur.fetchone()
        if len(data)!=1: # DOUBT
            cur.execute(f"update product_table set p_status=0 where p_id='{p_id}';")
            conn.commit()
        else:
            return "unable to delete data"
        cur.close()
        return "data deleted successfully"
    redirect("/BataBhai12345/product")


@app.route('/BataBhai12345/get_product_detail',methods=['GET','POST'])
def get_product_for_admin_ajax():
    if request.method=='POST':
        if request.form['p_id']=="*":
            conn=mysql.connect
            cur = conn.cursor()
            cur.execute(f"select * from product_table where p_status=1")
            data=cur.fetchall()
            data=dict_product(data)
            cur.close()
            print("d")
            return  json.dumps(data)
        else:
            p_id=request.form['p_id']
            conn=mysql.connect
            cur = conn.cursor()
            cur.execute(f"select * from product_table where p_id={p_id} and p_status=1")
            data=cur.fetchall()
            data=dict_product(data)
            cur.close()
            print("d")
            return  json.dumps(data)
    abort(404)
    

@app.route('/BataBhai12345/search_product',methods=['GET','POST'])
def search_product():
    if request.method=='POST':
        p_name=request.form['p_name']
        conn=mysql.connect
        cur=conn.cursor()
        cur.execute(f"select * from product_table where p_name like '%{p_name}%' and p_status=1;")
        data=cur.fetchall()
        if len(data)>=1:
            data=dict_product(data)
            cur.close()
            return json.dumps(data)
        else:
            return "false"
    return redirect('/BataBhai12345/product')


#here is catagory related stuff


def dict_category(data):
    lst=list()
    for i in data:
        map=dict()
        map["c_id"]=i[0]
        map["c_name"]=i[1]
        map["c_img"]=i[2]
        map["c_description"]=i[3]
        lst.append(map)
    return lst

@app.route('/BataBhai12345/category',methods=['GET','POST'])
def get_category_for_admin():
    conn=mysql.connect
    cur = conn.cursor()
    cur.execute(f"select * from category_table where c_status=1")
    data=cur.fetchall()
    data=dict_category(data)
    cur.close()
    return render_template('category.html',data=data) 

@app.route('/BataBhai12345/category/<string:c_id>',methods=['GET','POST'])
def get_product_from_url(c_id):
    c_id=str(c_id)
    if c_id.isnumeric()==False or c_id==" ":
        redirect('/BataBhai12345/category')
   
    conn=mysql.connect
    cur = conn.cursor()
    cur.execute(f"select * from product_table where c_id='{c_id}' and p_status=1;")
    data=cur.fetchall()
    if len(data)==0:
        redirect('/category')
    data=dict_product(data)
    cur.execute(f"select c_id,c_name from category_table where c_status=1")
    data2=cur.fetchall()
    cur.close()

    return render_template('product.html',data=data,data2=data2)

@app.route('/BataBhai12345/search_category',methods=['GET','POST'])
def search_category():
    if request.method=='POST':
        c_name=request.form['c_name']
        conn=mysql.connect
        cur=conn.cursor()
        cur.execute(f"select * from category_table where c_name like '%{c_name}%' and  c_status=1;")
        data=cur.fetchall()
        if len(data)>=1:
            data=dict_category(data)
            cur.close()
            return json.dumps(data)
        else:
            return "false"
    redirect('/BataBhai12345/category')


@app.route('/BataBhai12345/get_category_detail',methods=['GET','POST'])
def get_category_for_admin_ajax():
    if request.method=='POST':
        if request.form['c_id']=="*":
            conn=mysql.connect
            cur = conn.cursor()
            cur.execute(f"select * from category_table where c_status=1")
            data=cur.fetchall()
            data=dict_category(data)
            cur.close()
            return  json.dumps(data)
        else:
            c_id=request.form['c_id']
            conn=mysql.connect
            cur = conn.cursor()
            cur.execute(f"select * from category_table where c_id={c_id} and c_status=1")
            data=cur.fetchall()
            data=dict_category(data)
            cur.close()
            return  json.dumps(data)
    return abort(404)
            
@app.route('/BataBhai12345/category_add',methods=['GET','POST'])
def addcategory():
    if request.method=='POST':
        c_name=request.form['c_name']
        c_description=request.form['c_description']
        c_img=request.form['c_img']
        print(c_img)
        conn=mysql.connect
        cur = conn.cursor()
        if request.form['action']=='add':
            cur.execute(f"insert into category_table (c_name,c_description,c_img) values('{c_name}','{c_description}','{c_img}');")
            print("inserted")
        elif request.form['action']=='edit':
            c_id=request.form['c_id']
            cur.execute(f"update category_table SET c_name='{c_name}',c_description='{c_description}',c_img='{c_img}' where c_id='{c_id}';")
        conn.commit()
        
        return "inserted "
@app.route('/BataBhai12345/delete_category',methods=['GET','POST'])
def delete_category_for_admin():
    if request.method=='POST':
        c_id=int(request.form['c_id'])
        conn=mysql.connect
        cur = conn.cursor()
        cur.execute(f"select * from category_table where c_id='{c_id}'; ")
        data=cur.fetchall()
        print(len(data))
        if len(data)==1:
            cur.execute(f"update product_table set p_status=0  where c_id='{c_id}';")
            cur.execute(f"update category_table set c_status=0 where c_id='{c_id}';")
            conn.commit()
        else:
            return "unable to delete data"
        cur.close()
        return "data deleted successfully"
    return redirect("/BataBhai12345/category")



#here we deal with orders
def order_dict(i,cur):
    mp=dict()
    mp['o_id']=i[0]
    mp['o_status']=str(i[3]).capitalize()
    mp['o_date']=i[2]
    #find order total cost
    data=i[4]
    data=str(data)
    data=json.loads(data)
    total_cost=0
    total_item=len(data)
   
    count=0
    for i in data:
        count+=1
        for key in i:
            #print(i[key])
            quantity=int(i[key])
            p_id=int(key)
            if count==1:
                cur.execute(f"select p_img from product_table where p_id={p_id}")
                p_img=cur.fetchone()[0]
                mp['p_img']=p_img
            cur.execute(f"select p_price from product_table where p_id={p_id}")
            total_cost+=cur.fetchone()[0]*quantity
    mp['total_cost']=total_cost
    mp['total_item']=total_item
    return mp

@app.route('/BataBhai12345/order')
def get_all_order():
    conn=mysql.connect
    cur=conn.cursor()
    cur.execute(f"select * from order_table order by o_date desc;")
    orders=cur.fetchall()
    filtered_data=[]
    for order in orders:
        filtered_data.append(order_dict(order,cur))
    if len(filtered_data)==0:
        return "no data available"
    return  render_template('order.html',data=filtered_data)

@app.route('/BataBhai12345/order/<string:o_status>' ,methods=['GET','POST'])
def order_category(o_status):
    if o_status.isdigit() or o_status!='pending' and o_status!="failed" and o_status!="accepted" and o_status!="cancelled" and o_status!="shipped" and o_status!="delivered" and o_status!="rejected":
        return abort(404)
    conn=mysql.connect
    cur=conn.cursor()
    cur.execute(f"select * from order_table where o_status='{o_status}'  order by o_date desc;")
    orders=cur.fetchall()
    filtered_data=[]
    if len(orders)==0:
        return  render_template('order.html',data=filtered_data)
    filtered_data=[]
    for order in orders:
        filtered_data.append(order_dict(order,cur))
    conn.close()
    return  render_template('order.html',data=filtered_data)


def fetch_address(cur,mp,a_id):
    cur.execute(f"select * from address_table where a_id={a_id}")
    data=cur.fetchone()
    print(data)
    mp['a_id']=a_id
    mp['u_id']=data[1]
    mp['u_name']=data[2]
    mp['u_mob']=data[3]
    mp['u_address']=data[4]
    mp['u_city']=data[5]
    mp['u_pin']=data[6]
    
def dict_fetch_product(i,quantity,total_price):
    map=dict()
    map["p_id"]=i[0]
    map["p_name"]=i[1]
    map["p_img"]=i[2]
    map["c_id"]=i[3]
    map["p_price"]=i[4]
    map["p_description"]=i[5]
    map["p_quantity"]=i[6]
    map['p_size']=quantity
    map['total_price']=total_price
    return map

def fetch_dict(i,cur):
    mp=dict()
    mp['o_id']=i[0]
    mp['o_status']=str(i[3]).capitalize()
    mp['o_date']=i[2]
    a_id=i[1]
    #find order total cost
    data=i[4]
    data=str(data)
    data=json.loads(data)
    total_cost=0
    total_item=len(data)
    count=0
    quantity=0
    item_list=list()
    for i in data:
        count+=1
        for key in i:
            #print(i[key])
            quantity=int(i[key])#fetch name,unit,image,quantity,
            p_id=int(key)
            
            cur.execute(f"select * from product_table where p_id={p_id}")
            product=cur.fetchone()
            cur.execute(f"select p_price from product_table where p_id={p_id}")
            selling_price=cur.fetchone()[0]
            total_cost+=int(selling_price)*quantity
            total_price=selling_price*quantity
            item_list.append(dict_fetch_product(product,quantity,total_price))
            
   # item_list=json.dumps(item_list)#this need to be change at the time of rendering
    mp['item_list']=item_list
    mp['total_cost']=total_cost
    mp['total_item']=total_item
    
    fetch_address(cur,mp,a_id)
    return mp
@app.route('/BataBhai12345/order/fetch_order/<int:o_id>' ,methods=['POST','GET'])
def fetch_order(o_id):
    conn=mysql.connect
    cur=conn.cursor()
    cur.execute(f"select * from order_table where o_id='{o_id}';") 
    data=cur.fetchone()
    if len(data)==0:
        return "looking for bad gateway"
    #data=data[0]
    data=fetch_dict(data,cur)
    #return data
    return render_template('order_by_id.html',data=data)
    
@app.route('/BataBhai12345/update_order_id_admin',methods=['GET','POST'])
def update_admin():
    if request.method=="POST":
        o_id=request.form['o_id']
        o_status=str(request.form['o_status'])
        if o_status!='pending' and o_status!="failed" and o_status!="accepted" and o_status!="cancelled" and o_status!="shipped" and o_status!="delivered" and o_status!="rejected":
            return abort(404)
        conn=mysql.connect
        cur=conn.cursor()
        cur.execute(f"update order_table SET o_status='{o_status}' where o_id='{o_id}';")
        conn.commit()
        conn.close()
        return "Did'nt get  it"
        

    else:
        abort(404)


@app.route('/BataBhai12345/admin_home_info',methods=['POST','GET'])#enter point for admin
def admin_home():
    data=dict()
    conn=mysql.connect
    cur=conn.cursor()
    cur.execute(f"select count(*) from product_table where p_status=1;")
    p_total=cur.fetchone()
    p_total=str(p_total[0])
    cur.execute(f"select count(*) from order_table where o_status='pending';")
    o_p_total=cur.fetchone()
    o_p_total=str(o_p_total[0])
    cur.execute(f"select count(*) from order_table where o_status='accepted';")
    o_a_total=cur.fetchone()
    o_a_total=str(o_a_total[0])
    cur.execute(f"select count(*) from order_table where o_status='shipped';")
    o_s_total=cur.fetchone()
    o_s_total=str(o_s_total[0])
    cur.execute(f"select distinct count(*) from user_table;")
    u_total=cur.fetchone()
    u_total=str(u_total[0])
    print(u_total)
    cur.execute(f"select sum(o_total) from  order_table where o_status='delivered';")
    total_sales=cur.fetchone()
    total_sales=str(total_sales[0])
    data['p_total']=p_total
    data['o_p_total']=o_p_total
    data['o_a_total']=o_a_total
    data['o_s_total']=o_s_total
    data['u_total']=u_total
    data['total_sale']=total_sales
    return render_template('home.html' ,data=data)

@app.route('/BataBhai12345/image_upload/category',methods=['GET','POST'])
def upload_image():
    if request.method=='POST':
        f=request.files['file']
        print(f)
        filename=f.filename
        
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        
        return "success"
    return "fail"

@app.route('/BataBhai12345/users_management',methods=['GET','POST'])
def user_management():
    conn=mysql.connect
    curr=conn.cursor()
    curr.execute(f"select u_mob,u_name from address_table")
    data=curr.fetchall()
    list_data=[]
    for i in data:
        map=dict()
        map['u_name']=i[1]
        map['u_mob']=i[0]
        list_data.append(map)
   
    return render_template('user_manager.html',data=list_data)



        

###here we saterted with admin pannel
















































@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response



@app.route('/')#unprotescted
def index2():
    conn=mysql.connect
    curr=conn.cursor()
    curr.execute(f"select * from category_table where c_status=1 limit 5")
    data=curr.fetchall()
    main_result=[]
    for i in data:
        map=dict()
        map['c_id']=i[0]
       
        result=[]
        k=int(i[0])
        data=dict()
        conn=mysql.connect
        cur=conn.cursor()
        cur.execute(f"select * from product_table where c_id='{k}' and p_status=1 limit 5;")
        order=cur.fetchall()
        for orders in order:  
            data = {}
            data['p_id'] = orders[0]
            data['p_name'] = orders[1]
            data['p_img'] = orders[2]
            data['c_id'] = orders[3]
            data['p_price'] = orders[4]
            data['p_description'] = orders[5]
            data['p_quantity'] = orders[6]
            result.append(data)
        map['c_name']=i[1]
        map['c_img']=i[2]
        map['c_description']=i[3]
        map["c_item"]=result
        main_result.append(map)
    conn.close()
    #return json.dumps(main_result)
    return render_template('index.html' ,data=main_result)


@app.route('/login')#unprotected
def login():
    return render_template('login.html')


@app.route('/bag')
def see_bag():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn=mysql.connect
    curr=conn.cursor()
    curr.execute(f"select cart from user_table where u_id='{session['user_id']}';")
    data=curr.fetchone()
    data_list=[]
    address_list=[]
    print(data)
    if data[0]=='':
        return render_template('bag.html',data=data_list,address_list=address_list)
    if data==None or len(data)==0:
        return redirect(url_for('login'))
    try :
        data=json.loads(data[0])[0]
    except:
        return render_template('bag.html',data=data_list,address_list=address_list)
    size_config=data
    format_strings = ','.join(['%s'] * len(tuple(data.keys())))
    curr.execute("select * from product_table  WHERE p_id IN (%s) and p_status=1 and p_in_stock=1" % format_strings,
                tuple(data.keys()))
    data=curr.fetchall()
    
    for i in data:
        map=dict()
        map['p_id']=i[0]
        map['p_name']=i[1]
        map['p_img']=i[2]
        map['c_id']=i[3]
        map['p_price']=i[4]
        map['p_description']=i[5] 
        map['p_quantity']=i[6]
        map['p_size']=size_config[str(i[0])]
        data_list.append(map)
    curr.execute(f"select * from address_table where u_id='{session['user_id']}'")
    data=curr.fetchall()
    
    for i in data:
        map=dict()
        map['a_id']=i[0]
        map['u_id']=i[1]
        map['a_name']=i[2]
        map['ph_no']=i[3]
        map['a_address']=i[4]
        map['a_city']=i[5]
        map['a_pin']=i[6]
        address_list.append(map)
    
    return  render_template('bag.html',data=data_list,address_list=address_list)




@app.route('/category')
def see_category():
    conn=mysql.connect
    curr=conn.cursor()
    curr.execute(f"select * from category_table where c_status=1")
    data=curr.fetchall()
    list_data=[]
    for i in data:
        map=dict()
        map['c_id']=i[0]
        map['c_name']=i[1]
        map['c_img']=i[2]
        map['c_description']=i[3]
        list_data.append(map)
    conn.close()
    return render_template('category_client.html',data=list_data)
    

@app.route('/user_account_orders')#protected
def profile():
    if 'user_id' in session:
        #code for handling user
        conn=mysql.connect
        curr=conn.cursor()
        curr.execute(f"select * from order_table where a_id in (select a_id from address_table where u_id='{session['user_id']}') order by o_date desc")
        data=curr.fetchall()
        order_list=[]
        if data==None or len(data)==0 or len(data[0])==0:
            return render_template('user_order.html',data=order_list)
        
        for i in data:
            map=dict()
            map['o_id']=i[0]
            map['a_id']=i[1]
            map['o_date']=i[2]
            map['o_status']=i[3]
            map['o_total']=i[5]
            list=json.loads(i[4])[0]
            count=0
            for p in list:
                count+=int(list[p])
            map['item_count']=count
            order_list.append(map)
        return render_template('user_order.html',data=order_list)
    else:
        return redirect(url_for('login'))

@app.route('/logout')#unprotected
def logout():
    if 'user_id' in session:
        session.pop('user_id',None)
        return "loggout"
    else:
        return "all ready loggedout"



@app.route('/signup', methods = ['POST'])
def signupvalid():
    if request.method=='POST':
        data=dict()
        uname= request.form['u_name']
        uid= request.form['u_id']
        data['name']=uname
        data['mob1']=uid
        conn=mysql.connect
        cur=conn.cursor()
        cur.execute(f"select u_id from user_table where u_id='{uid}';")
        order=cur.fetchall()
        if len(order)!=0: 
            return "existing user"
        #cur.execute(f"insert into category_table (c_name,c_description,c_img) values('{c_name}','{c_description}','{c_img}');")
        else: 
            cur.execute(f"insert into user_table (u_id,u_name) values('{uid}','{uname}');")
        session.pop('user_id',None)
        session['user_id']=str(uid)
        conn.commit()
        return "authenticated"

@app.route('/auth_login',methods=['GET','POST'])
def authenticate_login():
    if request.method=="POST":
        user=request.form.get("u_id")
        session.pop('user_id',None)
        conn=mysql.connect
        curr=conn.cursor()
        curr.execute(f"select u_id from user_table where u_id='{request.form['u_id']}'")
        id=curr.fetchone()
        if id==None or len(id)==0:
            return "incorrect"
        session['user_id']=str(user)#session created here
        return "authenticated"
    return abort(404)
    

@app.route('/get_cart_detail',methods=['GET','POST'])
def get_cart_detail():
    if request.method=="POST":
        p_id=request.form['p_id']
        size=request.form['p_size']
        action=request.form['action']
        if 'user_id'  not in session:
            return "do login"
        print(p_id)
        conn=mysql.connect
        curr=conn.cursor()
        curr.execute(f"select * from product_table where p_id='{p_id}' and p_status=1 and p_in_stock=1")
        data=curr.fetchone()
        if data!=None :
            curr.execute(f"select cart from user_table where u_id='{session['user_id']}'; ")
            cart_item=curr.fetchone()
            if len(cart_item[0])==0:
                dict=[{p_id:1}]
                dict=json.dumps(dict)
                curr.execute(f"update  user_table set cart='{dict}' where u_id='{session['user_id']}'; ")
                conn.commit()
                return "success"
            else:
                curr.execute(f"select cart from user_table  where u_id='{session['user_id']}'; ")
                row=curr.fetchone()[0]
                print(row)
                row=json.loads(row)
                row=row[0]
                if row.get(str(p_id))!=None:
                    if action=='add one':
                        row[str(p_id)]=1
                    else:
                        row[str(p_id)]=int(row[str(p_id)])+int(size) #here we got the p_id and we just need to change it
                else:
                    row[str(p_id)]=size
                lst=list()
                
                lst.append(row)
                lst=json.dumps(lst)
                curr.execute(f"update user_table set cart='{lst}' where u_id='{session['user_id']}';")
                conn.commit()
                return "success"
                
        else:
            return "not found"


    else:
        abort(404)
    
@app.route('/save_cart',methods=['GET','POST'])
def save_cart():
    if 'user_id' not in session:
        return render_template('login.html')
    if request.method=='POST':
        data=request.form['dict']
        data=json.loads(data)
        for i in data:
            data[i]=data[i][0]
        lst=list()
        lst.append(data)
        data=lst
        data=json.dumps(data)
        conn=mysql.connect
        curr=conn.cursor()
        curr.execute(f"update  user_table set cart='{data}' where u_id='{session['user_id']}'; ")
        conn.commit()
        conn.close()
        return "hii"
    else:
        abort(404)

@app.route('/save_address',methods=['GET','POST'])
def sav_address():
    if 'user_id' not in session:
        return "failed"
    if request.method=='POST':
        action=request.form['action']
        if action=='select_address':
            a_id=request.form['a_id']
            conn=mysql.connect
            curr=conn.cursor()
            curr.execute(f"select * from address_table where a_id='{a_id}'")
            conn.close()
            data=curr.fetchall()
            if data==None or len(data)==0:
                return "no"

        elif action=='set_and_update':
            u_name=request.form['name'] 
            u_address=request.form['address']
            u_id=session['user_id']
            u_mob=request.form['number']
            u_pin=request.form['pin']
            u_city=request.form['city']
            conn=mysql.connect
            curr=conn.cursor()
            curr.execute(f"insert into address_table (u_id,u_mob,u_address,u_name,u_pin,u_city) values('{u_id}','{u_mob}','{u_address}','{u_name}','{u_pin}','{u_city}') ;")
            conn.commit()
            curr.execute(f"select a_id from address_table where u_id='{u_id}' and u_mob='{u_mob}' and u_address='{u_address}' and u_name='{u_name}' and u_city='{u_city}' and u_pin='{u_pin}';")
            a_id=curr.fetchone()[0]
            print(a_id)
            conn.close()
        else:
            return "get_lost"
        conn=mysql.connect
        curr=conn.cursor()
        curr.execute(f"select cart from user_table where u_id='{session['user_id']}';")
        
        
        data=curr.fetchone()
        if data==None or len(data)==0 or data=='':
            return "cart is empty"
        
        o_status="pending"
        o_item=json.loads(data[0])
        o_item=json.dumps(o_item)
 
        data=json.loads(data[0])[0]
        size_config=data
        format_strings = ','.join(['%s'] * len(tuple(data.keys())))
        curr.execute("select * from product_table  WHERE p_id IN (%s) and p_status=1 and p_in_stock=1" % format_strings,
                    tuple(data.keys()))
        data=curr.fetchall()
        total_cost=0
        for i in data:
            total_cost+=int(i[4])*int(size_config[str(i[0])])
        date=dt.now()
        o_date=date.strftime("%Y-%m-%d")
        print(o_date)
        curr.execute(f"insert into order_table (a_id,o_date,o_status,o_item,o_total) values('{a_id}','{o_date}','{o_status}','{o_item}','{total_cost}');")
        curr.execute(f"update user_table set cart='' where u_id='{session['user_id']}'")
        conn.commit()
        conn.close()
        #code for setting the cart to null with user session

    else:
        abort(404)
        
    return "success"


@app.route('/remove_item',methods=['POST','GET'])
def remove_item():
    if 'user_id' not in session:
        return "login"
    if request.method=='POST':
        p_id=request.form['p_id']
        conn=mysql.connect
        curr=conn.cursor()
        curr.execute(f"select cart from user_table where u_id='{session['user_id']}';")
        data=curr.fetchone()
        if data==None or len(data)==0 or data[0]=='':
            return "cart is empty"
        data=json.loads(data[0])[0]
        
        data.pop(str(p_id))
        if len(data)==0:
            curr.execute(f"update user_table set cart='' where u_id='{session['user_id']}'")
            conn.commit()
            conn.close()
            return "success"
        item=list()
        item.append(data)
        data=json.dumps(item)
        
        curr.execute(f"update user_table set cart='{data}' where u_id='{session['user_id']}'")
        conn.commit()
        conn.close()
        return "success"
@app.route('/all_product',methods=['POST','GET'])
def see_all_product():
    conn=mysql.connect
    curr=conn.cursor()
    curr.execute(f"select * from category_table where c_status=1 ")
    data=curr.fetchall()
    main_result=[]
    for i in data:
        map=dict()
        map['c_id']=i[0]
       
        result=[]
        k=int(i[0])
        data=dict()
        conn=mysql.connect
        cur=conn.cursor()
        cur.execute(f"select * from product_table where c_id='{k}' and p_status=1 limit 4;")
        order=cur.fetchall()
        for orders in order:  
            data = {}
            data['p_id'] = orders[0]
            data['p_name'] = orders[1]
            data['p_img'] = orders[2]
            data['c_id'] = orders[3]
            data['p_price'] = orders[4]
            data['p_description'] = orders[5]
            data['p_quantity'] = orders[6]
            result.append(data)
        map['c_name']=i[1]
        map['c_img']=i[2]
        map['c_description']=i[3]
        map["c_item"]=result
        main_result.append(map)
    conn.close()
    return render_template('product_view.html',data=main_result)





def fetch_address_client(cur,mp,a_id):
    cur.execute(f"select * from address_table where a_id={a_id}")
    data=cur.fetchone()
    print(data)
    mp['a_id']=a_id
    mp['u_id']=data[1]
    mp['u_name']=data[2]
    mp['u_mob']=data[3]
    mp['u_address']=data[4]
    mp['u_city']=data[5]
    mp['u_pin']=data[6]
def dict_fetch_product_client(i,quantity,total_price):
    map=dict()
    map["p_id"]=i[0]
    map["p_name"]=i[1]
    map["p_img"]=i[2]
    map["c_id"]=i[3]
    map["p_price"]=i[4]
    map["p_description"]=i[5]
    map["p_quantity"]=i[6]
    map['p_size']=quantity
    map['total_price']=total_price
    return map

def fetch_dict_client(i,cur):
    mp=dict()
    mp['o_id']=i[0]
    mp['o_status']=str(i[3]).capitalize()
    mp['o_date']=i[2]
    a_id=i[1]
    #find order total cost
    data=i[4]
    data=str(data)
    data=json.loads(data)
    total_cost=0
    total_item=len(data)
    count=0
    quantity=0
    item_list=list()
    for i in data:
        count+=1
        for key in i:
            #print(i[key])
            quantity=int(i[key])#fetch name,unit,image,quantity,
            p_id=int(key)
            
            cur.execute(f"select * from product_table where p_id={p_id}")
            product=cur.fetchone()
            cur.execute(f"select p_price from product_table where p_id={p_id}")
            selling_price=cur.fetchone()[0]
            total_cost+=int(selling_price)*quantity
            total_price=selling_price*quantity
            item_list.append(dict_fetch_product_client(product,quantity,total_price))
            
   # item_list=json.dumps(item_list)#this need to be change at the time of rendering
    mp['item_list']=item_list
    mp['total_cost']=total_cost
    mp['total_item']=total_item
    
    fetch_address_client(cur,mp,a_id)
    return mp


@app.route('/user_account_order/<int:o_id>' ,methods=['POST','GET'])#protected
def fetch_order_client(o_id):
    if 'user_id' not in session:
        return render_template('login.html')
    conn=mysql.connect
    cur=conn.cursor()
    cur.execute(f"select * from order_table where a_id in (select a_id from address_table where u_id='{session['user_id']}') and o_id='{o_id}' order by o_date desc")
    
    data=cur.fetchone()
    if data==None or len(data)==0:
        return abort(404)
    #data=data[0]
    data=fetch_dict_client(data,cur)
    #return data
    return render_template('order_summary.html',data=data)




@app.route('/product_detail/<int:c_id>')
def product_detail_client(c_id):
    conn=mysql.connect
    curr=conn.cursor()
    curr.execute(f"select * from product_table where c_id='{c_id}' and p_status=1 and p_in_stock=1")
    data=curr.fetchall()
    list_data=[]
    curr.execute(f"select c_name from category_table where c_id='{c_id}' and c_status=1")
    data2=curr.fetchone()[0]
    print(data2)
    for i in data:
        map=dict()
        map['p_id']=i[0]
        map['p_name']=i[1]
        map['p_img']=i[2]
        map['c_id']=i[3]
        map['p_price']=i[4]
        map['p_quantity']=i[6]
        list_data.append(map)
    curr.close()
    return render_template('productList.html',data=list_data,c_name=data2)



    
    
@app.route('/update_order_id_client',methods=['GET','POST'])
def update_admin_admin():
    if 'user_id' not in session:
        return render_template('login.html') 
    if request.method=="POST":
        o_id=request.form['o_id']
        o_status=str(request.form['o_status'])
        if o_status!='pending' and o_status!="failed" and o_status!="accepted" and o_status!="cancelled" and o_status!="shipped" and o_status!="delivered" and o_status!="rejected":
            return abort(404)
        conn=mysql.connect
        cur=conn.cursor()
        cur.execute(f"update order_table SET o_status='{o_status}' where o_id='{o_id}';")
        conn.commit()
        conn.close()
        return "order deleted successfully"
        

    else:
        abort(404)
        

@app.route('/search_product/<int:p_id>')
def search_product_admin(p_id):
    conn=mysql.connect
    curr=conn.cursor()
    curr.execute(f"select * from product_table where p_id='{p_id}' and p_status=1 and p_in_stock=1")
    i=curr.fetchone()
    map=dict()
    map['p_id']=i[0]
    map['p_name']=i[1]
    map['p_img']=i[2]
    map['c_id']=i[3]
    map['p_price']=i[4]
    map['p_quantity']=i[6]
    return render_template('product_description.html',data=map)

@app.route('/search_this',methods=['GET','POST'])
def search_this():
    conn=mysql.connect
    curr=conn.cursor()
    try:
        p_name=request.form['p_name']
    except:
        return abort(404)
    curr.execute(f"select p_id,p_name from product_table  where p_name like '%{p_name}%' and p_status=1 and p_in_stock=1 limit 10")
    data=curr.fetchall()
    if data==None or len(data)==0:
        return "none"
    lst=list()
    for i in data:
        map=dict()
        map['p_id']=i[0]
        map['p_name']=i[1]
        lst.append(map)
    lst=json.dumps(lst)
    return lst

    
if __name__=="__main__":
    app.run(port=5000, debug=True)




