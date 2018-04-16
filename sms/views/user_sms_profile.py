from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sms.models import UserSmsProfile
from sms.forms import UserForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied


@login_required() # only logged in users should access this
def edit_user(request, pk):

    # querying the User object with pk from url
    user = User.objects.get(pk=pk)
    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)
    # The sorcery begins from here, see explanation below
    ProfileInlineFormset = inlineformset_factory(User, UserSmsProfile, fields=('event_tags', 'get_notifications'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:

        user_sms_profile = UserSmsProfile.objects.get(user=user)

        if user_sms_profile.sms_number:
            user_sms_number = user_sms_profile.sms_number
        else:
            user_sms_number = None

        # TODO: refactor this to use PUT since it is only updating
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():

                existing_user = User.objects.filter(username=user_form.user.username)
                if existing_user.count():
                    user_instance = existing_user.first()
                else:
                    user_instance = user_form.save(commit=False)

                formset = ProfileInlineFormset(request.POST, request.FILES, instance=user_instance)

                if formset.is_valid():
                    user_instance.save()
                    formset.save()

        return render(request, "accounts/account_update.html", {
            "user_sms_number": user_sms_number,
            "user_pk": pk,
            "user_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
