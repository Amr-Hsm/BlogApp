from django.conf.urls import patterns, include, url

from blogs import views
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'trial.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$' , views.login, name='login'),
    url(r'^signin$' , views.signin, name = 'signin'),
    url(r'^signup$',views.signupbutton,name = 'signupbutton'),
    url(r'^profile$',views.signup,name = 'signup'),
    url(r'^bloglist/$',views.profile,name = 'profile'),
    url(r'^createblog/$' , views.createblogpage , name = 'createblogpage'),
    url(r'^createblogpage$',views.createblog,name = 'createblog'),
    url(r'^bloglist/(?P<blog_id>\d+)$' , views.blogpage , name = 'blogpage'),
    url(r'^posts/add$' , views.addpost,name='addpost'),
    url(r'^addpost$' , views.addpostbutton , name = 'addpostbutton'),
    url(r'^bloglist/posts/(?P<post_id>\d+)$' , views.posts , name = 'posts'),
    url(r'^(?P<post_id>\d+)/addcomment$' , views.addcomment , name = "addcomment"),
    url(r'^addcomment/(?P<post_id>\d+)$', views.addcommentbutton , name = "addcommentbutton"),
    url(r'^(?P<post_id>\d+)/editpost$' , views.editpost , name='editpost'),
    url(r'^editpost/(?P<post_id>\d+)$' , views.editpostbutton,name = "editpostbutton"),
    url(r'^(?P<post_id>\d+)/deletepost$' , views.deletepost , name = "deletepost"),
    url(r'^(?P<comment_id>\d+)/editcomment$',views.editcomment,name= "editcomment"),
    url(r'^editcomment/(?P<comment_id>\d+)$',views.editcommentbutton,name = "editcommentbutton"),
    url(r'^(?P<comment_id>\d+)/deletecomment$' , views.deletecomment,name="deletecomment"),
    url(r'^logout$',views.logout,name="logout"),
    url(r'^user/(?P<user_id>\d+)$',views.userpage , name = "userpage"),
    url(r'^follow/(?P<blog_id>\d+)$' , views.following , name = "following"),
    url(r'^unfollow/(?P<blog_id>\d+)$' , views.unfollow , name = "unfollow"),
    url(r'^inbox$',views.inbox,name = "inbox"),
    url(r'^sendmessage/(?P<user_id>\d+)$', views.sendmessage,name = "sendmessage"),
    url(r'^(?P<user_id>\d+)/sendmessage$' , views.sendmessagebutton , name = "sendmessagebutton"),
    url(r'^deletemessage/(?P<message_id>\d+)$',views.deletemessage,name = "deletemessage"),




 



    
)
