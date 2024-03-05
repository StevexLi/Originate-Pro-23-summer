def error_code_change(code):
    match code:
        case 'min_length':
            res = 1001
        case 'max_length':
            res = 1002
        case 'required':
            res = 1003
        case 'invalid':
            res = 1004
        case _:
            res = code
    return res

def get_first_error(invalid_form):
    error = invalid_form.errors.get_json_data()
    error_iter = iter(error)
    error_key = next(error_iter)
    error_list = error[error_key][0]
    code = error_code_change(error_list['code'])
    message = error_list['message']
    return code, message
