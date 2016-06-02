

"""
    Check if 's' is a string of digit.
    @:param s - the string to verify
    @:return true or false
"""
def check_int(s):
    if s[0] in ('+'):
    	return s[1:].isdigit()
    return s.isdigit()
