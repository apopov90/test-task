#encoding: utf-8
import json

from django.views.generic.simple import direct_to_template
from django.db.models import get_app, get_models, get_model, IntegerField, \
    DateField, CharField, AutoField
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import ModelForm


def Index(request):
    """

    Index page
    """
    app = get_app('test1')
    models_ = get_models(app)
    return direct_to_template(
        request,
        'index.html',
        locals()
    )


def LoadModel(request):
    """

    Load model structure and content via ajax
    """
    model_ = get_model("test1", request.GET.get('model'))
    struct = [
        {
            'name': x.verbose_name,
            'model_field': x.name,
            'date': isinstance(x, DateField)
        }
        for x in filter(lambda f: isinstance(f, (
            IntegerField, CharField, DateField, AutoField
        )), model_._meta.fields)
    ]
    return HttpResponse(
        json.dumps(
            dict(
                structure=struct,
                content=list(model_.objects.values())
            ),
            cls=DjangoJSONEncoder
        ),
        content_type="application/json"
    )


def UpdateModel(request):
    """

    Update model via ajax
    """
    model_ = get_model("test1", request.GET.get('model'))

    class Meta:
        fields = (request.GET.get('field'), )
        model = model_

    model_form = type('dynamic_update', (ModelForm,), {'Meta': Meta})
    instance_ = model_.objects.get(id=request.GET.get('id'))
    upd_ = model_form(
        {request.GET.get('field'): request.GET.get('value')},
        instance=instance_
    )
    if upd_.is_valid():
        upd_.save()
        return HttpResponse(json.dumps({
            'status': "OK",
        }), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            'status': upd_.errors,
        }), content_type="application/json")


def AddNew(request):
    """

    Add new entry via ajax
    """
    model_ = get_model("test1", request.GET.get('model'))

    class Meta:
        model = model_

    model_form = type('dynamic_update', (ModelForm,), {'Meta': Meta})
    upd_ = model_form(request.GET)
    if upd_.is_valid():
        instance_ = upd_.save()
        return HttpResponse(json.dumps({
            'status': "OK",
            'id': instance_.id
        }), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            'status': upd_.errors,
        }), content_type="application/json")
