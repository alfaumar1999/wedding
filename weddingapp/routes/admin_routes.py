#3rd party import

from flask import Flask, flash, render_template,redirect,request,session,url_for
from weddingapp.models import *
from sqlalchemy import desc 

#local import
from weddingapp import app, db, csrf

@app.route('/admin', methods=["POST","GET"])
@csrf.exempt #for the token
def admin_home():
    #return request.method
    #return render_template('admin/admin_login.html')
    if request.method =='GET':
        return render_template('admin/admin_login.html')
    else:
        username = request.form['username']
        pwd = request.form['pswd']

        ad = Admin.query.filter(Admin.admin_username==username,Admin.admin_pwd==pwd).first()
        if ad:
            adminid = ad.admin_id
            admin_fullname = ad.admin_name
            session['adminid'] = adminid
            session['adminname'] = admin_fullname
            return redirect('/admin/dashboard')
        else:
            flash('invalid credentials')
            return redirect('/admin')

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('adminid') !=None and session.get('adminname')!=None:
        return render_template('admin/admin_dashboard.html')
    else:
        return redirect('/admin')

@app.route('/admin/logout')
def admin_logout():
    session.pop('adminid',None)
    session.pop('adminname',None)
    return 'done'

@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/admin/managegifts')
def manage_gifts():
    if session.get('adminid') != None and session.get('adminname') != None:
        gifts = db.session.query(Gifts).all()
        #gifts = db.session.query(Gifts).order_by(Gifts.gift_name.desc()).offset(1).limit(2).all()
        #gifts = db.session.query(Gifts).order_by(Gifts.gift_name).all()
        return render_template('/admin/all_gifts.html', gifts=gifts)
    else:
        return redirect('/admin')

@app.route('/admin/add/gifts', methods=["POST","GET"])
def add_gifts():
    if session.get('adminid') != None and session.get('adminname') != None:
        if request.method == 'GET':
            return render_template('admin/newgift.html')
        else:
            #the gift listing page(/admin/managegifts)
            giftname = request.form['giftname']
            #add: instantiate an object o fthe model,add to session,commit
            g = Gifts(gift_name=giftname)
            db.session.add(g)
            db.session.commit()
            if g.gift_id > 0:#see all gifts
                return redirect(url_for('manage_gifts'))
            else:
                flash('It wasnt added, please try again')
                return redirect(url_for('add_gifts'))
    else:
        return redirect('/admin')

@app.route('/admin/edit/<id>')
def edit(id):
    deets = Gifts.query.get(id)
    return render_template('admin/edit_gift.html', deets=deets)


@app.route('/admin/delete/<id>')
def delete(id):
    #delete
    x = db.session.query(Gifts).get(id)
    db.session.delete(x)
    db.session.commit()
    flash('Gift Deleted')
    return "Edit Gift here"

@app.route('/admin/update/', methods=['POST'])
def update_gift():
    #retrieve the form data
    newname = request.form['giftname']
    id = request.form['id']
    newgift = db.session.query(Gifts).get(id)
    newgift.gift_name = newname
    db.session.commit()
    flash('Gift was successfully updated')

    return redirect('/admin/managegifts')

@app.route('/admin/guests/')
def admin_guests():
    guest = Guests.query.all()

    return render_template('admin/guestss.html', guest=guest)
