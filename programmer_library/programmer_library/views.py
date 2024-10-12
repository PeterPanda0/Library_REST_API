from django.http import HttpResponseRedirect


def redirect_to_api(request):
    return HttpResponseRedirect('/api/')
