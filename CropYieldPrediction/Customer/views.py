from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method=="POST":
        n=request.POST['name']
        m=request.POST['mail']
        p1=request.POST['psw1']
        p2=request.POST['psw2']
        if p1==p2:
            if User.objects.filter(username=n).exists():
                messages.info(request,"Username Exists")
                return render(request, "register.html")
            elif User.objects.filter(email=m).exists():
                messages.info(request,"Email Exists")
                return render(request, "register.html")
            else:
                user=User.objects.create_user(username=n,email=m,password=p2)
                user.save()
            return redirect('login')
        else:
            messages.info(request,"Password Not Matched")
            return render(request, "register.html")
    return render(request, 'register.html')

def login(request):
    if request.method=="POST":
        n=request.POST['name']
        p2=request.POST['psw2']
        user=auth.authenticate(username=n,password=p2)
        if user is not None:
            auth.login(request,user)
            return redirect('/customer/index')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,"login.html")
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/customer/index')

def crop_data(request):
    if request.method=="POST":
        area=request.POST['area']
        element=request.POST['element']
        item=request.POST['item']
        year=int(request.POST['year'])
        unit=request.POST['unit']
        from sklearn.preprocessing import LabelEncoder
        l=LabelEncoder()
        area1=l.fit_transform([area])
        element1=l.fit_transform([element])
        item1=l.fit_transform([item])
        unit1=l.fit_transform([unit])
        import pandas as pd
        df=pd.read_csv(r"static/dataset/crop_data.csv")
        print(df.head())
        print(df.isnull().sum())
        print(df.dropna(inplace=True))
        df=df.drop("Domain",axis=1)
        print(df.head())
        area=l.fit_transform(df["Area"])
        element=l.fit_transform(df["Element"])
        item=l.fit_transform(df["Item"])
        unit=l.fit_transform(df["Unit"])
        df=df.drop(["Area","Element","Item","Unit"],axis=1)
        df["Area"]=area
        df["Element"]=element
        df["Item"]=item
        df["Unit"]=unit
        print(df.head())
        x=df.drop("Value",axis=1)
        y=df["Value"]
        import matplotlib.pyplot as plt
        plt.plot(df["Year"],df["Value"])
        plt.show()
        from sklearn.linear_model import LinearRegression
        reg=LinearRegression()
        reg.fit(x,y)
        import numpy as np
        data=np.array([area1,element1,item1,year,unit1])
        prediction=reg.predict(data)
        print(prediction)
        return render(request,"predict.html",{"area":area,"element":element,"item":item,"year":year,"unit":unit,"prediction":prediction})
    return render(request,"cropdata.html")

def predict(request):
    return render(request,"predict.html")