from datetime import datetime

import enum
from weddingapp import db 

class Payment_status(enum.Enum):
    Paid = "Paid"
    Pending = 'Pending'
    Failed = 'Failed'

class Guests(db.Model): 
    guest_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    guest_fname =db.Column(db.String(50), nullable=False)
    guest_lname =db.Column(db.String(50), nullable=False)
    guest_email=db.Column(db.String(80), nullable=False)
    guest_image= db.Column(db.String(80), nullable=False)
    guest_pwd =db.Column(db.String(100), nullable=False)
    guest_regdate=db.Column(db.DateTime(), default=datetime.utcnow())
    
	
class Gifts(db.Model): 
    gift_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    gift_name =db.Column(db.String(50), nullable=False) 

class Admin(db.Model):
    #columname=db.Column(db.datatype())
    admin_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    admin_name =db.Column(db.String(50), nullable=False)
    admin_username =db.Column(db.String(50), nullable=False)
    admin_pwd =db.Column(db.String(30), nullable=False)

class Uniform(db.Model):
    #columname=db.Column(db.datatype())
    uni_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uni_name =db.Column(db.String(50), nullable=False)
    uni_price =db.Column(db.Float(), nullable=False)

# class Guest_gift(db.Model):
#     g_giftid = db.Column(db.Integer(), db.ForeignKey('gifts.gift_id'))
#     g_guestid =db.Column(db.Integer(), db.ForeignKey('guests.guest_id')) 
    


class Guest_gift(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_giftid = db.Column(db.Integer(), db.ForeignKey('gifts.gift_id'))
    g_guestid =db.Column(db.Integer(), db.ForeignKey('guests.guest_id')) 

    #set relationship
    #Relationship 1: When I am on Gifts table and want to know the guests that brought a particular gift, I will check inside variable 'dguests', when I am on this table (Guest_gift) and I want to know the details of a gift, I can check gift_deets.
    
    #Relationship 2: When I am on Guests table and I want to know the gifts brought by a particular guest, I will see it via variable 'dgifts' and When I am on this table (Guest_gift) and I want to know the details of a particular Guest, I will check guest_deets  
    gift_deets = db.relationship("Gifts", backref="dguests")
    guest_deets = db.relationship("Guests", backref="dgifts")


class Contact(db.Model):
    con_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    con_fullname = db.Column(db.String(50), nullable=True)
    con_email = db.Column(db.String(50), nullable=True) 
    con_message = db.Column(db.Text(), nullable=True)
    con_date = db.Column(db.DateTime(), default=datetime.utcnow())

class Comment(db.Model):
    comment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    comment_guest_id =db.Column(db.Integer(),db.ForeignKey('guests.guest_id'), nullable=False)
    comment_content =db.Column(db.String(100), nullable=False)
    comment_date=db.Column(db.DateTime(), default=datetime.utcnow())

class State(db.Model):
    state_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_name = db.Column(db.String(100), nullable=False)

class Lga(db.Model):
    lga_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_id = db.Column(db.Integer(),db.ForeignKey('State.state_id'), nullable=False)
    lga_name = db.Column(db.String(100), nullable=False)

class Orders(db.Model):
    order_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    order_ref = db.Column(db.String(100), nullable=False)
    order_totalamt = db.Column(db.Float(), nullable=True)
    order_by = db.Column(db.Integer(),db.ForeignKey('guests.guest_id'))
    order_status = db.Column(db.Enum('Completed','Pending'), nullable=False)
    order_date=db.Column(db.DateTime(), default=datetime.utcnow())

class Order_details(db.Model):
    det_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    det_orderid = db.Column(db.Integer(),db.ForeignKey('orders.order_id'))
    det_itemid = db.Column(db.Integer(),db.ForeignKey('uniform.uni_id'))
    det_itemprice = db.Column(db.Float(),nullable=False)

class Payment(db.Model):
    pay_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    pay_orderid = db.Column(db.Integer(),db.ForeignKey('orders.order_id'))
    pay_guestid = db.Column(db.Integer(),db.ForeignKey('guests.guest_id'))
    pay_amt = db.Column(db.Float(), nullable=False)
    pay_date = db.Column(db.DateTime(), default=datetime.utcnow())
    pay_status = db.Column(db.Enum(Payment_status))
    pay_mode = db.Column(db.String(200), nullable=True)
    pay_feedback = db.Column(db.String(200),nullable=True)

