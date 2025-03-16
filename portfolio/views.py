from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
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

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Email body
        email_body = f"""
        New message from portfolio contact form:
        
        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message:
        {message}
        """
        
        try:
            # Send email
            send_mail(
                f'Portfolio Contact: {subject}',
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')
            
    return render(request, 'contact.html')
