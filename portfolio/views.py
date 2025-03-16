from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Project

def home(request):
    projects = Project.objects.all().order_by('-created_at')[:3]  # Get only 3 most recent projects
    return render(request, 'home.html', {'projects': projects})

def about(request):
    return render(request, 'about.html')

def projects(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects.html', {'projects': projects})

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Compose email with a more professional format
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
            # Send email using your configured settings
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,  # From email (your Gmail: bigbren480@gmail.com)
                [settings.EMAIL_HOST_USER],  # To email (sending to yourself)
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully! I will get back to you soon.')
            return redirect('contact')
        except Exception as e:
            print(f"Email error: {str(e)}")  # For debugging
            messages.error(request, 'An error occurred while sending your message. Please try again later.')
            
    return render(request, 'contact.html')
