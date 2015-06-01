from django.conf.urls import patterns, include, url
from MyPage.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'JH_HomePage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', main_page),
    url(r'^hello/$', hello),
    url(r'^current_datetime/$', current_datetime),

# new user Join
    url(r'^Join/$', Join),
    url(r'^register/$', register),

# login logout
    url(r'^login_page/$', login_page),
    url(r'^login/$', login),
    url(r'^logout/$', logout),

    url(r'^user/$', userInformation),


    url(r'^photo/$', photo),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

# handphone login
    url(r'^mobileRegister/$', mobileRegister),
    url(r'^mobileLogin/$', mobileLogin),

# imageurl
    url(r'^auction/$', auction),

    url(r'^a/$', a),
)

urlpatterns += staticfiles_urlpatterns()
