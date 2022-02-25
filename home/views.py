from django.shortcuts import render, reverse, redirect
from products.models import Category
from .forms import ContactForm
# from videos.models import Video
# from news.models import News
# from pictures.models import Picture
# from django.core.mail import send_mail
#from django.template.loader import render_to_string
from datetime import datetime
from django.contrib import messages

def showHome(request):
    today = datetime.today()
    my_today = today.strftime('%d, %b %Y')
    categories = Category.objects.all().order_by('price')
    context = {'categories': categories, 'my_today': my_today}
    return render(request, 'home/home.html', context)

def showGallery(request):
    return render(request, 'home/gallery.html')
#
# def showOfficers(request):
#     return render(request, 'home/officers.html')

def showAbout(request):
    return render(request, 'home/about.html')

def showContact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            # send_mail(
            #     'Contact Qwikgas',
            #     'A message was sent by ' + name + '. Please log in to admin panel to read message',
            #     'yustaoab@gmail.com',
            #     [email],
            #     fail_silently=False,
            #     #html_message = render_to_string('home/home1.html')
            # )
            messages.success(request, str(name) + ", your message will receive attention shortly")
        else:
            return redirect('contact')
    return render(request, 'home/contact_form.html', {'form': form})
