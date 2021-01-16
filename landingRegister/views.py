from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.core.mail import send_mail
from validate_email import validate_email
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from todo.utils import staff_check

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
import threading
from django.db import connection
from django.contrib.auth.models import Group



# Create your views here.

class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


class RegistrationView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        context = {

            'data': request.POST,
            'has_error': False
        }

        company = request.POST.get('company')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        is_already_in_company = 1
        if Group.objects.filter(name=company):
            is_already_in_company = 1
        else:
            g1 = Group(name=company)
            g1. save()

        
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'passwords dont match')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Please provide a valid email')
            context['has_error'] = True

        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email is taken')
                context['has_error'] = True

        except Exception as identifier:
            pass

        try:
            if User.objects.get(username=username):
                messages.add_message(
                    request, messages.ERROR, 'Username is taken')
                context['has_error'] = True

        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, 'auth/register.html', context, status=400)

        user = User.objects.create_user(username=username, email=email, is_staff=is_already_in_company)
        user.set_password(password)
        user.is_active = True
        user.save()

        
        company_id = Group.objects.get(name=company)


        print("company_id: " + str(company_id.id))
        print("user_id: " + str(user.id))

        with connection.cursor() as cursor:
            user_groups_query = """Insert into auth_user_groups(user_id, group_id) 
                                    values ('{}', '{}')""".format(int(user.id), int(company_id.id));
            cursor.execute(user_groups_query)

        current_site = get_current_site(request)

        email_subject = 'Active your Account'
        message = render_to_string('auth/activate.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': generate_token.make_token(user)
                                   })

        email_message =  EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )
        # email_message.send()
        EmailThread(email_message).start()
        messages.add_message(request, messages.SUCCESS, 'account created succesfully')

        return redirect('login')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'account activated successfully')
            return redirect('login')
        return render(request, 'auth/activate_failed.html', status=401)


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Logout successfully')
        return redirect('login')


class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'auth/request-reset-email.html')

    def post(self, request):
        email = request.POST['email']

        if not validate_email(email):
            messages.error(request, 'Please enter a valid email')
            return render(request, 'auth/request-reset-email.html')

        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Reset your Password]'
            message = render_to_string('auth/reset-user-password.html',
                                       {
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                                           'token': PasswordResetTokenGenerator().make_token(user[0])
                                       }
                                       )

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )

            EmailThread(email_message).start()

        messages.success(
            request, 'We have sent you an email with instructions on how to reset your password')
        return render(request, 'auth/request-reset-email.html')


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, 'Password reset link, is invalid, please request a new one')
                return render(request, 'auth/request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            messages.success(
                request, 'Invalid link')
            return render(request, 'auth/request-reset-email.html')

        return render(request, 'auth/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False
        }

        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'passwords should be at least 6 characters long')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'passwords don`t match')
            context['has_error'] = True

        if context['has_error'] == True:
            return render(request, 'auth/set-new-password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(
                request, 'Password reset success, you can login with new password')

            return redirect('login')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Something went wrong')
            return render(request, 'auth/set-new-password.html', context)

        return render(request, 'auth/set-new-password.html', context)


class ContactUsView (View):
    def get(self, request):
        return render(request, 'auth/contactus.html')

def comingsoon(request):
    return render(request, 'auth/comingsoon.html')

@login_required
@user_passes_test(staff_check)
def graphsView(request):
    with connection.cursor() as cursor:
        get_user_id_query = """SELECT id from auth_user where username like '{}'""".format(request.user)
        cursor.execute(get_user_id_query)
        user_id = cursor.fetchall()
        user_id = user_id[0][0]
        # print(user_id)
        get_user_group_id = """select group_id from auth_user_groups where user_id == '{}'""".format(user_id)
        cursor.execute(get_user_group_id)
        user_group = cursor.fetchall()
        user_group = user_group[0][0]
        # print(user_group)
        user_count_query = """SELECT count(user_id) from auth_user_groups where group_id == '{}'""".format(user_group)
        cursor.execute(user_count_query)
        user_count = cursor.fetchall()
        user_count = user_count[0][0]
        # print(user_count)
        all_user_query = """ SELECT COUNT(*) FROM auth_user""".format()
        cursor.execute(all_user_query)
        all_user = cursor.fetchall()
        all_user = all_user[0][0]


        context={
            "user_count": user_count,
            "all_user": all_user,
        }

    return render(request, 'auth/charts.html', context)
