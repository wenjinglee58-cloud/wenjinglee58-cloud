from django.db import models
from devices.models import Device

class Policy(models.Model):
    POLICY_TYPES = [
        ('background_refresh', '后台应用刷新'),
        ('background_activity', '后台活动限制'),
        ('power_saving', '省电模式'),
        ('network_restriction', '网络限制'),
        ('app_management', '应用管理'),
    ]

    name = models.CharField(max_length=200, verbose_name="策略名称")
    policy_type = models.CharField(max_length=50, choices=POLICY_TYPES, verbose_name="策略类型")
    description = models.TextField(blank=True, verbose_name="描述")

    # 策略配置 (JSON格式存储详细配置)
    configuration = models.JSONField(default=dict, verbose_name="配置参数")

    # 应用范围
    devices = models.ManyToManyField(Device, blank=True, related_name='policies', verbose_name="应用设备")
    apply_to_all = models.BooleanField(default=False, verbose_name="应用到所有设备")

    # 计划任务
    enabled = models.BooleanField(default=True, verbose_name="启用")
    schedule_start = models.DateTimeField(null=True, blank=True, verbose_name="开始时间")
    schedule_end = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")

    # 元数据
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "策略"
        verbose_name_plural = "策略"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class PolicyHistory(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='history')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='policy_history')
    applied_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    message = models.TextField(blank=True)

    class Meta:
        verbose_name = "策略应用历史"
        verbose_name_plural = "策略应用历史"
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.policy.name} -> {self.device.name}"
