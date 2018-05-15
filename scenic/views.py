import json

from django.http import HttpResponse

from form import models as fmodels
from . import models

from .classification import classify as classifier

# Create your views here.

classifier.initial()


def get_spot_id(area_id, spot_names):
    area = models.ScenicArea.objects.get(id=area_id)

    if not area:
        return None

    spots = models.ScenicSpot.objects.filter(area=area)
    spot_id_list = []
    for name in spot_names:
        for spot in spots:
            if name == spot.name:
                spot_id_list.append(spot.id)
                break

    return spot_id_list


def area_detail(request, area_id):
    data = {'err': '景区不存在'}
    area = models.ScenicArea.objects.get(id=area_id)

    if not area:
        return HttpResponse(json.dumps(data), content_type='application/json')

    l = models.ScenicSpot.objects.filter(area=area)
    spots = []
    for spot in l:
        spots.append({'id': spot.id, 'name': spot.name})
    l = fmodels.AreaScore.objects.filter(area=area)
    score_sum = 0
    for score in l:
        score_sum += score.score
    if len(l):
        score = score_sum / len(l)
    else:
        score = 0
    result = {'id': area.id, 'name': area.name, 'spot_list': spots, 'score': score, 'about': area.about,
              'coord': {'latitude': area.latitude, 'longitude': area.longitude}}
    data = {'obj': result}
    return HttpResponse(json.dumps(data), content_type='application/json')


def spot_detail(request, spot_id):
    data = {'err': '景点不存在'}
    spot = models.ScenicSpot.objects.get(id=spot_id)

    if not spot:
        return HttpResponse(json.dumps(data), content_type='application/json')

    result = {'id': spot.id, 'name': spot.name, 'about': spot.about,
              'area_id': spot.area.id, 'area_name': spot.area.name}
    data = {'obj': result}
    return HttpResponse(json.dumps(data), content_type='application/json')


def area_and_spot(request, spot_id):
    data = {'err': '景点不存在'}
    spot = models.ScenicSpot.objects.get(id=spot_id)

    if not spot:
        return HttpResponse(json.dumps(data), content_type='application/json')

    result = {'area': {'id': spot.area.id, 'name': spot.area.name, 'about': spot.area.about},
              'spot': {'id': spot.id, 'name': spot.name, 'about': spot.about}}
    data = {'obj': result}
    return HttpResponse(json.dumps(data), content_type='application/json')


def area_list(request):
    areas = models.ScenicArea.objects.order_by('id')
    result = []
    for area in areas:
        t = {'id': area.id, 'name': area.name, 'coord': {'latitude': area.latitude, 'longitude': area.longitude}}
        result.append(t)
    data = {'obj': result}
    return HttpResponse(json.dumps(data), content_type='application/json')


def spot_list(request, area_id):
    spots = models.ScenicSpot.objects.filter(area__id=area_id).order_by('id')
    result = []
    for spot in spots:
        t = {'id': spot.id, 'name': spot.name, 'area_id': spot.area.id}
        result.append(t)
    data = {'obj': result}
    return HttpResponse(json.dumps(data), content_type='application/json')


def upload_image(request, area_id):
    data = {'err': 'no image recived'}
    if request.method != 'POST':
        return HttpResponse(json.dumps(data), content_type='application/json')

    images = request.FILES.get('img')
    image = list(images.chunks())[0]

    # with open(images.name, 'wb') as file:
    #    file.write(image)

    names, probs = classifier.classify_top_n(image, 4)
    new_probs = []
    for prob in probs:
        new_probs.append(int(prob * 100))
    id = get_spot_id(area_id, names)
    print(names)
    print(new_probs)
    print(id)
    result = {'names': names, 'probs': new_probs, 'id': id}
    data = {'obj': result}
    return HttpResponse(json.dumps(data), content_type='application/json')