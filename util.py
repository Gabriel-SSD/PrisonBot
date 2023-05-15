def to_pascal_case(string):
    string = string.strip()
    string = string.replace("'", " ")
    string = ' '.join(string.split())
    string = string.lower()
    words = string.split(' ')
    words = [word.capitalize() for word in words if word]
    pascal_case_string = ''.join(words)
    return pascal_case_string


def f_to_c(temp_f):
    return round((temp_f - 32) * 5 / 9, 1)
