from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from devices.models import Device, DeviceStatusHistory
from datetime import timedelta
from django.utils import timezone
import random

class Command(BaseCommand):
    help = '创建模拟设备数据'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='要创建的设备数量')
        parser.add_argument('--user', type=str, default='admin', help='设备所属用户的用户名')

    def handle(self, *args, **options):
        count = options['count']
        username = options['user']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'用户 "{username}" 不存在'))
            return

        # 设备型号列表
        models = ['iPhone 15 Pro', 'iPhone 14', 'iPhone 13 Pro Max', 'iPhone 12', 'iPhone SE']
        os_versions = ['iOS 17.2', 'iOS 17.1', 'iOS 16.7', 'iOS 15.8']
        battery_health_options = ['Good', 'Fair', 'Poor', 'Replace Soon']
        network_statuses = ['WiFi', '5G', '4G', '3G', 'No Connection']

        devices_created = 0
        for i in range(count):
            udid = f'DEVICE-{random.randint(100000, 999999)}-{random.randint(1000, 9999)}'
            model = random.choice(models)
            os_version = random.choice(os_versions)
            battery_level = random.randint(10, 100)
            memory_usage = random.randint(20, 90)
            storage_total = random.choice([64, 128, 256, 512])
            storage_used = random.randint(10, storage_total - 10)
            last_seen = timezone.now() - timedelta(minutes=random.randint(0, 1440))  # 最多24小时前

            device = Device.objects.create(
                name=f'设备 {i+1}',
                udid=udid,
                model=model,
                os_version=os_version,
                battery_level=battery_level,
                battery_health=random.choice(battery_health_options),
                memory_usage=memory_usage,
                storage_used=storage_used,
                storage_total=storage_total,
                network_status=random.choice(network_statuses),
                last_seen=last_seen,
                background_app_refresh_enabled=random.choice([True, False]),
                background_activity_restricted=random.choice([True, False]),
                low_power_mode=random.choice([True, False]),
                owner=user,
                enrolled=random.choice([True, False]),
                enrollment_date=timezone.now() - timedelta(days=random.randint(1, 365)) if random.choice([True, False]) else None
            )

            # 创建一些状态历史记录
            for j in range(random.randint(1, 5)):
                DeviceStatusHistory.objects.create(
                    device=device,
                    battery_level=random.randint(10, 100),
                    memory_usage=random.randint(20, 90),
                    storage_used=random.randint(10, storage_total - 10),
                    network_status=random.choice(network_statuses),
                    timestamp=last_seen - timedelta(hours=j*2)
                )

            devices_created += 1

        self.stdout.write(self.style.SUCCESS(f'成功创建 {devices_created} 台模拟设备'))