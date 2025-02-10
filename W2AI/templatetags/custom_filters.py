from django import template

register = template.Library()

@register.filter
def split_range(value):
    return value.split(' - ')

@register.filter
def convert(value):
    value1=''
    if value[2] != ' ' and value[3] != '':
        value1 = value1 + value[:2] + ' '+value[2] + ' ' + value[3:]
    return value1

@register.filter
def tolerance_calci(value):
    return int(value) - ((int(value)/100 * 25/100)*100)

@register.filter
def tolerance_water(value):
    return int(value) - ((int(value)/100 * 10/100)*100)

@register.filter
def convert(value):
    return str(value).replace('{','').replace('}','').replace("'",'')

@register.filter
def convert_list(value):
    return str(value).replace('[','').replace(']','').replace("'",'')

@register.filter
def typeofval(val):
    return type(val)

@register.filter
def starDisplay(maxval):
    if type(maxval) == int:
        return range(1, maxval)
    else:
        return range(0, int(maxval))
    
@register.filter
def split_loc(text):
    return text.split(',')

@register.filter
def is_temp_in_range(temp, range_str):
   
    try:
        # Ensure temp is a float
        temp = float(temp)
        # Ensure range_str is correctly split and converted
        min_temp, max_temp = map(float, range_str.split(' to '))
        return min_temp <= temp <= max_temp
    except (ValueError, TypeError):
        # Handle cases where conversion fails or range_str is invalid
        return False
    
@register.filter
def multiply_spacing(value):
    try:
        dimensions = value.split('*')
        return int(dimensions[0]) * int(dimensions[1])
    except (ValueError, IndexError):
        return None
    
@register.filter
def convert_int(value):
    a=int(value)
    return a