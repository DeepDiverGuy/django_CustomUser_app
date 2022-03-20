# "CustomUser" app for django projects



# Description:

A minimal Customized User app for django that has Email Verification functionalities by both sending links and OTP Tokens. Key functionalities are:

		- user-registration
		- activating user account upon clicking a link sent to a user's email address
		- login & logout
		- viewing and updating profile
		- changing email address of a user upon a successful OTP verification
		- password-change and password-reset
		- OTP verification
		- deleting a user after a successful OTP verification and password check.
		- using uuid field to identify a user instead of using an insecure pk
		- using email as the username field




# Dependencies:
- pip install django (>=4.0.2)
- pip install django-email-verification (>=0.1.0)
- pip install django-otp (>=1.1.3)



# Installation:
- Just copy-paste or add the "CustomUser" app (CustomUser directory) inside your django project.



# Configurations:

(i) In your project's settings.py, include the followings:

	- Pointing to the Custom User Model:
		AUTH_USER_MODEL = 'CustomUser.user'

	- In the INSTALLED_APPS list, add the followings:	
		'CustomUser.apps.CustomuserConfig',
	    	'django_email_verification',
	    	'django_otp',
	    	'django_otp.plugins.otp_email',

	- In the MIDDLEWARE list:	
		add 'django_otp.middleware.OTPMiddleware' just after the 'django.contrib.auth.middleware.AuthenticationMiddleware'. The sequence is necessary as the author of "django_otp" framework mentioned.

	- Specify the default LOGIN_URL:	
		from django.urls import reverse_lazy
		LOGIN_URL = reverse_lazy('CustomUser:login')

	- Specify the attributes for "django_email_verification" framework to use:

		def verified_callback(user):
		    user.is_active = True
		    user.emaildevice_set.create(user=user, name='Email')

		EMAIL_VERIFIED_CALLBACK = verified_callback
		EMAIL_FROM_ADDRESS = 'webmaster@localhost'
		EMAIL_PAGE_DOMAIN = 'http://localhost:8000/' #'http://mydomain.com/'
		EMAIL_TOKEN_LIFE = 60 * 60
		EMAIL_MAIL_SUBJECT = 'Confirm your email'
		EMAIL_MAIL_HTML = 'CustomUser/dj_e_v_mail_body.html'
		EMAIL_MAIL_PLAIN = 'CustomUser/dj_e_v_mail_body.txt'
		EMAIL_PAGE_TEMPLATE = 'CustomUser/dj_e_v_confirm_template.html'
		
	- You can optionally specify django's own email attributes as per your needs.
	
	- You also can optionally specify "django_otp" attributes (according to the documentation) if you decide not going with the defaults.
	
			
(ii) In urls.py (root), include the followings:

	from django.urls import path, include
	from django_email_verification import urls as django_email_verification_urls

	urlpatterns = [
	    path('user/', include('CustomUser.urls')),
	    path('email/', include(django_email_verification_urls)), # "django_email_verification" uses this path
	]
	

(iii) Lastly, all we have left to do is migration. Go to your projects root directory and type the followings into your terminal:

	python3 manage.py makemigrations
	python3 manage.py migrate
	
	
(iv) A trick: If you want to show the email address where an OTP Token is sent (in the webpage) each time the user clicks "send token"; you can do that just by replacing line 72 of "django_otp.plugins.otp_email.models.py" file:

	message = f"sent to {self.email or self.user.email}"
	
	

# Using the App:

After we've configured the app successfully, we can start the development server from our project's root directory:

	python3 manage.py runserver
	
and start playing around. Also, if you're not using the "django.core.mail.backends.console.EmailBackend" for your email backend, you can start a debugging server in another terminal to catch all the emails that are being sent from your localhost:
	
	python3 -m smtpd -n -c DebuggingServer localhost:1025
	


# Further Works: 
Now, everything should work perfectly. We can Edit and Customize the app as suits best for our projects!



# Issues: 
If you find any issues, please feel free to open one.



# Pull Requests: 
PRs are welcome; especially, if new functionalities are added.
	
	
	


