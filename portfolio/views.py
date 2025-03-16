from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.conf import settings
import socket
import smtplib
from .models import Project

def home(request):
    projects = Project.objects.all().order_by('-created_at')[:3]  # Get only 3 most recent projects
    return render(request, 'home.html', {'projects': projects})

def about(request):
    return render(request, 'about.html')

def projects(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects.html', {'projects': projects})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        email_subject = f'New Contact Form Submission: {subject}'
        email_message = f"""
        New message from your portfolio website contact form.
        
        Sender Details:
        ---------------
        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message Content:
        ---------------
        {message}
        
        This email was sent from your portfolio website's contact form.
        """
        
        try:
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            messages.success(request, 'Your message has been sent successfully! I will get back to you soon.')
            return redirect('contact')
            
        except (socket.timeout, socket.gaierror) as e:
            print(f"Socket Timeout Error: {str(e)}")
            messages.error(request, 'Connection timed out. Please try again.')
            
        except smtplib.SMTPServerDisconnected as e:
            print(f"SMTP Server Disconnected: {str(e)}")
            messages.error(request, 'Lost connection to email server. Please try again.')
            
        except smtplib.SMTPException as e:
            print(f"SMTP Error: {str(e)}")
            messages.error(request, 'Email server error. Please try again later.')
            
        except BadHeaderError:
            print("Invalid header found in email")
            messages.error(request, 'Invalid email headers detected. Please try again.')
            
        except Exception as e:
            print(f"Unexpected email error: {str(e)}")
            messages.error(request, 'An unexpected error occurred. Please try again later.')
            
    return render(request, 'contact.html')
