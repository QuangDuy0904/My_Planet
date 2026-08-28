from django.http import HttpResponse
from django.template import loader
from .models import Planet

def planet(request):
  myplanet = Planet.objects.all().values()
  template = loader.get_template('all_planet.html')
  context = {
    'myplanet': myplanet,
  }
  return HttpResponse(template.render(context, request))

def details(request, id):
  myplanet = Planet.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'myplanet': myplanet,
  }
  return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def testing(request):
  template = loader.get_template('template.html')
  mydata = Planet.objects.all().values()
  mydata = Planet.objects.values_list('firstname')
  context = {
   'myplanets': mydata, 
   'fruits': ['Apple', 'Banana', 'Cherry'],  
  }
  return HttpResponse(template.render(context, request))