

from flask import Flask,request,render_template,redirect,abort
from flask.helpers import make_response, url_for
from flask_mysqldb import MySQL
import json
from werkzeug.utils import secure_filename
import os
from werkzeug.datastructures import Accept

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost' 
app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']='B@taBh2i99b'
app.config['MYSQL_PASSWORD']='NIRmal@0797'
app.config['MYSQL_DB']='new_db'
app.config['UPLOAD_FOLDER']='./static/images/product'
mysql=MySQL(app)





@app.route('/BataBhai12345')
def index():
    return render_template('index.html')

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

@app.route('/BataBhai12345/delete_product',methods=['GET','POST'])
def delete_product_for_admin():
    if request.method=='POST':
        p_id=int(request.form['p_id'])
        conn=mysql.connect
        cur = conn.cursor()
        cur.execute(f"select * from product_table where p_id='{p_id}' and p_status=1;")
        data=cur.fetchone()
        if len(data)!=1:
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
        return "fuck it"
        

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
        filename=secure_filename(f.filename)
        
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


app.run(host='0.0.0.0',port=5000,debug=True)
        

