from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    # 设备标识
    name = models.CharField(max_length=200, verbose_name="设备名称")
    udid = models.CharField(max_length=100, unique=True, verbose_name="设备唯一标识")
    model = models.CharField(max_length=100, blank=True, verbose_name="设备型号")
    os_version = models.CharField(max_length=50, blank=True, verbose_name="操作系统版本")

    # 状态信息
    battery_level = models.IntegerField(default=0, verbose_name="电池电量 (%)")
    battery_health = models.CharField(max_length=50, blank=True, verbose_name="电池健康状态")
    memory_usage = models.IntegerField(default=0, verbose_name="内存使用率 (%)")
    storage_used = models.FloatField(default=0, verbose_name="已用存储 (GB)")
    storage_total = models.FloatField(default=0, verbose_name="总存储 (GB)")
    network_status = models.CharField(max_length=50, blank=True, verbose_name="网络状态")
    last_seen = models.DateTimeField(auto_now=True, verbose_name="最后在线时间")

    # 后台控制设置
    background_app_refresh_enabled = models.BooleanField(default=True, verbose_name="启用后台应用刷新")
    background_activity_restricted = models.BooleanField(default=False, verbose_name="限制后台活动")
    low_power_mode = models.BooleanField(default=False, verbose_name="低电量模式")

    # 设备管理
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="所有者")
    enrolled = models.BooleanField(default=False, verbose_name="已注册MDM")
    enrollment_date = models.DateTimeField(null=True, blank=True, verbose_name="注册日期")

    # 元数据
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = "设备"
        ordering = ['-last_seen']

    def __str__(self):
        return f"{self.name} ({self.model})"

class DeviceStatusHistory(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='status_history')
    battery_level = models.IntegerField()
    memory_usage = models.IntegerField()
    storage_used = models.FloatField()
    network_status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "设备状态历史"
        verbose_name_plural = "设备状态历史"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.device.name} at {self.timestamp}"
