from django.shortcuts import render

# Create your views here.
@login_required
def my_logout(request):
    logout(request)
    return redirect('my_login')

def my_login(request):
    context={}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            #create session
            login(request, user)
            
            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('homepage')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Missing Username OR Password'

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url
            
     
    return render(request, 'login/login.html',context = context)

def createAccount(request):
    context={}
    if request.method == 'POST':
        completed = request.POST.get('agree-term')
        username = request.POST.get('username')
        password = request.POST.get('password')
        re_password = request.POST.get('password_again')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')

        if completed:
            if re_password != password:
                context['error'] = 'Password do not match'
            else:
                try:
                    user = User.objects.create_user(username, email, password)
                    print('reach')
                    Groups = Group.objects.get(name='register_user')
                    user.first_name = fname
                    user.last_name = lname
                    user.groups.add(Groups)
                    user.save()
                    success = 'Your Account '+username+' : Success Sign up' 
                    request.session['success'] = success
                    return redirect('my_login')
                except Exception as e:
                    context['error'] = '%s' % (e.args)
                
        else:
            context['error'] = 'Please agree Terms of service'

        context['username'] = username
        context['fname']= fname
        context['lname'] = lname
        context['email'] = email
        context['signup'] = 'True'
 
    return render(request,'login/create_account.html',context=context)
    
@login_required
def ChangePassword(request):
    context={}
    if request.method == 'POST':
        user = request.user.username
        password = request.POST.get('password')
        re_password = request.POST.get('password_again')

        if password != re_password:
            context['error'] = 'Password do not match'
        else:
            u = User.objects.get(username=user)
            u.set_password(password)
            u.save()
            context['success'] = 'Change Password Successfully'
            return redirect('my_logout')

    return render(request, 'login/changepassword.html', context=context)