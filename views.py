from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from .models import Feedback, Register
def index(request):
    if request.method=="POST":
        r = Register(emailid=request.POST["txtemail"],password=request.POST["txtpass"],mobile=request.POST["txtmobile"],fullname=request.POST["txtfname"])
        r.save()
        return render(request,"bootapp/index.html",{"res":"data submitted successfully"})
    return render(request,"bootapp/index.html")

def logincode(request):
      s = Register.objects.filter(emailid=request.POST["txtemail"],password=request.POST["txtpass"])
      if s.count()>0:
        request.session["uid"]=request.POST["txtemail"]
        return redirect('userdash')
      else:
        return HttpResponse("Invalid Userid and Password")  

def services(request):
    return render(request,"bootapp/services.html")
def aboutus(request):
    return render(request,"bootapp/aboutus.html")

def userdash(request):
    if(request.session.has_key('uid')):
      data = Feedback.objects.filter(feedby=request.session["uid"])  # select * from feedback
      if request.method=="POST":
        f = Feedback(feedby=request.session["uid"],feedto=request.POST["ddlfeedto"],feeddesc=request.POST["txtdesc"],feedrate=request.POST['ddlfeedrate'],feeddate=request.POST['txtdate'])
        f.save()
        return render(request,"bootapp/userdash.html",{"res":"data submitted successfully","res1":data})
      return render(request,"bootapp/userdash.html",{"res1":data})   
    else:
        return redirect("/bootapp")       

def finduserdash(request):
    data = Feedback.objects.get(pk=request.GET["q"]) 
    if request.method=="POST":
       data.feedby = request.POST["txtfeedby"]
       data.feedto = request.POST["txtfeedto"]
       data.feeddesc = request.POST["txtdesc"]
       data.feedrate = request.POST["txtrate"]
       data.feeddate = request.POST["txtdate"]
       data.save()
       return redirect('userdash')
   # select * from feedback where id=?q
    return render(request,"bootapp/finduserdash.html",{"res":data})    
def logout(request):
    del request.session['uid']   
    return redirect('/bootapp') 