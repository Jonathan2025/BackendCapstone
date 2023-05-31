from django.core.exceptions import ValidationError

def file_size(value):
    file_size = value.size 
    if file_size > 100000000: #if the file is more than 10 mb then raise an error 
        raise ValidationError("Maximum file size is 100 mb")
