import json

from django.http import HttpResponse
from . import models


# Create your views here.


def scenic_areas(request):
    area_list = models.ScenicArea.objects.order_by('id')
    result = []
    for area in area_list:
        t = {'id': area.id, 'name': area.name, 'coord': {'latitude': area.latitude, 'longitude': area.longitude}}
        result.append(t)
    data = {'obj': result}
    return HttpResponse(json.dumps(data), content_type='application/json')
