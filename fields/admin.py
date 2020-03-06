import datetime
import icu
import nested_admin

from admin_auto_filters.filters import AutocompleteFilter
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.admin.filters import SimpleListFilter
from django.http import Http404
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from gsuite.views import gauth


class ImprovAdminSite(AdminSite):
    site_header = "Poločas nápadu"
    name = 'admin'
    site_url = settings.APP_WEBSITE_URL

    def __init__(self):
        super(ImprovAdminSite, self).__init__(self.name)
        if settings.DJANGO_ADMIN_SSO:
            self.login = gauth

    def get_model_sort_helper(self, request):
        collator = icu.Collator.createInstance(icu.Locale(request.LANGUAGE_CODE))
        return lambda x: collator.getSortKey(x['name'][0])

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        sort_helper = self.get_model_sort_helper(request)
        for app in app_list:
            app['models'].sort(key=sort_helper)
        app_list.sort(key=sort_helper)
        return app_list

    def app_index(self, request, app_label, extra_context=None):
        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            raise Http404('The requested admin page does not exist.')
        app_dict['models'].sort(key=self.get_model_sort_helper(request))
        app_list = [app_dict]
        return super().app_index(request, app_label, {
            **(extra_context or {}),
            'app_list': app_list
        })

    def hookup(self, admin_model):
        return self.register(admin_model.model, admin_model)


class BaseAdminModel(nested_admin.NestedModelAdmin):
    pass


class BaseInlineAdminModel(nested_admin.NestedTabularInline):
    """Base admin for Inline models."""

    extra = 1


class BaseStackedAdminModel(nested_admin.NestedStackedInline):
    """Base admin for Inline models."""

    extra = 1


class LocationFilter(AutocompleteFilter):
    title = _("Location")
    field_name = "location"


class ShowFilter(AutocompleteFilter):
    title = _("Show")
    field_name = "show"


class ShowTypeFilter(AutocompleteFilter):
    title = _("Show type")
    field_name = "show_type"


class SeasonFilter(SimpleListFilter):
    field = None
    season_end = 8
    season_start = 9
    start = 2014
    title = _("Season")
    parameter_name = "season"

    def lookups(self, request, model_admin):
        seasons = []
        for season in range(self.start, datetime.date.today().year):
            season_name = "%s/%s" % (
                self.get_season_start(season).year,
                self.get_season_end(season).year,
            )
            seasons.append((season, season_name))

        return seasons

    def get_season_end(self, season):
        return self.get_season_start(season) + relativedelta(months=12)

    def get_season_start(self, season):
        return datetime.date(year=season, month=self.season_start, day=1)

    def queryset(self, request, queryset):
        try:
            filter_value = int(self.value())
        except TypeError:
            return queryset

        kwargs = {
            "%s__gte" % self.field: self.get_season_start(filter_value),
            "%s__lt" % self.field: self.get_season_end(filter_value),
        }
        return queryset.filter(**kwargs)


def empty_value(value):
    return mark_safe('<span class="empty-value">%s</span>' % value)
