from django.shortcuts import render
from katalog.models import CatalogItem


# TODO: Create your views here.
def show_katalog(request):
    daftar_item_katalog = CatalogItem.objects.all()
    context = {
        'list_item': daftar_item_katalog,
        'nama': 'Muhammad Nabiel Andityo Purnomo',
        'npm': '2106750465',
    }
    return render(request, 'katalog.html', context)