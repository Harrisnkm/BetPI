from django import template

register = template.Library()

@register.filter()
def decimalToAmerican(value):
    '''Converts Decimal to American'''
    #check if value is less 2.00
    if value >= 2:
        return (value - 1)*100
        #if yes return: 2.00: (2.00 – 1)*100 = 1*100 = +100
    #if else:
    else:
        return ((-100)/(value-1))
        #(-100)/(1.9091 – 1) = (-100)/(0.9091) = -109.99 = -110
