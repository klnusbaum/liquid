from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.db import IntegrityError
from intranet.models import Member, Group, GroupMember
from intranet.group_manager.forms import GroupForm, GroupMemberFormSet
from utils.group_decorator import group_admin_required, specific_group_admin_required
import string

# Create your views here.
def main(request):
   if not request.user.is_top4():
      groups = Group.objects.filter(members=request.user,membership__is_admin=True)
   else:
      groups = Group.objects.all()
   
   return render_to_response('intranet/group_manager/main.html',{"section":"intranet","page":'group','groups':groups},context_instance=RequestContext(request))

@group_admin_required(['Top4'])
def new(request):
  if request.method == 'POST': # If the form has been submitted...
      form = GroupForm(request.POST) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
          form.save()
          return HttpResponseRedirect('/intranet/group') # Redirect after POST
  else:
      form = GroupForm() # An unbound form

  return render_to_response('intranet/group_manager/form.html',{
      'form': form,
      "section":"intranet",
      "page":'group',
      "page_title":"Create new Group"
      },context_instance=RequestContext(request))

@specific_group_admin_required('id')
def edit(request,id):
  g = Group.objects.get(id=id)
  forms = GroupMemberFormSet(instance=g)
  if request.method == 'POST': # If the form has been submitted...
      form = GroupForm(request.POST,instance=g) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
          form.save()
          return HttpResponseRedirect('/intranet/group') # Redirect after POST
  else:
    form = GroupForm(instance=g)

  
  return render_to_response('intranet/group_manager/form.html',{
    "form":form,
    "section":"intranet",
    "page":'group',
    "page_title":"Edit Group",
    },context_instance=RequestContext(request))

@specific_group_admin_required('id')
def manage(request,id):
  saved = False
  g = Group.objects.get(id=id)
  if request.method == 'POST': # If the form has been submitted...
    forms = GroupMemberFormSet(request.POST,instance=g)
    if forms.is_valid(): # All validation rules pass
      forms.save()
      saved = True
  else:
    forms = GroupMemberFormSet(instance=g)

  return render_to_response('intranet/group_manager/manage.html',{
    "section":"intranet",
    "page":'group',
    "group":g,
    "forms":forms,
    "saved":saved
    },context_instance=RequestContext(request))

@specific_group_admin_required('id')
def add(request,id):
  g = Group.objects.get(id=id)
  added = []
  badid = []
  duplicate = []
  members = Member.objects.filter(status='active')
  if request.method == 'POST':
    netids = [i.strip() for i in string.split(request.POST['netids'],",")]
    for i in netids:
      if len(i) > 0:
        try:
          m = Member.objects.get(username=i)
          gm = GroupMember(member=m,group=g)
          gm.save()
          added.append(m)
        except Member.DoesNotExist:
          badid.append(i)
        except IntegrityError:
          duplicate.append(m)


  return render_to_response('intranet/group_manager/add.html',{
    "section":"intranet",
    "page":'group',
    "group":g,
    "added": added,
    "badid": badid,
    "duplicate": duplicate,
    "members": members
    },context_instance=RequestContext(request))
