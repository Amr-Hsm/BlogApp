from django.db import models


class user(models.Model):

	user_name = models.CharField(max_length=50 , unique = True)
	
	user_password = models.CharField(max_length=50)
	user_email = models.CharField(max_length=100, unique=True)
	
	def __unicode__(self):
		return self.user_name

class blog(models.Model):

	blog_name = models.CharField(max_length=50)
	
	user = models.ForeignKey(user)
	



class post(models.Model):

	post_text = models.CharField(max_length=200)
	user = models.ForeignKey(user)
	
	
	blog = models.ForeignKey(blog)
	def __unicode__(self):
		return self.post_text

class comment(models.Model):
	post = models.ForeignKey(post)
	comment_text = models.CharField(max_length=100)
	
	user = models.ForeignKey(user)
	user_name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.comment_text




class viewing(models.Model):
	user = models.ForeignKey(user)
	
	blog = models.ForeignKey(blog)
	
class followers(models.Model) :
	user = models.ForeignKey(user)
	following_id = models.IntegerField(max_length = 100)
	following_name = models.CharField(max_length = 100)

class message(models.Model) :
	user = models.ForeignKey(user)
	from_name = models.CharField(max_length=100)
	message_text = models.CharField(max_length = 500)
	to_id = models.IntegerField(max_length = 100)
	



		

	


# Create your models here.
