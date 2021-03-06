import requests

from community.git import get_owner
from data.models import Contributor
from django.core.management.base import BaseCommand

org_name = get_owner()
IMPORT_URL = 'https://webservices.' + org_name + '.io/contrib/'


class Command(BaseCommand):
    def import_data(self, contributor):
        login = contributor.get('login', None)
        name = contributor.get('name', None)
        bio = contributor.get('bio', None)
        num_commits = contributor.get('contributions', None)
        issues_opened = contributor.get('issues', None)
        reviews = contributor.get('reviews', None)

        try:
            c, created = Contributor.objects.get_or_create(
                login=login,
                name=name,
                bio=bio,
                num_commits=num_commits,
                issues_opened=issues_opened,
                reviews=reviews
            )
            if created:
                c.save()
                print('\nContributor, {}, has been saved.'.format(c))
        except Exception as ex:
            print('\n\nSomething went wrong saving this contributor: {}\n{}'
                  .format(login, str(ex)))

    def handle(self, *args, **options):
        """
        Makes a GET request to the  API.
        """
        headers = {'Content-Type': 'application/json'}
        response = requests.get(
            url=IMPORT_URL,
            headers=headers,
        )

        response.raise_for_status()
        data = response.json()

        for contributor in data:
            self.import_data(contributor)
