from django.shortcuts import render
from blogs.models import user
from blogs.models import post
from blogs.models import comment
from blogs.models import viewing
from blogs.models import blog
from django.http import HttpResponseRedirect
from blogs.models import followers
from django.http import HttpResponse
from blogs.models import message



def logout(request):
	del request.session['member'] 
	return HttpResponseRedirect("/login")

def login(request):
	error = False
	return render(request,'signin.html' , {"error":error})

def signin(request):
	error = False
	
	email = ""
	password = ""
	if "email" in request.POST  :
	 email = request.POST['email']
	if "password" in request.POST :
		password = request.POST['password']
	try:
		ObjUser = user.objects.get(user_email = email)
		if password != ObjUser.user_password:
			error = True
			return render(request,'signin.html' , {"error":error})
			
	except user.DoesNotExist:
		error = True
		return render(request,'signin.html' , {"error":error})
	
	if len(ObjUser.user_email) == 0 or len(ObjUser.user_password) == 0 :
		error = True
	if error :

		return render(request,'signin.html' , {"error":error})
	else:
		request.session['member'] = user.objects.get(user_email = email)
		return HttpResponseRedirect("bloglist/")

def signupbutton(request):
	errors =  []
	return render(request,"signup.html",{"errors":errors})

def signup(request):
	errors = []
	email = ""
	password = ""
	username = ""
	
	if "email" in request.POST  :
		email = request.POST['email']
		if len(email) == 0 :
			errors.append("Please enter an email")
		elif request.POST.get('email') and '@' not in request.POST['email'] :
			errors.append("Please enter a valid email")
	if 'name' in request.POST :
		username = request.POST['name']
		if len(username) ==0 :
			errors.append("Please enter a username")
	if 'password' in request.POST:
		password = request.POST['password']
		if len(password) ==0 :
			errors.append("Please enter a password")
		elif len(password) < 8 :
				errors.append("Please enter at least 8 character password")	
	
	if len(errors) ==0 :
		user.objects.create(user_email=email , user_password = password , user_name = username)
		request.session['member'] = user.objects.get(user_email = email)
		return HttpResponseRedirect("/bloglist")



	return render(request,'signup.html',{'errors':errors})
		
def profile(request):
	flag = False
	blog_list = blog.objects.all()
	user_id = request.session['member'].id
	Objblog = 0
	try:
		Objblog = blog.objects.get(user_id = user_id)
	except Exception :
		flag = True

	
	
	return render(request,'newsfeed.html' , {"blogs":blog_list , "flag":flag , "blogobj" : Objblog})

def createblogpage(request) :
	error = False
	return render(request,'createblog.html' ,{"error":error})

def createblog(request):
	error = False
	blog_name = ""
	if 'blog_name' in request.POST :
		blog_name = request.POST['blog_name']
	if len(blog_name) ==0 :
			error = True


	if error :
		return render(request,'createblog.html' , {"error" : error})
	else :
		blog.objects.create(blog_name = blog_name , user_id = request.session['member'].id)
		Objblog = blog.objects.get(user_id = request.session['member'].id)
		return HttpResponseRedirect("/bloglist/%s" %Objblog.id)

def blogpage(request , blog_id):
	view_num = visitblog(blog_id , request.session['member'].id)
	posts_list = post.objects.filter(blog_id = blog_id)
	has_blog = False

	try:
		blogobj = blog.objects.get(user_id = request.session['member'].id)
	except Exception:
		has_blog = True
	

	error = False
	flag = False
	user_id = blog.objects.get(id = blog_id).user_id
	user_name = user.objects.get(id = user_id)
	follow_list = followers.objects.filter(user_id = request.session['member'].id)
	try:
		followobj = followers.objects.get(following_id = user_id , user_id = request.session['member'].id)
	except Exception:
		flag = True
	
	if user_id != request.session['member'].id :
		error = True

	return render(request,'blog.html' , {"user_id" : user_id,"has_blog" : has_blog,"flag":flag,"blog_id":blog_id , "posts" : posts_list,"error":error , "view_num" : view_num , "user_name" : user_name , "follow_list":follow_list})

def addpost(request):
	error = False
	return render(request,'Addpost.html',{"error":error})
def addpostbutton(request) :
	error = False
	user_id = request.session['member'].id
	post_text = ""
	if "post_text" in request.POST :
		post_text = request.POST["post_text"]
		if len(post_text) ==0 or post_text.isspace():
			error = True
			return render(request,"Addpost.html",{"error":error})
	blog_id = blog.objects.get(user_id = user_id).id

	post.objects.create(post_text = post_text , user_id = user_id ,blog_id = blog_id)
	return HttpResponseRedirect("bloglist/%s" % blog_id)


def posts(request,post_id):
	
	comment_list = comment.objects.filter(post_id = post_id)
	currentuser_id = request.session['member'].id
	postobj = post.objects.get(id = post_id)
	flag = False
	if postobj.user_id != currentuser_id :
		flag = True
	
	error = False
	if len(comment_list) == 0:
		error = True
	


	return render(request,'posts.html',{"comments":comment_list ,"post":postobj ,  "error":error , "flag":flag ,"user_id" :request.session['member'].id})

