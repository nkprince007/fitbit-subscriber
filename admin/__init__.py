from django import forms
from django.apps import AppConfig
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db.models import Model, ManyToManyField


class DisplayAllAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ManyToManyField: {'widget': forms.CheckboxSelectMultiple}
    }

    def __init__(self, model, site):
        self.list_display = [field.name for field in model._meta.fields]
        super(DisplayAllAdmin, self).__init__(model, site)


class _GenericModelFormTemplate(forms.ModelForm):
    # template methods / search fields go in here
    pass


class _GenericModelAdminTemplate(DisplayAllAdmin):
    # any relevant behavioural specifics
    search_fields = ('id', )


class _GenericModelFormMeta(type):
    """
    A meta class to control admin form generation.

    Reference: http://stackoverflow.com/a/6581949
    """
    def __new__(cls, clsname, bases, attrs):
        # making sure we are using the correct class
        if len(bases) < 1:  # pragma: no cover
            raise ValueError('GenericAdminForm requires a base class')
        assert issubclass(bases[0], Model)

        meta = type('GenericAdminModelFormMeta',
                    (object, ),
                    {'model': bases[0], 'fields': '__all__'})
        class_dict = {'Meta': meta}

        # add user overrides, if specified
        class_dict.update(attrs)
        model_form = type(
            bases[0].__name__ + 'ModelForm',
            (_GenericModelFormTemplate, ),
            class_dict)
        return model_form


class _GenericModelAdminMeta(type):
    """
    ``type()`` magic for the ModelAdmin class.
    """
    def __new__(cls, clsname, bases, attrs):
        # making sure we are using the correct class
        if len(bases) < 1:  # pragma: no cover
            raise ValueError('GenericAdminForm requires a base class')

        # django ModelAdmin classes are required to have a Meta member class
        # with a 'model' attribute that points to the model type
        meta = type('GenericAdminModelAdminMeta',
                    (object, ),
                    {'model': bases[0]})
        class_dict = {'Meta': meta}

        # we want all our generic form behaviours to be inherited as well, so
        # add these to the attribute dict.
        class_dict['form'] = _GenericModelFormMeta(
            clsname, bases, attrs)
        class_dict.update(attrs)
        model_admin = type(
            bases[0].__name__ + 'ModelAdmin',
            (_GenericModelAdminTemplate, ),
            class_dict)
        return model_admin


def register_models(models, mixins=None, **attr_dict):
    if mixins is None:
        mixins = ()

    mixins = tuple(mixins)
    models = list(models)

    model_admins = [
        _GenericModelAdminMeta(x.__name__, (x,) + mixins, attr_dict)
        for x in models
    ]

    for model, model_admin in zip(models, model_admins):
        try:
            admin.site.register(model, model_admin)
        except AlreadyRegistered:
            pass


class AdminAppConfig(AppConfig):
    def ready(self):
        register_models(self.get_models())
