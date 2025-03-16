from django.core.management.base import BaseCommand
from django.core.files import File
from portfolio.models import Technology, Project
import os
from django.conf import settings
from urllib.request import urlretrieve
import tempfile
import shutil

class Command(BaseCommand):
    help = 'Populates the database with sample projects and technologies'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate database...')

        # Create a temporary directory in the media folder
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        # Create Technologies
        technologies = [
            'Python', 'Django', 'React', 'Node.js', 'TypeScript',
            'Docker', 'AWS', 'PostgreSQL', 'MongoDB', 'Redis',
            'TensorFlow', 'PyTorch', 'Flutter', 'Swift', 'Kotlin'
        ]

        tech_objects = {}
        for tech_name in technologies:
            tech, created = Technology.objects.get_or_create(name=tech_name)
            tech_objects[tech_name] = tech
            if created:
                self.stdout.write(f'Created technology: {tech_name}')

        # Sample project data
        projects_data = [
            {
                'title': 'AI-Powered Chat Application',
                'description': 'A real-time chat application with AI-powered features including sentiment analysis and automatic language translation.',
                'image_url': 'https://picsum.photos/800/600?random=1',
                'github_url': 'https://github.com/example/ai-chat',
                'live_url': 'https://ai-chat-demo.herokuapp.com',
                'technologies': ['Python', 'TensorFlow', 'React', 'MongoDB', 'Redis']
            },
            {
                'title': 'Cloud-Native Microservices Platform',
                'description': 'A scalable microservices architecture built with Docker and Kubernetes, featuring automatic deployment and scaling.',
                'image_url': 'https://picsum.photos/800/600?random=2',
                'github_url': 'https://github.com/example/cloud-platform',
                'live_url': 'https://cloud-platform-demo.com',
                'technologies': ['Docker', 'AWS', 'Node.js', 'PostgreSQL']
            },
            {
                'title': 'Cross-Platform Mobile App',
                'description': 'A feature-rich mobile application built with Flutter, supporting both iOS and Android platforms.',
                'image_url': 'https://picsum.photos/800/600?random=3',
                'github_url': 'https://github.com/example/mobile-app',
                'live_url': 'https://mobile-app-demo.com',
                'technologies': ['Flutter', 'Swift', 'Kotlin']
            },
            {
                'title': 'E-commerce Analytics Dashboard',
                'description': 'A comprehensive analytics dashboard for e-commerce platforms with real-time data visualization.',
                'image_url': 'https://picsum.photos/800/600?random=4',
                'github_url': 'https://github.com/example/analytics-dashboard',
                'live_url': 'https://analytics-demo.com',
                'technologies': ['TypeScript', 'React', 'PostgreSQL', 'Redis']
            },
            {
                'title': 'Machine Learning Pipeline',
                'description': 'An end-to-end machine learning pipeline for data processing, model training, and deployment.',
                'image_url': 'https://picsum.photos/800/600?random=5',
                'github_url': 'https://github.com/example/ml-pipeline',
                'live_url': 'https://ml-pipeline-demo.com',
                'technologies': ['Python', 'PyTorch', 'Docker', 'MongoDB']
            }
        ]

        try:
            # Create projects
            for project_data in projects_data:
                try:
                    # Check if project already exists
                    if not Project.objects.filter(title=project_data['title']).exists():
                        # Create temporary file path
                        temp_image_path = os.path.join(temp_dir, f"temp_image_{project_data['title']}.jpg")
                        
                        # Download image
                        urlretrieve(project_data['image_url'], temp_image_path)

                        # Create project
                        project = Project.objects.create(
                            title=project_data['title'],
                            description=project_data['description'],
                            github_url=project_data['github_url'],
                            live_url=project_data['live_url']
                        )

                        # Add image
                        with open(temp_image_path, 'rb') as img_file:
                            project.image.save(
                                f"project_{project.id}.jpg",
                                File(img_file)
                            )

                        # Add technologies
                        for tech_name in project_data['technologies']:
                            project.technologies.add(tech_objects[tech_name])

                        self.stdout.write(f'Created project: {project.title}')
                        
                        # Clean up temporary image
                        os.remove(temp_image_path)
                    else:
                        self.stdout.write(f'Project already exists: {project_data["title"]}')

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating project {project_data["title"]}: {str(e)}')
                    )

        finally:
            # Clean up temporary directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))