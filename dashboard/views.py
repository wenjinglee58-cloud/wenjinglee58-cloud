from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from datetime import timedelta
from devices.models import Device
from policies.models import Policy

def home(request):
    """首页，如果已登录则重定向到仪表板"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def register_view(request):
    """用户注册视图"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    """用户登录视图"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def dashboard_view(request):
    """主仪表板视图"""
    # 获取用户相关的设备
    devices = Device.objects.filter(owner=request.user).order_by('-last_seen')
    total_devices = devices.count()

    # 计算30分钟前的时间点
    timezone_now_minus_30min = timezone.now() - timedelta(minutes=30)

    # 设备状态统计
    devices_low_battery = devices.filter(battery_level__lt=20).count()
    devices_offline = devices.filter(last_seen__lt=timezone_now_minus_30min).count()

    # 获取策略
    policies = Policy.objects.filter(enabled=True)

    context = {
        'total_devices': total_devices,
        'devices_low_battery': devices_low_battery,
        'devices_offline': devices_offline,
        'devices': devices[:10],  # 最近10台设备
        'policies': policies[:5],  # 最近5个策略
        'timezone_now_minus_30min': timezone_now_minus_30min,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def devices_view(request):
    """设备列表视图"""
    devices = Device.objects.filter(owner=request.user).order_by('-last_seen')
    return render(request, 'dashboard/devices.html', {'devices': devices})

@login_required
def policies_view(request):
    """策略列表视图"""
    policies = Policy.objects.all()
    return render(request, 'dashboard/policies.html', {'policies': policies})
