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
    ProfileInlineFormset = inlineformset_factory(User, UserSmsProfile, fields=('sms_number',))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/accounts/profile/')

        return render(request, "accounts/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
