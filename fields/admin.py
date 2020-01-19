import datetime

from dateutil.relativedelta import relativedelta
from admin_auto_filters.filters import AutocompleteFilter
from django.contrib.admin.filters import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
import nested_admin


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
