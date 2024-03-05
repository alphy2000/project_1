from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib import messages 
from .models import *
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
import re

from django.http import JsonResponse,HttpResponse
import random


import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# ------------------- SIGNUP/LOGIN/LOGOUT FUNCTIONS STARTS ---------------------

# User Login

def login(l1):
    if l1.method=='POST':
        u = l1.POST.get('username')
        p =  l1.POST.get('password')
        if u=='admin'and p=='123':
            return redirect(adminindex)

        elif usersignup.objects.filter(username=u).exists():
            usr = usersignup.objects.filter(username=u).first()
            if usr.password == p:
                l1.session['id'] = [usr.id]
                return redirect(index)
            else:
                messages.info(l1,'Incorrect Password',extra_tags="login")
                return redirect(login)

        else:
            messages.info(l1,'Username not found',extra_tags="login")
            return redirect(login)
        
    return render(l1,'login.html')

# Logout page

def logout(l3):
    if 'id' in l3.session:
        l3.session.flush()
        return redirect(index)
    return redirect(index)


# User Signup

def signup(l2):
    if l2.method == 'POST':
        n = l2.POST.get('name')
        e = l2.POST.get('email')
        ph = l2.POST.get('phone')
        u = l2.POST.get('username')
        p = l2.POST.get('password')
        p2 = l2.POST.get('repassword')
        if p == p2:
            if usersignup.objects.filter(username=u).exists():
                messages.info(l2,"Username already exists",extra_tags="signup")
                return redirect(signup) 
            elif usersignup.objects.filter(email=e).exists():
                messages.info(l2,"Email already exists",extra_tags="signup")
                return redirect(signup)  
            else:
                try:
                    y=re.search("(?=.{8,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[~!@#$%^&*?])",p)
                    x=re.findall(r'^[6-9][0-9]{9}',ph)
                    if x==[ph]:
                        if y==None:
                            messages.info(l2,"Password is not strong",extra_tags="signup")
                            return redirect(signup)
                        else:
                            val=usersignup.objects.create(name=n,email=e,phone=ph,username=u,password=p)
                            val.save()  
                            return redirect(login) 
                    else:
                        messages.info(l2,"Not a valid phone number",extra_tags="signup")
                        return redirect(signup)
                except:
                    messages.info(l2,"Invalid input",extra_tags="signup")
        else:
            messages.info(l2,"Password doesn't match",extra_tags="signup")
            return redirect(signup) 

    return render(l2,'login.html')

# ------------------- SIGNUP/LOGIN/LOGOUT FUNCTIONS ENDS ---------------------
##########################



# ------------------- HOME FUNCTIONS STARTS ---------------------

# Main pages

def base(r11):
    if 'id' in r11.session:
        se = r11.session.get('id')
        val = se[0]
        usr = usersignup.objects.filter(id=val).first()
        c = mycart.objects.filter(usr=val).all()
        pro = profilepic.objects.filter(user=usr).first()
        cnt = c.count()
        return render(r11,'base.html',{'cnt':cnt,'usr':usr,'pro':pro})
    return render(r11,'base.html')

def index(r1):
    if 'id' in r1.session:
        se = r1.session.get('id')
        val = se[0]
        usr = usersignup.objects.filter(id=val).first()
        c = mycart.objects.filter(usr=val).all()
        pro = profilepic.objects.filter(user=usr).first()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if len(l) < 3:
                l.append(i)
            else:
                pass
        k=[]
        n=[]
        for i in obj:
            k.append(i)
        k.reverse()
        for j in k:
            if len(n) < 6:
                n.append(j)
            else:
                pass
        return render(r1,'index.html',{'l':l,'n':n,'cnt':cnt,'usr':usr,'pro':pro})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if len(l) < 3:
                l.append(i)
            else:
                pass
        k=[]
        n=[]
        for i in obj:
            k.append(i)
        k.reverse()
        for j in k:
            if len(n) < 6:
                n.append(j)
            else:
                pass
        print(n)
        print(k)
        return render(r1,'index.html',{'l':l,'n':n})

    

