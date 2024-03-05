"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.index,name="index"),
    path('base',views.base),

    path('about',views.about,name="about"),

# ------------------- CART URLS START ---------------------

    path('cartt',views.cartt,name="cartt"),
    path('single/addcart/<wal>',views.addcart,name="addcart"),

    path('deletecart/<de>',views.deletecart,name="deletecart"),
    path('minuscart/<de>',views.minuscart,name="minuscart"),
    path('pluscart/<de>',views.pluscart,name="pluscart"),

# ------------------- CART URLS END ---------------------

    path('searchfn',views.searchfn,name="searchfn"),



    path('checkout',views.checkout,name="checkout"),
    path('contact',views.contact,name="contact"),
    path('single/<wal>',views.single,name="single"),
    path('shop',views.shop,name="shop"),
    path('thanku',views.thanku,name="thanku"),
    path('login',views.login,name="login"),
    path('signup',views.signup,name="signup"),
    path('logout',views.logout,name="logout"),


# ------------------- ADMIN PAGE STARTS ---------------------

    path('admini',views.adminindex,name="admini"),
    path('adminpro',views.adminpro,name="adminpro"),
    path('bs',views.bs,name="bs"),
    path('addproduct',views.addproduct,name="addproduct"),
    path('adsingle/editproduct/<wal>',views.editproduct,name="editproduct"),
    path('adsingle/editproduct/editproduct2/<wal>',views.editproduct2,name="editproduct2"),
    path('adsingle/deleteproduct/<wal>',views.deleteproduct,name="deleteproduct"),
    path('userss',views.userss,name="userss"),
    path('userbookings',views.userbookings,name="userbookings"),
    path('adsingle/<wal>',views.adsingle,name="adsingle"),
    path('statusup/<wal>',views.statusup,name="statusup"),


# ------------------- ADMIN PAGE ENDS ---------------------

###########################################################


# ------------------- SUB PAGES STARTS ---------------------

    path('medicines',views.medicines,name="medicines"),
    path('diabetes',views.diabetes,name="diabetes"),
    path('health',views.health,name="health"),
    path('pain',views.pain,name="pain"),
    path('ayurveda',views.ayurveda,name="ayurveda"),
    path('homeo',views.homeo,name="homeo"),
    path('derma',views.derma,name="derma"),
    path('oral',views.oral,name="oral"),
    path('baby',views.baby,name="baby"),
    path('vitamins',views.vitamins,name="vitamins"),
    path('sports',views.sports,name="sports"),
    path('family',views.family,name="family"),
    path('supports',views.supports,name="supports"),


#__________________PROFILE EDIT_____________________
    
    path("proedit",views.profileedit,name="proedit"),
    path("change",views.change,name="change"),


#________________FORGET PASSWORD______________________

    path("forgot",views.forgot_password,name="forgot"),
    path("reset/<token>",views.reset_password,name="reset"),
    path("reset/reset2/<token>",views.reset_password2,name="reset2"),


#_________________MESSAGES__________________________

    path('messeges',views.mess1,name='messages'),
    path('reply/<em>',views.reply,name='reply'),
    path('reply/replymail/<em>',views.replymail,name='replymail'),
    path('deletemsg/<em>',views.deletemsg,name='deletemsg'),

 
 #__________________ORDER___________________________

    path('place-order', views.placeorder, name='placeorder'),
    path('proceed-to-pay', views.razorpaycheck, name='proceed-to-pay'),
    path('myorder', views.orderss, name='myorder'),
    
    


   
# ------------------- SUB PAGES ENDS ---------------------


]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
