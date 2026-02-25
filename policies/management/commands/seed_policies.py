from django.core.management.base import BaseCommand
from policies.models import Policy, Device
import random

class Command(BaseCommand):
    help = '创建模拟策略数据'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=5, help='要创建的策略数量')

    def handle(self, *args, **options):
        count = options['count']

        # 策略类型和配置模板
        policy_templates = [
            {
                'name': '限制后台应用刷新',
                'type': 'background_refresh',
                'config': {'allowed_apps': ['邮件', '日历', '天气'], 'refresh_interval': 30}
            },
            {
                'name': '省电模式策略',
                'type': 'power_saving',
                'config': {'enable_below': 30, 'disable_charging': True}
            },
            {
                'name': '后台活动限制',
                'type': 'background_activity',
                'config': {'restrict_network': True, 'restrict_location': False}
            },
            {
                'name': '工作时间网络限制',
                'type': 'network_restriction',
                'config': {'time_range': '9:00-18:00', 'block_social_media': True}
            },
            {
                'name': '禁止非企业应用',
                'type': 'app_management',
                'config': {'allowed_bundle_ids': ['com.apple.mail', 'com.apple.calendar']}
            }
        ]

        devices = list(Device.objects.all())
        if not devices:
            self.stdout.write(self.style.WARNING('没有设备可用，请先创建设备'))
            return

        policies_created = 0
        for i in range(count):
            template = random.choice(policy_templates)

            policy = Policy.objects.create(
                name=f'{template["name"]} #{i+1}',
                policy_type=template['type'],
                description=f'这是{template["name"]}的示例策略，用于演示目的。',
                configuration=template['config'],
                apply_to_all=random.choice([True, False]),
                enabled=random.choice([True, False])
            )

            # 如果不是应用到所有设备，则随机分配一些设备
            if not policy.apply_to_all and devices:
                assigned_devices = random.sample(devices, min(len(devices), random.randint(1, 3)))
                policy.devices.set(assigned_devices)

            policies_created += 1

        self.stdout.write(self.style.SUCCESS(f'成功创建 {policies_created} 个模拟策略'))