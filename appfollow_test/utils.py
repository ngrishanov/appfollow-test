from functools import wraps

from sanic import response


def validate_args(schema):
    def decorator(func):
        @wraps(func)
        async def func_wrapper(request, *args, **kwargs):
            errors = []

            for field, params in schema.items():
                value = request.args.get(field)

                if not value:
                    continue

                if params['type'] == 'int':
                    try:
                        value = int(value)

                        if value < params['min']:
                            errors.append({
                                'field': field,
                                'code': 'too_small',
                                'param': params['min'],
                            })
                        elif value > params['max']:
                            errors.append({
                                'field': field,
                                'code': 'too_big',
                                'param': params['max'],
                            })
                    except ValueError:
                        errors.append({
                            'field': field,
                            'code': 'invalid_value',
                        })

                if params['type'] == 'str':
                    if value not in params['allowed_values']:
                        errors.append({
                            'field': field,
                            'code': 'not_allowed',
                            'param': params['allowed_values'],
                        })

            if errors:
                return response.json({
                    'success': False,
                    'errors': errors,
                }, status=400)

            return await func(request, *args, **kwargs)

        return func_wrapper

    return decorator
