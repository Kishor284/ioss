from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import URL
from .serializers import URLSerializer
from .utils import generate_short_code
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

class URLCreateAPIView(generics.CreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def perform_create(self, serializer):
        short_code = generate_short_code()
        # Ensure uniqueness
        while URL.objects.filter(short_code=short_code).exists():
            short_code = generate_short_code()
        serializer.save(short_code=short_code)


class URLListAPIView(generics.ListAPIView):
    queryset = URL.objects.all().order_by('-created_at')
    serializer_class = URLSerializer


def redirect_view(request, code):
    try:
        url = URL.objects.get(short_code=code)
        return redirect(url.original_url)
    except URL.DoesNotExist:
        return render(request, '404.html', status=404)


def index(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        if original_url:
            short_code = generate_short_code()
            while URL.objects.filter(short_code=short_code).exists():
                short_code = generate_short_code()
            URL.objects.create(original_url=original_url, short_code=short_code)

    urls = URL.objects.all().order_by('-created_at')  # get all saved URLs
    context = {"urls": urls}
    return render(request, 'index.html', context)

@csrf_exempt
def delete_url(request, id):
    if request.method == "POST":
        try:
            url = URL.objects.get(id=id)
            url.delete()
            return HttpResponse(status=204)
        except URL.DoesNotExist:
            return HttpResponse(status=404)