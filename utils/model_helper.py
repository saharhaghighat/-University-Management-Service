from django.core.validators import RegexValidator


def user_image_path(instance, filename):
    ext = filename.split(".")[-1]
    return f"profile_images/user_{instance.id}.{ext}"


phone_regex = RegexValidator(
    regex=r"^09\d{9}$",
    message="The phone number is wrong. The phone number must be 11 digits and start with 09",
)

national_code_regex = RegexValidator(
    regex=r"^\d{10}$",
    message="The national code is wrong.",
)
