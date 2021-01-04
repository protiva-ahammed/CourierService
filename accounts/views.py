from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import Group

"""#
from .models import Product#GeneralOrder
from xhtml2pdf import pisa
from django.views.generic import ListView
from django.template.loader import get_template
"""


from django.http import FileResponse



from .forms import OrderForm, CreateUserForm, CustomerForm,GeneralOrderForm

from .filters import OrderFilter

#from django.template import Context

#from cgi import escape

from django.contrib.auth.decorators import login_required
from .models import * 
from .decorators import unauthenticated_user,allowed_users,admin_only


@unauthenticated_user
def registerPage(request):

    form= CreateUserForm()
        
    if request.method=='POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')

            

            messages.success(request,'Account has been created for ' + username)
            return redirect('login')

    context={'form':form}
    return render (request,'accounts/register.html', context) 


@unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:


        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate( request, username=username, password = password)

            if user is not None:

                login(request, user)
                return redirect('home')
            else:
                messages.info(request,'Username or password is in correct!')
                return render (request,'accounts/login.html')


        context={}
        return render (request,'accounts/login.html',context)



def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()

    total_customers=customers.count()
    total_orders=orders.count()

    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={'orders':orders,'customers':customers,'total_customers':total_customers,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/dashboard.html',context)

def contract(request):
    return render(request,'accounts/about.html')




@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()

    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()
    print('orders:',orders)
    context={'orders':orders,'customers':customers,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/user.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)

    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context={'form':form}
    return render(request,'accounts/account_settings.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products=Product.objects.all()

    return render(request,'accounts/products.html',{'products':products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request,pk_test):
    customer=Customer.objects.get(id=pk_test)

    orders=customer.order_set.all()
    orders_count=orders.count()

    myFilter= OrderFilter(request.GET,queryset=orders)
    orders =myFilter.qs

    context = {'customer':customer ,'orders':orders,'orders_count':orders_count, 'myFilter': myFilter}
    return render(request,'accounts/customers.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form=OrderForm(initial={'customer':customer})
    if request.method=='POST':

        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'form':formset}
    return render(request,'accounts/order_form.html',context)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method == "POST":
        #print(request.post)
        form=OrderForm (request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render (request,'accounts/order_form.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'order':order}
	return render(request, 'accounts/delete.html', context)






@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def generalorder(request):
    form=GeneralOrderForm()

    if request.method=='POST':
        form=GeneralOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('generalorderlist')
    context={'form':form}
    return render(request,'accounts/generalorder.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def generalorderlist(request):
    generalorderlist=GeneralOrder.objects.all()
    total_orders=generalorderlist.count()

    delivered=generalorderlist.filter(status='Delivered').count()
    pending=generalorderlist.filter(status='Pending').count()
    context={'generalorderlist':generalorderlist,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/generalorderlist.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def filledUp(request,pk):
    order=GeneralOrder.objects.get(id=pk)

    return render(request,'accounts/filledup.html',{'order':order})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrderG(request, pk):
	order = GeneralOrder.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('generalorderlist')

	context = {'order':order}
	return render(request, 'accounts/deleteG.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrderG(request,pk):
    order=GeneralOrder.objects.get(id=pk)
    form=GeneralOrderForm(instance=order)
    if request.method == "POST":
        #print(request.post)
        form=GeneralOrderForm (request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('generalorderlist')
    context={'form':form}
    return render (request,'accounts/generalorder.html',context)




"""def pdf(request,pk):
    order=GeneralOrder.objects.get(id=pk)

    return render(request,'accounts/pdf1.html',{'order':order})



#



class ProductListView(ListView):
    model=Product
    template_name='accounts/pdf.html'

def product_render_pdf_view(request,*args,**kwargs):
    pk=kwargs.get('pk')
    order= Product.objects.get(pk=pk)
    template_path = 'accounts/pdf.html'
    context = {'order': order}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download only
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if to show only
    response['Content-Disposition'] = 'filename="bill_memo.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    

#
def render_pdf_view(request):
    template_path = 'accounts/pdf.html'
    context = {'order': order}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download only
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if to show only
    response['Content-Disposition'] = 'filename="bill_memo.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

"""