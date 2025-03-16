# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your email provider's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = 'your-app-password'  # Your email password or app-specific password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
CONTACT_EMAIL = 'your-email@gmail.com'  # Email where you want to receive contact form messages