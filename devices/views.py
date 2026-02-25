from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Device

@login_required
def toggle_background_refresh(request, device_id):
    """切换设备的后台应用刷新状态"""
    device = get_object_or_404(Device, id=device_id, owner=request.user)

    if request.method == 'POST':
        device.background_app_refresh_enabled = not device.background_app_refresh_enabled
        device.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'enabled': device.background_app_refresh_enabled,
                'message': f'后台应用刷新已{"启用" if device.background_app_refresh_enabled else "禁用"}'
            })
        else:
            # 非AJAX请求，重定向回设备列表
            return redirect('devices')

    # GET请求返回设备详情页
    return redirect('devices')

@login_required
def bulk_toggle_background_refresh(request):
    """批量切换后台应用刷新状态"""
    if request.method == 'POST':
        device_ids = request.POST.getlist('device_ids')
        action = request.POST.get('action', 'toggle')

        devices = Device.objects.filter(id__in=device_ids, owner=request.user)

        updated_count = 0
        for device in devices:
            if action == 'enable':
                device.background_app_refresh_enabled = True
            elif action == 'disable':
                device.background_app_refresh_enabled = False
            else:  # toggle
                device.background_app_refresh_enabled = not device.background_app_refresh_enabled

            device.save()
            updated_count += 1

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'updated_count': updated_count,
                'message': f'成功更新 {updated_count} 台设备的后台应用刷新设置'
            })
        else:
            return redirect('devices')

    return redirect('devices')

@login_required
def background_refresh_management(request):
    """后台应用刷新管理页面"""
    devices = Device.objects.filter(owner=request.user).order_by('-last_seen')

    # 统计
    enabled_count = devices.filter(background_app_refresh_enabled=True).count()
    disabled_count = devices.filter(background_app_refresh_enabled=False).count()

    context = {
        'devices': devices,
        'enabled_count': enabled_count,
        'disabled_count': disabled_count,
        'total_devices': devices.count(),
    }
    return render(request, 'devices/background_refresh.html', context)

@login_required
def toggle_background_activity(request, device_id):
    """切换设备的后台活动限制状态"""
    device = get_object_or_404(Device, id=device_id, owner=request.user)

    if request.method == 'POST':
        device.background_activity_restricted = not device.background_activity_restricted
        device.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'restricted': device.background_activity_restricted,
                'message': f'后台活动限制已{"启用" if device.background_activity_restricted else "禁用"}'
            })
        else:
            return redirect('devices')

    return redirect('devices')

@login_required
def background_activity_management(request):
    """后台活动限制管理页面"""
    devices = Device.objects.filter(owner=request.user).order_by('-last_seen')

    # 统计
    restricted_count = devices.filter(background_activity_restricted=True).count()
    unrestricted_count = devices.filter(background_activity_restricted=False).count()

    context = {
        'devices': devices,
        'restricted_count': restricted_count,
        'unrestricted_count': unrestricted_count,
        'total_devices': devices.count(),
    }
    return render(request, 'devices/background_activity.html', context)

@login_required
def generate_mdm_profile(request):
    """生成MDM配置文件"""
    from django.http import HttpResponse
    import uuid
    import plistlib
    import datetime

    # 创建配置字典
    profile_uuid = str(uuid.uuid4()).upper()
    now = datetime.datetime.utcnow()

    payload_content = {
        'PayloadUUID': profile_uuid,
        'PayloadType': 'Configuration',
        'PayloadVersion': 1,
        'PayloadIdentifier': f'com.ioscontrol.mdm.{profile_uuid}',
        'PayloadDisplayName': 'iOS设备管理配置文件',
        'PayloadDescription': '用于管理iOS设备的配置描述文件',
        'PayloadOrganization': 'iOS设备后台管理系统',
        'PayloadRemovalDisallowed': False,
        'PayloadContent': [
            {
                'PayloadUUID': str(uuid.uuid4()).upper(),
                'PayloadType': 'com.apple.mdm',
                'PayloadVersion': 1,
                'PayloadIdentifier': f'com.ioscontrol.mdm.{profile_uuid}.mdm',
                'PayloadDisplayName': 'MDM配置',
                'PayloadDescription': '移动设备管理配置',
                'PayloadOrganization': 'iOS设备后台管理系统',
                'PayloadContent': {
                    'AccessRights': 8191,
                    'CheckInURL': f'{request.build_absolute_uri("/")}mdm/checkin',
                    'CheckOutWhenRemoved': True,
                    'ServerURL': f'{request.build_absolute_uri("/")}mdm/server',
                    'Topic': 'com.apple.mgmt.External.' + profile_uuid,
                    'SignMessage': False,
                    'ServerCapabilities': ['com.apple.mdm.per-user-connections'],
                }
            }
        ]
    }

    # 转换为plist格式
    plist_data = plistlib.dumps(payload_content)

    # 创建HTTP响应
    response = HttpResponse(plist_data, content_type='application/x-apple-aspen-config')
    response['Content-Disposition'] = f'attachment; filename="mdm_profile_{profile_uuid[:8]}.mobileconfig"'
    return response
