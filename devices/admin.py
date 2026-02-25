from django.contrib import admin
from .models import Device, DeviceStatusHistory

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'udid', 'model', 'os_version', 'battery_level', 'last_seen', 'enrolled')
    list_filter = ('enrolled', 'background_app_refresh_enabled', 'background_activity_restricted', 'low_power_mode')
    search_fields = ('name', 'udid', 'model')
    readonly_fields = ('last_seen', 'created_at', 'updated_at')
    fieldsets = (
        ('设备信息', {
            'fields': ('name', 'udid', 'model', 'os_version', 'owner')
        }),
        ('状态监控', {
            'fields': ('battery_level', 'battery_health', 'memory_usage',
                      'storage_used', 'storage_total', 'network_status', 'last_seen')
        }),
        ('后台控制', {
            'fields': ('background_app_refresh_enabled', 'background_activity_restricted', 'low_power_mode')
        }),
        ('MDM管理', {
            'fields': ('enrolled', 'enrollment_date')
        }),
        ('元数据', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(DeviceStatusHistory)
class DeviceStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('device', 'battery_level', 'memory_usage', 'network_status', 'timestamp')
    list_filter = ('timestamp', 'network_status')
    search_fields = ('device__name', 'device__udid')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
