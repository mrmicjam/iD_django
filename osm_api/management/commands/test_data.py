from django.core.management.base import BaseCommand, CommandError
from osm_api.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        model_user = User.objects.all()[0]

        #create the changeset
        model_changeset = Changeset()
        model_changeset.created_by = model_user
        model_changeset.save()

        model_way = Way()
        model_way.changeset = model_changeset
        model_way.save()

        cnt = 0
        model_first_node = None
        for coord in ((-112.0, 33.4), (-111.8, 33.4), (-111.9, 33.2)):
            pnt = Point(*coord)
            #create the node thats part of the triangle
            model_node = Node()
            model_node.changeset = model_changeset
            model_node.geom = pnt
            model_node.save()
            if not model_first_node:
                model_first_node = model_node
            WayNodes.objects.create(way=model_way, node=model_node, idx=cnt)
            cnt += 1

        #close the loop
        WayNodes.objects.create(way=model_way, node=model_first_node, idx=cnt)

        model_way.update_geom()

        model_relation = Relation()
        model_relation.changeset = model_changeset
        model_relation.save()
