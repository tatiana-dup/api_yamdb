import os
import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import MdbUser


class Command(BaseCommand):
    help = 'Import CSV files into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'directory', type=str, help='Directory containing CSV files'
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        directory = kwargs['directory']

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if filename == 'category.csv':
                self.import_categories(filepath)
            elif filename == 'comments.csv':
                self.import_comments(filepath)
            elif filename == 'genre_title.csv':
                self.import_genre_titles(filepath)
            elif filename == 'genre.csv':
                self.import_genres(filepath)
            elif filename == 'review.csv':
                self.import_reviews(filepath)
            elif filename == 'titles.csv':
                self.import_titles(filepath)
            elif filename == 'users.csv':
                self.import_users(filepath)

    def import_categories(self, filepath):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {filepath}')
        )

    def import_comments(self, filepath):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Comment.objects.create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date']
                )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {filepath}')
        )

    def import_genre_titles(self, filepath):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                GenreTitle.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id']
                )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {filepath}')
        )

    def import_genres(self, filepath):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {filepath}')
        )

    def import_reviews(self, filepath):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Review.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']
                )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {filepath}')
        )

    def import_titles(self, filepath):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category']
                )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {filepath}')
        )

    def import_users(self, filepath):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                MdbUser.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {filepath}')
        )