def editpost(request,post_id) :
	post_text = post.objects.get(id=post_id).post_text
	return render(request , "editpost.html" , {"post_text":post_text , "post_id" :post_id})
def editpostbutton(request,post_id):
	post_text = request.POST['post_text']
	postobj = post.objects.get(id = post_id)
	postobj.post_text = post_text
	postobj.save()
	blog_id = postobj.blog_id
	return HttpResponseRedirect("/bloglist/%s" % blog_id)
def deletepost(request , post_id) :
	postobj = post.objects.get(id = post_id)
	blog_id = postobj.blog_id
	postobj.delete()
	return HttpResponseRedirect("/bloglist/%s" % blog_id)

def addcomment(request , post_id ) :
	error = False
	return render(request , "Addcomment.html" , {"error":error , "post_id" : post_id} )
def addcommentbutton(request , post_id):
	error = False

	if "comment_text" in request.POST:
		comment_text = request.POST['comment_text']
	else :
		error = True
	user = request.session['member']
	user_id = user.id
	user_name = user.user_name
	

	if len(comment_text) != 0 and not comment_text.isspace():
		comment.objects.create(comment_text=comment_text , user_id = user_id , post_id = post_id , user_name = user_name)
		
		return HttpResponseRedirect("/bloglist/posts/%s" % post_id)
	else :
		error = True
		return render(request,"Addcomment.html" , {"error":error , "post_id" : post_id})

def editcomment(request,comment_id):
	commentobj = comment.objects.get(id = comment_id)
	
	return render(request,"editcomment.html",{"comment_text":commentobj.comment_text , "comment_id":comment_id})

def editcommentbutton(request , comment_id):
	if 'comment_text' in request.POST:
		comment_text = request.POST['comment_text']
		commentobj = comment.objects.get(id = comment_id)
		commentobj.comment_text = comment_text
		commentobj.save()
		return HttpResponseRedirect("/bloglist/posts/%s" % commentobj.post_id)

def deletecomment(request,comment_id):
	commentobj = comment.objects.get(id = comment_id)
	post_id = commentobj.post_id
	commentobj.delete()
	return HttpResponseRedirect("/bloglist/posts/%s" %post_id)

def visitblog(blog_id , user_id):

	viewlist = viewing.objects.filter(blog_id = blog_id , user_id= user_id)

	if len(viewlist) ==0 :
		viewing.objects.create(user_id = user_id , blog_id = blog_id)
	viewlist = viewing.objects.filter(blog_id = blog_id)
	return  len(viewlist)

def following(request , blog_id):
   user_id = request.session['member'].id
   blogobj = blog.objects.get(id = blog_id)
   following_id = blogobj.user_id
   user_name = user.objects.get(id = following_id).user_name 
   followers.objects.create(user_id = user_id , following_id = following_id , following_name = user_name)
   return HttpResponseRedirect("/bloglist/%s" % blog_id)

def userpage(request , user_id) :

	try:
		blogobj = blog.objects.get(user_id = user_id)
	except Exception:
		return HttpResponse("That User has no blog")

	return HttpResponseRedirect("/bloglist/%s" %blogobj.id)

def unfollow(request , blog_id) :
	user_id = blog.objects.get(id = blog_id).user_id
	followobj = followers.objects.get(user_id = request.session['member'].id , following_id = user_id)
	followobj.delete()
	return HttpResponseRedirect("/bloglist/%s" %blog_id)

def sendmessage(request , user_id) :
	error = False
	return render(request,"sendmessage.html" , {"user_id" : user_id , "error" : error})

def sendmessagebutton(request , user_id ) :
	error = False
	message_text = request.POST['message_text']
	from_id = request.session['member'].id
	from_name = request.session['member'].user_name
	to_id = user_id
	if len(message_text) == 0 or message_text.isspace():
		error = True
		return render(request , "sendmessage.html" , {"user_id" :user_id , "error" : error})

	try:
		blog_id = blog.objects.get(user_id = to_id).id
		
	except Exception:
		message.objects.create(user_id = from_id , to_id = to_id , from_name = from_name , message_text = message_text)
		return HttpResponse("Your message is sent, but %s has no blog" % user.objects.get(id = to_id).user_name)
	message.objects.create(user_id = from_id , to_id = to_id , from_name = from_name , message_text = message_text)
	return HttpResponseRedirect("/bloglist/%s" % blog_id)

def deletemessage(request , message_id) :
	messageobj = message.objects.get(id = message_id)
	messageobj.delete()
	return HttpResponseRedirect("/inbox")

def inbox(request) :
	messageobj = message.objects.filter(to_id = request.session['member'].id)
	return render(request,"inbox.html" , {"messages" : messageobj})




	




     

	
	
	


	



 







	





	

