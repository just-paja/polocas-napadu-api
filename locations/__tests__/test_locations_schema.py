from django.test import TestCase
from graphene.test import Client
from model_bakery import baker

from api import schema
from fields import VISIBILITY_PRIVATE, VISIBILITY_PUBLIC


class LocationsSchemaTest(TestCase):
    def test_location_list_includes_visible_excludes_private(self):
        baker.make(
            "locations.Location",
            name="Divadlo Bez Hranic",
            description="Malé divadlo v Nuslích",
            visibility=VISIBILITY_PUBLIC,
        )
        baker.make(
            "locations.Location",
            name="Neobyčejná klubovna",
            description="Klubovna Poutníků",
            visibility=VISIBILITY_PRIVATE,
        )
        client = Client(schema.PUBLIC)
        result = client.execute("""{ locationList { name } }""")
        self.assertEqual(
            result, {"data": {"locationList": [{"name": "Divadlo Bez Hranic",},],},}
        )

    def test_usual_place_list_includes_visible_excludes_private(self):
        baker.make(
            "locations.UsualPlace",
            name="Domácí scéna",
            description="Hrajeme tady ...",
            visibility=VISIBILITY_PUBLIC,
            location=baker.make(
                "locations.Location",
                name="Divadlo Bez Hranic",
                description="Malé divadlo v Nuslích",
                visibility=VISIBILITY_PUBLIC,
            ),
        )
        baker.make(
            "locations.UsualPlace",
            name="Tréninky",
            description="Každý týden se zde ...",
            visibility=VISIBILITY_PRIVATE,
            location=baker.make(
                "locations.Location",
                name="Neobyčejná klubovna",
                description="Klubovna Poutníků",
                visibility=VISIBILITY_PRIVATE,
            ),
        )
        client = Client(schema.PUBLIC)
        result = client.execute("""{ usualPlaceList { name } }""")
        self.assertEqual(
            result, {"data": {"usualPlaceList": [{"name": "Domácí scéna",},],},}
        )
