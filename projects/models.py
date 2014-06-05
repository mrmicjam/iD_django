from django.contrib.gis.db import models
from django.contrib.auth.models import User
import uuid

class Project(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name="projects")
    starting_point = models.PointField(srid=4326, blank=True, null=True)

    objects = models.GeoManager()

    def set_main_changeset(self, model_changeset):
        if model_changeset.project != self:
            raise Exception("Changeset doesn't belong to this project.")

        # Uncheck is_main for all model_changesets
        for o_changeset in self.changesets.all():
            o_changeset.is_main = False
            o_changeset.save()
        model_changeset.is_main = True
        model_changeset.save()

    def get_main_changeset(self):
        chngsets = self.changesets.filter(is_main=True)
        if chngsets:
            return chngsets[0]
        else:
            return None


class UserToProject(models.Model):
    proj = models.ForeignKey(Project, related_name="members")
    user = models.ForeignKey(User, blank=True, null=True, related_name="subscribed_projects")
    dt_invited = models.DateTimeField(auto_now_add=True)
    invitation_email = models.EmailField()
    key = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = str(uuid.uuid4())
        super(UserToProject, self).save(*args, **kwargs)


class ProjectComment(models.Model):
    proj = models.ForeignKey(Project, related_name="comments")
    user = models.ForeignKey(User, blank=True, null=True, related_name="comments")
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()