# ------------------- HOME FUNCTIONS ENDS ---------------------
##########################



# ------------------- CART FUNCTIONS STARTS ---------------------

# Cart function

def cartt(c1):
    if 'id' in c1.session:
        se = c1.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        cl = {}
        t=0
        for i in c:
            cl[i.products]=[i.quantity,i.id,i.products.discount*i.quantity]
            t=t+(i.products.discount*i.quantity)

        usr = usersignup.objects.filter(id=val).first()
        return render(c1,'cart.html',{"usr":usr,"cl":cl,'cnt':cnt,'t':t})
    return redirect(login)

# Add to Cart function

def addcart(r3,wal=0):
    if 'id' in r3.session:
        se = r3.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        if r3.method == 'POST':
            p = products.objects.filter(id=wal).first()
            usr = usersignup.objects.get(id = val)
            if c:
                f=0
                for i in c:
                    if i.products == p:
                        f=1
                        i.quantity = i.quantity + 1
                        i.save()
                        return redirect(cartt)
                if f==0:
                    val = mycart.objects.create(usr = usr,products = p,quantity = 1,delivered = False)
                    val.save()
                    return redirect(cartt)   
            else:
                val = mycart.objects.create(usr = usr,products = p,quantity = 1,delivered = False)
                val.save()  
                return redirect(cartt)
    return redirect(login)


# Deleting cart items

def deletecart(d1,de):
    if 'id' in d1.session:
        c=mycart.objects.get(id=de)
        c.delete()
        return redirect(cartt)

# Decreasing cart items

def minuscart(d2,de):
    if 'id' in d2.session:
        c=mycart.objects.get(id=de)
        if c.quantity>1:
            c.quantity = c.quantity - 1
            c.save()
        else:
            c.delete()
        return redirect(cartt)

# Increasing cart items

def pluscart(d3,de):
    if 'id' in d3.session:
        c=mycart.objects.get(id=de)
        c.quantity = c.quantity + 1
        c.save()
        return redirect(cartt)


# ------------------- CART FUNCTIONS ENDS ---------------------
##########################



# ------------------- SEARCH FUNCTIONS STARTS ---------------------

