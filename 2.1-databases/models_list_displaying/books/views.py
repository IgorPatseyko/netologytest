from django.shortcuts import render
from books.models import Book


def books_list_view(request):
    template = 'books/books_list.html'
    context = {
        'books': Book.objects.all()
    }
    return render(request, template, context)


def books_view(request, pub_date):
    template = 'books/books_list.html'
    dates_list = [book.pub_date for book in Book.objects.all().order_by('pub_date').distinct('pub_date')]
    print(dates_list)
    page_num = dates_list.index(pub_date)

    context = {
        'books': Book.objects.filter(pub_date=pub_date),
    }
    if page_num > 0:
        context['prev_page'] = dates_list[page_num-1]
    if page_num < len(dates_list)-1:
        context['next_page'] = dates_list[page_num+1]

    return render(request, template, context)
