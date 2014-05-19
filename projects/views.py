from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos.collections import Point
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from forms import CreateForm
from models import Project
from osm_api.models import Changeset
import urllib

def index(request):
    if request.user.is_active:
        return HttpResponseRedirect("/project_list/")
    else:
        return render_to_response("index.html", {}, context_instance=RequestContext(request))

@login_required
def project_list(request):
    return render_to_response("project_list.html", {"user": request.user}, context_instance=RequestContext(request))

def project_page(request, project_id):
    data = {}
    # data["lat"] = request.GET.get("lat", "38.90085")
    # data["lng"] = request.GET.get("lng", "-77.02271")

    model_project = Project.objects.get(id=project_id)

    data["state"] = "new"

    # get the state
    changesets = Changeset.objects.filter(project=model_project, parent=None)
    if changesets:
        data["state"] = "created"
        data["changeset"] = changesets[0]

        # list all the edits
        child_changesets = Changeset.objects.filter(project=model_project, parent=changesets[0])
        data["child_changesets"] = child_changesets

    data["proj"] = model_project

    return render_to_response('project.html', data)

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def create_project(request):

    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["project_name"]
            lat_lng = form.cleaned_data["location"]
            pnt = Point(lat_lng["lng"], lat_lng["lat"])
            model_proj = Project.objects.create(name=name, starting_point=pnt, owner=request.user)
            return HttpResponseRedirect('/project/%s/' % model_proj.id)
    else:
        form = CreateForm()
    return render_to_response('create_project.html', {"form": form, "user": request.user}, context_instance=RequestContext(request))