# Search page
def searchfn(s):
    if 'id' in s.session:
        se = s.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        if s.method == 'POST':
            sr = s.POST.get('sr')
            l = products.objects.filter(name__icontains = sr)
            return render(s,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
        return render(s,'shop-single.html',{'cnt':cnt,"usr":usr})
    else:
        if s.method == 'POST':
            sr = s.POST.get('sr')
            l = products.objects.filter(name__icontains = sr)
            return render(s,'shop-list.html',{'l':l})
        return render(s,'shop-single.html')



    # if s.method == 'POST':
    #     sr = s.POST.get('sr')
    #     l = products.objects.filter(name__icontains = sr)
    #     return render(s,'shop-list.html',{'l':l})
    # return render(s,'shop-list.html')


# ------------------- SEARCH FUNCTIONS ENDS ---------------------
##########################



# ------------------- CHECKOUT FUNCTIONS STARTS ---------------------

# Checkout page

def checkout(r4):
    if 'id' in r4.session:
        se = r4.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        if c:
            cnt = c.count()
            cl = {}
            t=0
            for i in c:
                cl[i.products]=[i.quantity,i.id,i.products.discount*i.quantity]
                t=t+(i.products.discount*i.quantity)

            usr = usersignup.objects.filter(id=val).first()
            det = profile.objects.filter(user=usr).first()

            return render(r4,'checkout.html',{"usr":usr,"cl":cl,'cnt':cnt,'t':t,"det":det})
    return redirect(cartt)
# Thankyou page

def thanku(r8):
    if 'id' in r8.session:
        se = r8.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        return render(r8,'thankyou.html',{"usr":usr})
    else:
        return render(r8,'thankyou.html')

# ------------------- CHECKOUT FUNCTIONS ENDS ---------------------
##########################



# ------------------- ABOUT AND CONTACT FUNCTIONS STARTS ---------------------

def about(r2):
    if 'id' in r2.session:
        se = r2.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        return render(r2,'about.html',{'cnt':cnt,"usr":usr})
    else:
        return render(r2,'about.html')


def contact(r5):
    if 'id' in r5.session:
        se = r5.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        if r5.method=='POST':
            n=r5.POST.get('name')
            m=r5.POST.get('mobile')
            e=r5.POST.get('email')
            me=r5.POST.get('message')
            l=msg.objects.create(name=n,mobile=m,email=e,message=me)
            l.save()
            return redirect(contact)
        return render(r5,'contact.html',{'cnt':cnt,"usr":usr})
    else:
        return redirect(login)

# ------------------- ABOUT AND CONTACT FUNCTIONS ENDS ---------------------
##########################



# ------------------- SHOP PAGES FUNCTIONS STARTS ---------------------

# Single product

def single(r6,wal):
    if 'id' in r6.session:
        se = r6.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        g=[]
        for i in c:
            g.append(i.products)

        cnt = c.count()
        l=products.objects.filter(id=wal).first()
        return render(r6,'shop-single.html',{'l':l,'cnt':cnt,"usr":usr,'c':c,'g':g})
    else:
        l=products.objects.filter(id=wal).first()
        return render(r6,'shop-single.html',{'l':l})

# Category page

def shop(r7):
    if 'id' in r7.session:
        se = r7.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        g=[]
        for i in c:
            g.append(i.products_id)
        cnt = c.count()
        return render(r7,'shop.html',{'cnt':cnt,"usr":usr,'g':g})
    else:
        return render(r7,'shop.html')

##########################



# Sub pages - Category

def medicines(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        g=[]
        for i in c:
            g.append(i.products_id)
        cnt = c.count()
        l=products.objects.all()
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr,'g':g })
    else:
        l=products.objects.all()
        return render(r10,'shop-list.html',{'l':l})

def diabetes(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='a':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='a':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def health(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='b':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='b':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})
    
