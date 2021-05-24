from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import PatientListForm,CreateUserForm, EmpForm
from .filters import OrderFilter
from .decorators import unauthenticated_user,allowed_users, admin_only



def mainPage (request):
    return render(request, 'total/main.html')

def index (request):
    return render(request, 'total/index.html')

def privacy(request):
    return render(request, 'total/services.html')



#@unauthenticated_user
def registerPage(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

           
            messages.success(request, ' Account was created for ' + username )
            return redirect('login')

    context ={'form':form}
    return render(request,'total/registerpage.html', context)

@login_required(login_url='login')
@unauthenticated_user
def empLogin(request):
              
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password= password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')            

    context = {}
    return render(request, 'total/loginPage.html', context)


@login_required(login_url='login')
@admin_only
def home(request):
   orders = Order.objects.all()
   emps = Emp.objects.all()

   total_emp = emps.count()
   total_orders = orders.count()

   evals = orders.filter(status='Eval').count()
   schedule = orders.filter(status='Schedule').count()

   context = {'orders':orders,'emps':emps,'total_emp':total_emp,
   'total_orders':total_orders,'evals': evals,'schedule':schedule}

   return render(request, 'total/home.html',context )


def logoutUser(request):
    logout(request)
    return redirect ('login')




@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def userPage (request):
    orders = request.user.emp.order_set.all()

    total_orders = orders.count()
    evals = orders.filter(status='Eval').count()
    schedule = orders.filter(status='Schedule').count()
    print('ORDERS:', orders)

    context = {'orders':orders, 'total_orders':total_orders,'evals': evals,'schedule':schedule}
    return render(request, 'total/user.html'. context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def accountSettings(request):
    emp = request.user.emp
    form = EmpForm(instance=emp)

    if request.method == 'POST':
        form = EmpForm(request.POST, request.FILES,instance=emp)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'total/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def patient (request):
    patients = PatientList.objects.all()
    return render(request, 'total/patientlist.html',{'patients': patients})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def ptprofile(request, pk_test):
    emp = Emp.objects.get(id=pk_test)

    orders = emp.order_set.all()
    order_count = orders.count()

    myfilter = OrderFilter(request.GET,queryset=orders)
    orders = myfilter.qs

    context = {'emp':emp,'orders':orders,'order_count':order_count,'myfilter':myfilter}

    return render(request, 'total/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def schedule(request,pk):
    ScheduleFormSet = inlineformset_factory(Emp, Order, fields=('patient','status'), extra=10)
    emp = Emp.objects.get(id=pk)
    formset=ScheduleFormSet(queryset= Order.objects.none(), instance=emp)
    #form = PatientListForm(initial={'staff':staff})
    if request.method == 'POST':
        #form = PatientListForm(request.POST)
        formset=ScheduleFormSet(request.POST, instance=emp)
        if formset.is_valid():
            formset.save()
            return redirect('/home')


    context = {'formset':formset}
    return render(request, 'total/scheduleform.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateSchedule(request,pk):

    order = Order.objects.get(id=pk)
    form = PatientListForm(instance=order)

    if request.method == 'POST':
        form = PatientListForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/home')

    context ={'form':form}
    return render(request,'total/scheduleform.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/home')

    context = {'item':order}
    return render(request,'total/delete.html',context )



    class SignUpView(PassRequestMixin, SuccessMessageMixin, generic.CreateView):
        form_class = CustomUserCreationForm
        template_name = 'accounts/signup.html'
        success_message = 'Success: Sign up succeeded. You can now Log in.'
        success_url = reverse_lazy('index')