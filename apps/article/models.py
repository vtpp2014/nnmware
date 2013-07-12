from django.conf import settings
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from nnmware.apps.address.models import Region
from nnmware.core.abstract import Tree, AbstractDate, AbstractName
from nnmware.core.managers import ArticleManager


class ArticleCategory(Tree):
    slug_detail = 'article_category'

    class Meta:
        ordering = ['parent__id', 'name']
        verbose_name = _('Article Category')
        verbose_name_plural = _('Articles Categories')

    @property
    def _active_set(self):
        return Article.objects.filter(category=self)


STATUS_DELETE = 0
STATUS_LOCKED = 1
STATUS_PUBLISHED = 2
STATUS_STICKY = 3
STATUS_MODERATION = 4
STATUS_DRAFT = 5

STATUS_CHOICES = (
    (STATUS_DELETE, _("Deleted")),
    (STATUS_LOCKED, _("Locked")),
    (STATUS_PUBLISHED, _("Published")),
    (STATUS_STICKY, _("Sticky")),
    (STATUS_MODERATION, _("Moderation")),
    (STATUS_DRAFT, _("Draft")),
)


class Article(AbstractDate, AbstractName):
    region = models.ForeignKey(Region, verbose_name=_('Region'), blank=True, null=True, related_name="%(class)s_reg",
                               on_delete=models.PROTECT)
    category = models.ForeignKey(ArticleCategory, verbose_name=_('Category'), null=True, blank=True,
                                 on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.PROTECT)
    status = models.IntegerField(_("Status"), choices=STATUS_CHOICES, default=STATUS_DRAFT)

    objects = ArticleManager()

    class Meta:
        ordering = ['-created_date', ]
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    @permalink
    def get_absolute_url(self):
        return "article_detail", (), {'pk': self.pk}

    @permalink
    def get_edit_url(self):
        return 'articles_edit', (), {'pk': self.pk}
