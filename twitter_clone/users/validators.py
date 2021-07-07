from django.core.exceptions import ValidationError


def validate_me_word(content):
    if "me" == content.lower():
        raise ValidationError(f"{content} is not available")
    return content
