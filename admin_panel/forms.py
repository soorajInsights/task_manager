from django import forms
from accounts.models import CustomUser

class CreateAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    class Meta:
        model = CustomUser
        # Force role to ADMIN by the view unless SuperAdmin specifically sets SUPERADMIN
        fields = ("username", "email", "first_name", "last_name", "role", "password")

    def clean_role(self):
        role = self.cleaned_data.get("role")
        # Only allow ADMIN or SUPERADMIN values; SuperAdmin only via server-side check
        if role not in ("ADMIN", "SUPERADMIN"):
            raise forms.ValidationError("Invalid role.")
        return role

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
