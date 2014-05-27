from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos.collections import Point
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, RequestContext
from forms import CreateForm, InvitationForm, CommentForm
from models import Project, ProjectComment
from osm_api.models import Changeset
from emailer import invite_people as email_people
from django.http import HttpResponse
import json

def index(request):
    if request.user.is_active:
        return HttpResponseRedirect("/project_list/")
    else:
        return render_to_response("index.html", {}, context_instance=RequestContext(request))

@login_required
def project_list(request):
    return render_to_response("project_list.html", {"user": request.user}, context_instance=RequestContext(request))

@login_required
def project_page(request, project_id):
    data = {
        "state": "new",
        "is_owner": False
    }

    model_project = Project.objects.get(id=project_id)
    if model_project.owner != request.user:
        if not model_project.members.filter(user=request.user):
            key = request.GET.get("key", None)
            invites = model_project.members.filter(key=key).filter(user__isnull=True)
            if not invites:
                # isn't a member and doesn't have an invite
                raise Http404()
            model_invite = invites[0]
            model_invite.user = request.user
            model_invite.save()

    if request.user == model_project.owner:
        data["is_owner"] = True

    # get the state
    project_changeset = model_project.get_main_changeset()
    if project_changeset:
        data["state"] = "created"
        data["changeset"] = project_changeset

        # list all the edits that the user didn't make, the lastest changeset per user
        li_owners = []
        li_return_child_changesets = []
        child_changesets = Changeset.objects.filter(project=model_project).exclude(created_by=model_project.owner).order_by("-timestamp")
        for child_changeset in child_changesets:
            chng_owerner = child_changeset.created_by
            if chng_owerner.id not in li_owners:
                li_owners.append(chng_owerner.id)
                li_return_child_changesets.append(child_changeset)

        data["child_changesets"] = li_return_child_changesets

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

@login_required
def invite_people(request, project_id):
    # TODO: verify user is owner of the project

    model_project = Project.objects.get(id=int(project_id))

    if request.method == "POST":
        form = InvitationForm(request.POST)
        if form.is_valid():
            emails = form.cleaned_data["emails"]
            email_people(model_project, emails)
            return render_to_response('email_success.html', {"li_emails": emails, "proj": model_project}, context_instance=RequestContext(request))
    else:
        form = InvitationForm()
    return render_to_response('invite_people.html', {"form": form}, context_instance=RequestContext(request))


def return_json(func):
    def inner(*args, **kwargs):
        data = func(*args, **kwargs)
        kwargs = {'content_type': 'text/json'}
        return HttpResponse(json.dumps(data), **kwargs)
    return inner


@login_required
@return_json
def post_comment(request, project_id):
    dct_return = {
        "status": "error",
        "data": ""
    }

    model_project = Project.objects.get(id=int(project_id))

    if model_project.owner != request.user and not model_project.members.filter(user=request.user):
        dct_return["data"] = "Not authorized"
        return dct_return

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            ProjectComment.objects.create(proj=model_project, user=request.user, comment=comment)
    else:
        form = InvitationForm()

    dct_return["status"] = "success"
    dct_return["data"] = form.as_table()
    return dct_return


@login_required
@return_json
def get_comments(request, project_id):
    dct_return = {
        "status": "error",
        "data": ""
    }

    model_project = Project.objects.get(id=int(project_id))

    if model_project.owner != request.user and not model_project.members.filter(user=request.user):
        dct_return["data"] = "Not authorized"
        return dct_return

    li_comments = []
    for comment in model_project.comments.all().order_by("timestamp"):
        li_comments.append({"user": comment.user.username,
                            "timestamp": comment.timestamp.strftime("%m-%d-%Y"),
                            "comment": comment.comment})
    dct_return["status"] = "success"
    dct_return["data"] = li_comments
    return dct_return
