from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Question

class Command(BaseCommand):
    help = '将发布超过3天且未被解决的问题悬赏金币退还给作者，并清零悬赏。'

    def handle(self, *args, **kwargs):
        # 计算出3天前的时间点
        three_days_ago = timezone.now() - timedelta(days=3)

        # 筛选出符合条件的问题：
        # 1. 创建时间早于等于3天前
        # 2. 尚未被解决 (is_resolved=False)
        # 3. 悬赏金币大于0
        expired_questions = Question.objects.filter(
            created_at__lte=three_days_ago,
            is_resolved=False,
            bounty__gt=0
        )

        # 获取符合条件的数量
        count = expired_questions.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('没有找到需要处理的过期悬赏。'))
            return

        self.stdout.write(f'找到了 {count} 个需要处理的过期悬赏...')

        for question in expired_questions:
            author_profile = question.author.profile
            bounty_amount = question.bounty

            # 1. 将金币退还给提问者
            author_profile.coins += bounty_amount
            author_profile.save()

            # 2. 将问题的悬赏清零
            question.bounty = 0
            question.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'成功将问题 "{question.title}" 的 {bounty_amount} 金币退还给用户 "{question.author.username}"。'
                )
            )
        
        self.stdout.write(self.style.SUCCESS(f'任务完成！共处理了 {count} 个过期悬赏。'))