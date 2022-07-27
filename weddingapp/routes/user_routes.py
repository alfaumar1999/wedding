#3rd party import

import random,os,json

import requests

from werkzeug.security import generate_password_hash,check_password_hash
from flask import render_template,redirect,request,flash,session,jsonify
from weddingapp.forms import ContactForm,SignupForm
from weddingapp.models import Contact, Gifts, Guest_gift,Guests,Comment,Lga, Order_details,State, Uniform,Orders

#local import
from weddingapp import app, db

@app.route('/accommodation')
def accommodation():
    username = 'zaynab'
    password = 'abcd'
    try:
        rsp = requests.get("http://127.0.0.1:9990/api/v1.0/getall", auth=(username,password))
        rsp_json = rsp.json()  #converts rsp from HTTP response to json
        return render_template('user/accommodation.html',rsp_json=rsp_json)
    except:
        return 'Please try again Later, The server May be down'


@app.route('/')
def home():
    return render_template('user/index.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    sign = SignupForm()
    if request.method == "GET":
        return render_template('user/signup.html', sign=sign)
    else:
        if sign.validate_on_submit():
            fname = sign.firstname.data #request.form['firstname']
            lname = request.form['lastname']
            email = request.form['email']
            password = request.form['password']
            hashed = generate_password_hash(password)
            # insert into db
            g = Guests(guest_fname=fname,guest_lname=lname,guest_email=email,guest_pwd=password,guest_image='')
            db.session.add(g)
            db.session.commit()
            guestid = g.guest_id #retrieve guestid
            session['guest'] = guestid
            return redirect('/login')
        else:
            return render_template('user/signup.html', sign=sign)

@app.route('/profile',methods=['POST','GET'])
def user_profile():
    loggedin = session.get('guest')
    if loggedin != None:
        guest_deets = db.session.query(Guests).filter(Guests.guest_id==loggedin).first()
        return render_template('user/profile.html', guest_deets=guest_deets)
    else:
        flash("You must be Logged in to view this page")
        return redirect('/login')

@app.route('/user/logout')
def user_logout():
    session.pop('guest', None)
    return render_template('/')

@app.route('/message')
def message():
    cform = ContactForm()
    return render_template('user/contact.html', cform=cform)

@app.route('/login')
def login():
    return render_template('user/login.html')

@app.route('/submitlogin', methods=['POST','GET'])
def submitlogin():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:
        email = request.form['email']
        password = request.form['pass']
        # retrieve the hashed password beloging to this user
        userdeets = Guests.query.filter(Guests.guest_email==email).first()
        passing = Guests.query.filter(Guests.guest_pwd==password).first()
        if userdeets and passing: #check_password_hash(userdeets.guest_pwd, password):
            session['guest'] = userdeets.guest_id
            return redirect('/profile')
        else:
            flash("Invalid credentials")
            return redirect("/login")

        # use function checK_password_hash() to see if th password in the db and the one on the form are the same

@app.route('/submitcontact', methods=['POST'])
def insert_message():
    cform = ContactForm()
    #return request.form
    if cform.validate_on_submit():
        fname = request.form['fullname']
        email = request.form['email']
        msg = request.form['message']
        contact = Contact(con_fullname=fname,con_email=email,con_message=msg)
        db.session.add(contact)
        db.session.commit()
        flash("Message sent!")
        return redirect('/')
    else:
        return render_template('user/contact.html', cform=cform)

@app.route('/user/edit')
def edit_user_profile():
    loggedin = session.get('guest')
    if loggedin != None:
        guest_deets = db.session.query(Guests).filter(Guests.guest_id==loggedin).first()
        return render_template('user/editprofile.html', guest_deets=guest_deets)

@app.route('/user/update', methods=["POST"])
def update_user():
    loggedin = session.get('guest')
    if loggedin != None:
        fname = request.form['fname']
        lname = request.form['lname']
        address = request.form['address']
        record = db.session.query(Guests).get(loggedin)
        record.guest_fname = fname
        record.guest_lname = lname
        record.guest_address = address
        db.session.commit()
        flash('Details Updated')
        return redirect('/profile')
    else:
        return redirect('/login')

@app.route('/user/upload')
def upload_pix():
    loggedin = session.get('guest')
    if loggedin != None:
        return render_template('user/uploadprofile.html')
    else:
        return redirect('/login')


@app.route('/user/submit_upload',methods=['POST'])
def submit_upload():
    loggedin = session.get('guest')
    if loggedin != None:
        #retireving form data and upload picture
        if request.files != "":
            allowed = ['.jpg','.png','.jpeg']
            fileobj = request.files['profilepix']
            original_filename = "weddingapp/static/uploads/"+fileobj.filename
            fileobj.save(f"{original_filename}")#to save the file

            newname = random.random() * 100000
            picturename, ext = os.path.splitext(original_filename) #splits
            #file into 2 parts on the extention
            if ext in allowed:
                path = "weddingapp/static/uploads"+str(newname)+ext
                fileobj.save(f"{path}")

                deets = db.session.query(Guests).get(loggedin)
                deets.guest_image = str(newname)+ext
                db.session.commit()
                flash('Image Successfully Uploaded')
            else:
                flash('Invalid Format')
            return redirect('/profile')
        else:
            flash('please select a valid image')
            return redirect('/user/upload')
    else:
        return redirect('/login')

@app.route('/registry')
def gift_registry():
    loggedin = session.get('guest')  
    if loggedin != None:
        promised_gifts = []
        promised = db.session.query(Guest_gift).filter(Guest_gift.g_guestid==loggedin).all()

        if promised:
            for p in promised:
                promised_gifts.append(p.g_giftid)
        gifts = db.session.query(Gifts).all()
        return render_template('user/gift_registry.html',gifts = gifts, promised_gifts=promised_gifts)
    else:
        flash('you need to be logged in')
        return redirect('/login')

@app.route('/submit/registry',methods=['POST'])
def submit_registry():
    loggedin = session.get('guest')
    if loggedin != None:
        selected = request.form.getlist('selected_gift')
        db.session.execute(f"DELETE FROM guest_gift WHERE g_guestid ='{loggedin}'")
        db.session.commit()

        for s in selected:  #[2,3,4,5,1]
            gg = Guest_gift()
            db.session.add(gg)
            gg.g_giftid = s
            gg.g_guestid = loggedin
            db.session.commit()
            flash('Thank you ,gift inserted successfully')
            return redirect('/profile')
    else:
        flash('You need to be logged in')
        return redirect('/login')  

@app.route('/forum')
def forum():
    return render_template('user/forum.html')  

@app.route('/send_forum', methods=["POST"])
def send_forum():
    loggedin = session.get('guest')
    if loggedin != None:
        d = request.form.get('suggestion')
        c = Comment(comment_guest_id=loggedin, comment_content=d)
        db.session.add(c)
        db.session.commit()
        if c.comment_id > 0:
            return 'thank you for posting comment'
        else:
            return 'please try again'
    else:
        return 'you need to be logged in to post a comment'

#Below are some Ajax demo"""
@app.route('/ajaxtest')
def ajaxtest():
    #retrieve all the states
    states = db.session.query(State).all()
    return render_template('user/testing.html', states=states)

@app.route('/ajaxtest/checkusername', methods=["POST","GET"])
def ajaxtest_submit():
    user = request.values.get('username') #Either post or get
    #to check if the email exists inthe database
    chk = db.session.query(Guests).filter(Guests.guest_email==user).first()
    if chk != None:
        return "<div class='alert alert-danger'>Username has been taken</div>"
    else:
        return '<div class="alert alert-success">Username is available </div>'

@app.route('/ajaxtests/state')
def ajaxtests_state():
    selected = request.args.get('stateid')
    #write a query to fetch all LGAs where state_id == selected
    lgas = db.session.query(Lga).filter(Lga.state_id == selected).all()

    make = ''
    for i in lgas:
        make = make + f"<option value'{i.lga_id}'>{i.lga_name} </option>"
    return make

@app.route('/ajaxtests/final',methods=["POST"])
def final_test():
    appended_data = request.form.get('missing')
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    #retrieving the file
    fileobj = request.files['image']
    original_filename = fileobj.filename
    fileobj.save(f'weddingapp/static/images/{original_filename}')

    #INSERT INTO GUEST TABLE
    return jsonify(firstname=firstname,lastname=lastname,appended_data=appended_data,filename=original_filename)

def get_price(itemid):
    deets = Uniform.query.get(itemid)
    if deets != None:
        return deets.uni_price
    else:
        return 0

def generate_ref():
    ref = random.random() *1000000000
    return int(ref)

#PROCESS FOR MAKING PAYMENTS

@app.route('/asoebi', methods=['POST','GET'])
def asoebi():
    loggedin = session.get('guest')
    if loggedin != None:
        if request.method == 'GET':
            uni = db.session.query(Uniform).all()
            return render_template('user/aso_ebi.html', uni=uni)
        else:
            #TO retrieve
            uniform_selected = request.form.getlist('uniform')
            if uniform_selected:
                ref = generate_ref()
                session['reference'] = ref
                ord = Orders(order_by=loggedin,order_status='pending',order_ref=ref)
                db.session.add(ord)
                db.session.commit()
                #INSERT ALL THE ITEMS INTO ORDER_DETAILS
                orderid = ord.order_id
                
                total = 0
                for i in uniform_selected:
                    price = get_price(i)
                    ord_det = Order_details(det_orderid=orderid,det_itemid=i,det_itemprice=price)
                    total = total + price
                    db.session.add(ord_det)
                ord.order_totalamt = total
                db.session.commit()
                return redirect('/confirmation')
                #return 'Done'
            else:
                flash('Please make a selection')
                return redirect('/asoebi')
    else:
         return redirect('/login')

@app.route('/confirmation')
def confirmations():
    loggedin = session.get('guest')
    ref = session.get('reference')
    if loggedin != None:
        deets = Orders.query.join(Order_details,Orders.order_id==Order_details.det_orderid).join(Uniform,Order_details.det_itemid==Uniform.uni_id).filter(Orders.order_by==loggedin, Orders.order_ref==ref).add_columns(Order_details,Uniform).all()

        t = Orders.query.filter(Orders.order_ref==ref).first()
        return render_template('user/confirmation.html', deets=deets,total = t.order_totalamt)
    else:
        return redirect('/login')

@app.route('/initialize_paystack')
def initialize():
    #connect to  paystack and send amount,email,ref,key
    loggedin = session.get('guest')
    if loggedin  != None:
        ref = session.get('reference')
        a = db.session.query(Orders).filter(Orders.order_ref==ref).first()
        amount= a.order_totalamt
        g = db.session.query(Guests).get(loggedin)

        data = {"email":g.guest_email, "amount":a.order_totalamt*100, "reference":ref}
        headers = {"Content-Type"}
    return "done"

















    
