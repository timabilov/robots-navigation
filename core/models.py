from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.notifications import AWAITING_BOTS


class Landmark(models.Model):

    name = models.CharField(max_length=400)

    # normalize to query after
    x = models.PositiveIntegerField(verbose_name='X')
    y = models.PositiveIntegerField(verbose_name='Y')

    def __str__(self):
        return self.name


class Route(models.Model):
    """
    Defines set of instructions to accomplish some route.
    """
    name = models.CharField(default='Route', max_length=255)
    target = models.CharField(verbose_name='Target group name', max_length=400, null=True, blank=True)

    start = ArrayField(models.PositiveIntegerField(), default=[0, 0], null=True)

    # We can store this information completely in binary way for huge optimizations
    # this is middle ground though (between indexing and full de-normalization)
    # { 'north:5', 'left:', 'reach:Saint Valley' }
    instructions = ArrayField(models.CharField(max_length=40), null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

    def notify(self, target=None):
        group = target or self.target
        target_bots = AWAITING_BOTS
        if group:
            target_bots = filter(lambda bot: bot.group == group, AWAITING_BOTS)

        for bot in target_bots:
            bot.load(self)

    def __iter__(self):
        yield from self.instructions

    def __str__(self):
        return self.name