def pain(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='c':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='c':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def ayurveda(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='d':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='d':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def homeo(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='e':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='e':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def derma(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='f':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='f':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def oral(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='g':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='g':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def baby(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='h':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='h':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def vitamins(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='i':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='i':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def sports(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='j':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='j':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def family(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='k':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='k':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def supports(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='l':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='l':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})


# ------------------- SHOP PAGES FUNCTIONS ENDS --------------------- 
##########################



# ------------------- ADMIN FUNCTIONS STARTS ---------------------

# Admin dashboard



def adminindex(a2):
    obj = products.objects.all()
    usr = usersignup.objects.all()
    objc = 0
    usrc = 0
    for i in obj:
        objc = objc + 1
    for j in usr:
        usrc = usrc + 1
    return render(a2,'myadmin/index.html',{'objc':objc,'usrc':usrc})

def adminpro(a2):
    obj=products.objects.all()
    return render(a2,'myadmin/products.html',{'obj':obj})

def bs(a2):
    return render(a2,'myadmin/base.html')

def addproduct(a2):
    if a2.method=='POST':
        n=a2.POST.get('name')
        dc=a2.POST.get('description')
        f=a2.POST.get('features')
        p=a2.POST.get('price')
        d=a2.POST.get('discount')
        c=a2.POST.get('category')
        img=a2.FILES.get('img')
        obj = products.objects.create(name=n,price=p,description=dc,features=f,discount=d,category=c,image=img)
        obj.save()
        return redirect(adminpro) 
    return render(a2,'myadmin/add-product.html')

def editproduct(a2,wal):
    obj = products.objects.filter(id=wal).first()
    return render(a2,'myadmin/edit-product.html',{'obj':obj})


def editproduct2(a2,wal):
    obj = products.objects.get(id=wal)
    if a2.method=='POST':
        obj.name=a2.POST.get('name')
        obj.description=a2.POST.get('description')
        obj.features=a2.POST.get('features')
        obj.price=a2.POST.get('price')
        obj.discount=a2.POST.get('discount') 
        obj.category=a2.POST.get('category')
        img = a2.FILES.get('img')
        if img == None:
            obj.save()
        else:
            obj.image=a2.FILES.get('img')
            obj.save()
        return redirect(adminpro)
    return render(a2,'myadmin/edit-product.html',{'obj':obj})

def deleteproduct(a2,wal):
    obj = products.objects.get(id=wal)
    obj.delete()
    return redirect(adminpro)

def userss(a2):
    obj = usersignup.objects.all()
    return render(a2,'myadmin/users.html',{'obj':obj})


def userbookings(a2):
    o = order.objects.all()     
    return render(a2,'myadmin/userbookings.html',{'o':o})

def statusup(r,wal):
    if r.method == "POST":
        st = order.objects.get(id=wal)
        st.status = r.POST.get('status')
        st.save()
        return redirect(userbookings)

def mess1(r):
    l=msg.objects.all()
    return render(r,'myadmin/messages.html',{'l':l})

def reply(r,em):
    l=msg.objects.filter(id=em).first()
    return render(r,"myadmin/replymail.html",{'l':l})
 
def replymail(r,em):
    if r.method=='POST':
        l=msg.objects.filter(id=em).first()
        n=r.POST.get('message')
        try:
            send_mail('Reply from PHARMA', f'{n}','settings.EMAIL_HOST_USER', [l.email],fail_silently=False)
            return redirect(mess1)
        except:
            ms = "NETWORK CONNECTION FAILED"
            return render(r, 'myadmin/replymail.html',{"ms":ms})
        
    return render(r, 'myadmin/replymail.html')

def deletemsg(r,em):
    l=msg.objects.get(id=em)
    l.delete()
    return redirect(mess1)

def adsingle(r6,wal):
    if 'id' in r6.session:
        se = r6.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        l=products.objects.filter(id=wal).first()
        return render(r6,'myadmin/single.html',{'l':l,'cnt':cnt,"usr":usr,'c':c})
    else:
        l=products.objects.filter(id=wal).first()
        return render(r6,'myadmin/single.html',{'l':l})



# Admin dashboard end
 
# ------------------- ADMIN FUNCTIONS ENDS ---------------------


def profileedit(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        pro = profilepic.objects.filter(user=usr).first()
        if r.method == 'POST':
            usr.name = r.POST.get('name')
            usr.email = r.POST.get('email')
            usr.phone = r.POST.get('phone')
            pic = r.FILES.get('img')
            if pic == None:
                usr.save()
            else:
                if pro:
                    pro.user = usr
                    pro.propic = pic
                    usr.save()
                    pro.save()
                else:
                    cr = profilepic.objects.create(user=usr,propic=pic)
                    cr.save()
            return redirect(index)
        return render(r,'profileedit.html',{'usr':usr,'pro':pro,'cnt':cnt})
    return render(r,'profileedit.html')

def change(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        if r.method == 'POST':
            o = r.POST.get('opass')
            n = r.POST.get('npass')
            rp = r.POST.get('rpass')
            if o == usr.password:
                try:
                    y=re.search("(?=.{8,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[~!@#$%^&*?])",n)
                    if y==None:
                        messages.info(r,"Password is not strong")
                        return redirect(change)
                    else:
                        if n==rp:
                            usr.password=n
                            usr.save()
                            return redirect(profileedit)
                        else:
                            messages.info(r,"Password doesnt match")
                            return redirect(change) 
                except:
                    messages.info(r,"Invalid input")
                
            else:
                messages.info(r,"Incorrect old password")
                return redirect(change) 

        return render(r,"changepswd.html",{'usr':usr,'cnt':cnt})

# ------------------- PASSWORD FUNCTIONS STARTS ---------------------


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = usersignup.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try: 
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'password_reset_sent.html')

# def resetpage(r,token):
#     return render(r, 'reset_password.html')

def reset_password(request, token):
    # Verify token and reset the password
    password_reset = PasswordReset.objects.get(token=token)
    usr = usersignup.objects.get(id=password_reset.user_id)
    return render(request, 'reset_password.html',{'token':token})

def reset_password2(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    usr = usersignup.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('repeatpassword')
        if repeat_password == new_password:
            password_reset.user.password = new_password
            password_reset.user.save()
            password_reset.delete()
            return redirect(login)
    return render(request, 'reset_password.html')

# ------------------- PASSWORD FUNCTIONS ENDS ---------------------





# ------------------- PAYMENT FUNCTIONS STARTS ---------------------



def placeorder(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        t=0
        for i in c:
            t=t+(i.products.discount*i.quantity)
        if r.method == 'POST':   
            if r.POST.get('save')=='save':
                fname = r.POST.get('fname')
                lname = r.POST.get('lname')
                email = r.POST.get('email')
                phone = r.POST.get('phone')
                address = r.POST.get('address')
                city = r.POST.get('city')
                state = r.POST.get('state')
                country = r.POST.get('country')
                pincode = r.POST.get('pincode')
                pro = profile.objects.filter(user=usr).first()  
                if pro:
                    
                    pro.fname = r.POST.get('fname')
                    pro.lname = r.POST.get('lname')
                    pro.email = r.POST.get('email')
                    pro.phone = r.POST.get('phone')
                    pro.address = r.POST.get('address')
                    pro.city = r.POST.get('city')
                    pro.state = r.POST.get('state')
                    pro.country = r.POST.get('country')
                    pro.pincode = r.POST.get('pincode')
                    pro.save()
                else:
                    cr = profile.objects.create(user=usr,fname=fname,lname=lname,email=email,phone=phone,address=address,city=city,state=state,country=country,pincode=pincode)
                    cr.save()
                return redirect(placeorder)
            else:
                neworder = order()
                neworder.user = usr
                neworder.fname = r.POST.get('fname')
                neworder.lname = r.POST.get('lname')
                neworder.email = r.POST.get('email')
                neworder.phone = r.POST.get('phone')
                neworder.address = r.POST.get('address')
                neworder.city = r.POST.get('city')
                neworder.state = r.POST.get('state')
                neworder.country = r.POST.get('country')
                neworder.pincode = r.POST.get('pincode')

                neworder.total_price = t

                neworder.payment_mode = r.POST.get('payment_mode')
                neworder.payment_id = r.POST.get('payment_id')

                trackno = 'pharma'+str(random.randint(1111111,9999999))
                while order.objects.filter(tracking_no=trackno) is None:
                    trackno = 'pharma'+str(random.randint(1111111,9999999))
                neworder.tracking_no = trackno
                neworder.save()

                for item in c:
                    orderitem.objects.create(
                        orderdet = neworder,
                        product = item.products,
                        price = item.products.discount,
                        quantity = item.quantity
                    )

                mycart.objects.filter(usr=val).delete()

                messages.success(r, 'Your order has been placed successfully')

                payMode = r.POST.get('payment_mode')
                if payMode == "Razorpay":
                    return JsonResponse({'status':'Your order has been placed successfully'})

        return redirect(checkout)
    

def razorpaycheck(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        t=0
        for i in c:
            t=t+(i.products.discount*i.quantity)

    return JsonResponse({
        'total_price':t
    })

def orderss(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        o = order.objects.all()
        l=[]
        for i in o:
            if i.user==usr:
                l.append(i)
        return render(r,'myorders.html',{'l':l})
    return render(r,'myorders.html')