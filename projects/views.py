from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from forms import CreateForm
import urllib

def project_page(request):
    data = {}
    data["lat"] = request.GET.get("lat", "38.90085")
    data["lng"] = request.GET.get("lng", "-77.02271")
    return render_to_response('index.html', data)

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

def create_project(request):

    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["project_name"]
            lat_lng = form.cleaned_data["location"]
            return HttpResponseRedirect('/project/?%s' % urllib.urlencode(lat_lng))
    else:
        form = CreateForm()
    return render_to_response('create_project.html', {"form": form, "user": request.user}, context_instance=RequestContext(request))

