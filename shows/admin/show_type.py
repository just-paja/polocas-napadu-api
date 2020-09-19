from fields.admin import BaseAdminModel, BaseInlineAdminModel

from ..models import ShowType, ShowTypePhoto


class ShowTypePhotoAdmin(BaseInlineAdminModel):
    model = ShowTypePhoto


class ShowTypeAdmin(BaseAdminModel):
    model = ShowType
    inlines = [
        ShowTypePhotoAdmin,
    ]
    fields = (
        "name",
        "slug",
        "visibility",
        "short_description",
        "description",
        "use_games",
        "use_fouls",
    )
    readonly_fields = ("slug",)
    list_display = ("name", "use_games", "use_fouls", "visibility")
    list_filter = ("use_games", "use_fouls", "visibility")
    search_fields = ("name",)
