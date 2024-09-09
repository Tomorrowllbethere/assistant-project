from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
# Create your views here.
import features.rate.rate.spiders.rate_usd_eur as rate
import scrapydo
import datetime as dt
from addressbook.models import AllContact
import requests
from django.http import JsonResponse
# Ініціалізуємо scrapydo
scrapydo.setup()

def rate_view(request):
    # Отримуємо дані з кешу, якщо вони є
    rates = cache.get('rates_data')
    
    # Якщо даних немає в кеші, запускаємо павука
    if rates is None:
        results = scrapydo.run_spider(rate.RateUsdEurSpider)
        rates = results[0] if results else {}
        
        # Зберігаємо результати в кеші на 10 хвилин
        cache.set('rates_data', rates, timeout=600)

    return rates

def week_upcomming_birthday(request):
    contacts_delta=[]
    day_now = dt.date.today()
    for i in range(7):
            target_date = day_now + dt.timedelta(days=i)
            contacts = AllContact.objects.filter(birthday__day=target_date.day, birthday__month=target_date.month).all()
            if contacts:
                for contact in contacts:
                    current_year = day_now.year
                    current_date = dt.date(current_year, contact.birthday.month, contact.birthday.day)
                    delta = (current_date - day_now).total_seconds()
                    age = (current_date.year-contact.birthday.year)
                    contacts_delta.append({
                        'contact': contact,
                        'age': age,
                        'delta': delta,
                    })    
    return contacts_delta




def welcome(request):
    return render(request, 'custom_auth/welcome.html')

@login_required
def main(request):
    # Отримання інформації про тарифи (залежно від реалізації)
    rates = rate_view(request)
    upcoming_birthday= week_upcomming_birthday(request)

    # Відображення даних на сторінці
    return render(request, 'custom_auth/index.html', context={
        "rates": rates,
        "upcoming": upcoming_birthday
    })

