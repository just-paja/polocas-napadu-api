from django.test import TestCase
from graphene.test import Client
from model_mommy import mommy

from api import schema
from fields import VISIBILITY_PRIVATE, VISIBILITY_PUBLIC

class ShowsSchemaTest(TestCase):
    def test_list_shows_includes_visible(self):
        show_type = mommy.make('shows.ShowType', name='Představení', visibility=VISIBILITY_PUBLIC)
        show_location = mommy.make(
            'locations.Location',
            name='Divadlo Bez Hranic',
            visibility=VISIBILITY_PUBLIC,
        )
        mommy.make('shows.Show',
            name='Test show',
            location=show_location,
            visibility=VISIBILITY_PUBLIC,
            show_type=show_type,
        )

        client = Client(schema.PUBLIC)
        result = client.execute('''{ listShows { name } }''')
        self.assertEqual(result, {
            'data': {
                'listShows': [
                    {
                        'name': 'Test show',
                    },
                ],
            },
        })

    def test_list_shows_excludes_private(self):
        show_type = mommy.make('shows.ShowType', name='Představení', visibility=VISIBILITY_PUBLIC)
        show_location = mommy.make(
            'locations.Location',
            name='Divadlo Bez Hranic',
            visibility=VISIBILITY_PUBLIC,
        )
        mommy.make('shows.Show',
            name='Test show',
            location=show_location,
            visibility=VISIBILITY_PRIVATE,
            show_type=show_type,
        )

        client = Client(schema.PUBLIC)
        result = client.execute('''{ listShows { name } }''')
        self.assertEqual(result, {
            'data': {
                'listShows': [],
            },
        })
