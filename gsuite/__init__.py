from django.conf import settings
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from .groups import (
    GROUPS,
    MODELS_ALL,
    MODEL_ACCESS_RO,
    MODEL_ACCESS_RW,
    MODEL_ACTION_VIEW,
    MODEL_ACTIONS,
)

PERM_ENSURE = "ensure"
PERM_DELETE = "delete"


def get_perm_method(action, access):
    if action == MODEL_ACTION_VIEW:
        return (
            PERM_ENSURE if access in [MODEL_ACCESS_RO, MODEL_ACCESS_RW] else PERM_DELETE
        )
    return PERM_ENSURE if access == MODEL_ACCESS_RW else PERM_DELETE


def get_model_perms(model, access):
    perms = {}
    for action in MODEL_ACTIONS:
        codename = "%s_%s" % (action, model.lower())
        perms[codename] = get_perm_method(action, access)
    return perms


def get_all_model_names(apps):
    names = []
    models = apps.get_models()
    for model in models:
        names.append(model.__name__)
    return names


def get_models_permissions(apps, group):
    perms = {}
    for perm in group["perms"]:
        models = (
            get_all_model_names(apps)
            if perm["models"] == MODELS_ALL
            else perm["models"]
        )
        for model in models:
            perms = {**perms, **get_model_perms(model, perm["access"])}
    return perms


def bind_group_permission(apps, group, permission, method):
    if settings.DEBUG:
        print("Configuring permission %s:%s" % (group.name, permission))
    perm_cls = apps.get_model("auth", "Permission")
    perm = perm_cls.objects.get(codename=permission)
    exists = group.permissions.filter(id=perm.id).exists()
    if method == PERM_ENSURE and not exists:
        group.permissions.add(perm)
    elif method == PERM_DELETE and exists:
        group.permissions.remove(perm)


def bind_group_model_permissions(apps, group):
    permissions = get_models_permissions(apps, group)
    for permission, method in permissions.items():
        bind_group_permission(apps, group["instance"], permission, method)


def ready_group(apps, group):
    group_cls = apps.get_model("auth", "Group")
    try:
        instance = group_cls.objects.get(name=group["name"])
    except group_cls.DoesNotExist:
        instance = group_cls(name=group["name"])
        instance.save()
    group["instance"] = instance
    bind_group_model_permissions(apps, group)
    print("Configured group %s" % instance.name)


def configure_groups(sender, apps, **kwargs):
    for group in GROUPS:
        ready_group(apps, group)


class GSuiteConfig(AppConfig):
    name = "gsuite"
    verbose_name = _("Gsuite")

    def ready(self):
        post_migrate.connect(configure_groups, sender=self)
