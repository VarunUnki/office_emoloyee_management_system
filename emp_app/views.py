from django.shortcuts import render,redirect,HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Hardcoded username and password for testing purposes
        predefined_username = 'sampan'
        predefined_password = 'shetty777'
        
        if username == predefined_username and password == predefined_password:
            try:
                # Check if the user already exists
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # If the user doesn't exist, create a new user
                user = User.objects.create_user(username=username, password=password)
            
            # Log the user in
            login(request, user)
            return redirect('index')  # Redirect to home page after successful login
        else:
            # error_message = "Invalid username or password. Please try again."
            # messages.error(request, error_message)
            return redirect('login')
    else:
        error_message = "Invalid username or password. Please try again."
        return render(request, 'login.html')



def index(request):
    return render(request,'index.html')

def all_emp(request):
    emps = Employee.objects.all()#django command to view all items in a module i.e.., Users.objects.all()
    context={
        'emps': emps
    }
    print(context)
    return render(request,'view_all_emp.html',context)
    

def add_emp(request):
    if request.method == 'POST':
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept_id = int(request.POST['dept'])
        role_id = int(request.POST['role'])
        
        # Create new employee object
        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept_id=dept_id, role_id=role_id, hire_date=datetime.now())
        # Save new employee to the database
        new_emp.save()
        
        return HttpResponse('Employee Added Successfully, you can see it in view all Employee Details')
    elif request.method == 'GET':
        
        departments = Department.objects.all()
        roles = Role.objects.all()
        
        # Pass departments and roles data to the template
        return render(request, 'add_emp.html', {'departments': departments, 'roles': roles})
    else:
        return HttpResponse("An Exception Occurred! Employee Has Not Been Added")

def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse('Employee Removed Successfully, you can now see updated Employee details in View All Employee')
        except:
            return HttpResponse("Please Enter A Valid Employee ID")
    emps = Employee.objects.all()
    context= {
        'emps':emps
    }
    return render(request,'remove_emp.html',context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps= emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name)) #icontains is used to avoid case sensitive 
        if dept:    
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context={
            'emps' : emps
        }
        return render(request,'view_all_emp.html',context)
    
    elif request.method == 'GET':
        return render(request,'filter_emp.html')
    
    else:
        return HttpResponse('An Exception Occured')


