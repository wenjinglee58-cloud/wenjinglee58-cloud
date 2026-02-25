from django.contrib import admin
from .models import Policy, PolicyHistory

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'policy_type', 'enabled', 'apply_to_all', 'created_at')
    list_filter = ('policy_type', 'enabled', 'apply_to_all')
    search_fields = ('name', 'description')
    filter_horizontal = ('devices',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'policy_type', 'description')
        }),
        ('策略配置', {
            'fields': ('configuration',)
        }),
        ('应用范围', {
            'fields': ('apply_to_all', 'devices')
        }),
        ('计划任务', {
            'fields': ('enabled', 'schedule_start', 'schedule_end')
        }),
        ('元数据', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(PolicyHistory)
class PolicyHistoryAdmin(admin.ModelAdmin):
    list_display = ('policy', 'device', 'applied_at', 'success')
    list_filter = ('success', 'applied_at')
    search_fields = ('policy__name', 'device__name')
    readonly_fields = ('applied_at',)
    date_hierarchy = 'applied_at'
