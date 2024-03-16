from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Prefetch
from .models import Post, Review, ReportPost,Image,UserProfile
from .forms import SignupForm,LoginForm,PassChangeForm,PassSetForm,EditUserProfileForm,EditAdminProfileForm,ReportForm,ReviewForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import get_user_model
from .utils import calculate_cosine_similarity,find_nearest_dest
from .forms import PostForm
from django.views.generic import UpdateView,DetailView
from django.urls import reverse_lazy
import json


User = get_user_model()


def Sign_up(request):
    if request.method=='POST':
        f=SignupForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request,'Account created successfully!!!')
            return HttpResponseRedirect('/')
    else:
        f=SignupForm()
    return render(request,'signup.html',{'form':f})

def Log_in(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                email=form.cleaned_data['username']
                passwprd=form.cleaned_data['password']
                user=authenticate(email=email,password=passwprd)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully!!!')
                    return HttpResponseRedirect('/')
        else:
            form=LoginForm()
        return render(request,'login.html',{'form':form})
    else:
        return HttpResponseRedirect('/')
    
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    
    def get(self,request,pk,*args, **kwargs):

        user = UserProfile.objects.prefetch_related(
        Prefetch('user_posts', queryset=Post.objects.order_by('-created_on'))
        ).get(pk=pk)

        return render(request,'profile.html',{'user':user})
        
    
def log_out(request):
    logout(request)
    messages.success(request,'Logged out successfully!!!')
    return HttpResponseRedirect('/login/')

def Password_chage(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=PassChangeForm(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Password changed successfully!!')
                return redirect('login')
        
        else:
            form=PassChangeForm(user=request.user)
        return render(request,'passwordchange.html',{'form':form})
    else:
        return redirect('login')
    

def Password_set(request):
    
    if request.user.is_authenticated:
        if request.method=='POST':
            form=PassSetForm(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                #after changing password django automatically redirects into login page but to keep logged in we need to update sesstion 
                update_session_auth_hash(request,form.user)
                messages.success(request,'Password set sucessfully!!!')
                return HttpResponseRedirect('/')
        else:
            form= PassSetForm(user=request.user)
        return render(request,'passwordreset.html',{'form':form})
    else:
        return redirect('login')
    
def user_detail(request,id):
    if request.user.is_authenticated:
        if request.user.is_superuser==True:
            pi=User.objects.get(pk=id)
            if request.method=='POST':
             form=EditAdminProfileForm(request.POST,instance=pi)
             if form.is_valid():
                form.save()
            else:
                form=EditAdminProfileForm(instance=pi)
            return render(request,'userdetail.html',{'form':form})
        else:
            return HttpResponseRedirect('/')
    else:
        return redirect('/login/')
        
class HomeView(View):
    def get(self,request,*args, **kwargs):
        query = request.GET.get('q')
        if query:
            user_preference = f"{query}"
            print(user_preference)

            posts = Post.objects.filter(availability=True)
            post_info_list = []
            for post in posts:
                post_info = {"id":post.id,"information":f"{post.title},{post.province},{post.district},{post.city},{post.latitude},{post.longitude},{post.fare},{post.description}"}
                post_info_list.append(post_info)
            
            post_infos =[post["information"] for post in post_info_list]

            formatted_data = [' '.join(item.split(',')) for item in post_infos]
            #print(formatted_data)
            
            post_primary_keys = [post['id'] for post in post_info_list]
            
            recommend = calculate_cosine_similarity(user_preference,formatted_data,post_primary_keys)
        
            recommended_posts = [Post.objects.get(pk=pk) for pk in recommend]

            return render(request,'homepage.html',{'posts':recommended_posts})
        else:

            nearby_posts = Post.objects.filter(availability=True).order_by('?')[:5] 
            return render(request, 'homepage.html', {'posts': nearby_posts})
        
@method_decorator(login_required, name='dispatch')
class PostCreateView(View):
    def get(self,request,*args, **kwargs):
        form = PostForm()
        return render(request,'post_create.html',{'form':form})
    
    def post(self,request,*args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user.profile
            new_post.save()
            for f in request.FILES.getlist('images'):
                img = Image.objects.create(image=f)
                new_post.images.add(img)
            messages.success(request,'Your room/flat has been listed for rent')
            return HttpResponseRedirect('/')





class PostDetailView(View):
    def get(self,request,pk,*args, **kwargs):
        post = Post.objects.get(pk=pk)
        reviews = Review.objects.filter(post=post)
        review_form = ReviewForm()
        return render(request,'post_detail.html',{'post':post,'reviews':reviews,'review_form':review_form})
    
    def post(self,request,pk,*args, **kwargs):
        form = ReviewForm(request.POST)
        p = Post.objects.get(pk=pk)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.post = p
            new_form.author = request.user.profile
            new_form.save()
            messages.success(request,'Review has been submitted!!')
            return redirect('post_detail',p.id)
        
        return HttpResponseRedirect('/')
    

@method_decorator(login_required, name='dispatch')
class PostUpdateView(View):
    def get(self,request,pk,*args, **kwargs):
        p = Post.objects.get(pk=pk)
        form = PostForm(instance=p)
        return render(request,'update_post.html',{'form':form,'post':p})
    
    def post(self,request,pk,*args, **kwargs):
        p = Post.objects.get(pk=pk)
        current_images = p.images.all()

        form = PostForm(request.POST, request.FILES, instance=p)
        if form.is_valid():
            # Save the updated post instance (excluding images for now)
            updated_post = form.save(commit=False)
            updated_post.save()

            if request.FILES.getlist('images'):
                # Clear existing images associated with the post
                p.images.clear()

                # Save new images and associate them with the post
                for image_file in request.FILES.getlist('images'):
                    new_image = Image(image=image_file)
                    new_image.save()
                    updated_post.images.add(new_image)


            updated_post.save()  # Save the post instance with updated images


            return redirect('post_detail', p.id)
        
@method_decorator(login_required, name='dispatch') 
class ReportView(View):
    def get(self,request,*args, **kwargs):
        form = ReportForm()
        return render(request,'report.html',{'form':form})
    
    def post(self,request,pk,*args, **kwargs):
        p = Post.objects.get(pk=pk)
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.post = p
            report.user = request.user.profile  # Assuming UserProfile model linked to user
            report.save()
            messages.success(request,'Report has been submitted!!')
            return redirect('post_detail',pk=pk)



class FindNearByView(View):
    def post(self,request,*args, **kwargs):
        data = json.loads(request.body)
        lat = data.get('latitude')
        lng = data.get('longitude')
        print('request.comes')

        result = find_nearest_dest(lat,lng)
        
        if result:
            near_posts = [{'post':item['post'],'distance':item['distance']} for item in result]

            return render(request,'findnearby.html',{'post':near_posts})
        return HttpResponseRedirect('/')