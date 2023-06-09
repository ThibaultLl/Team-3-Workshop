from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import logging
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control


from django.shortcuts import redirect

from .models.customer import Customer
from .models.action import Action

def parse_file_from_csv(uploaded_file):
        file_data = uploaded_file.read().decode("utf-8")
        lines = file_data.split("\n")
        #loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict["first_name"] = fields[0]
            data_dict["name"] = fields[1]
            data_dict["email"] = fields[2]
            data_dict["mobile"] = fields[3]
            data_dict["address"] = fields[4]
            try:
                Customer.objects.create(**data_dict)
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
            pass


@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        if not uploaded_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("import_contact"))
        
        if uploaded_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (uploaded_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("import_contact"))
        parse_file_from_csv(uploaded_file)
    return render(request, 'import_contact.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def download(request):
    # export all Customer to csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'
    customers = Customer.objects.all()
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['first_name', 'name', 'email', 'mobile', 'address', 'status', 'action_type', 'description'])
    for customer in customers:
        action = Action.objects.filter(id=customer.pk)
        action = action[0] if action else None
        if action:
            writer.writerow([customer.first_name, customer.name, customer.email, customer.mobile, customer.address, customer.status, action.action_type, action.description])
        else:
            writer.writerow([customer.first_name, customer.name, customer.email, customer.mobile, customer.address, customer.status, 'aucune action', 'aucune description'])
    return response


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def logincrm(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def logoutcrm(request):
    logout(request)
    return redirect('/')
