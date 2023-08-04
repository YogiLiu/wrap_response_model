from inspect import iscoroutinefunction
from functools import wraps
from typing import Optional

from fastapi import HTTPException
from pydantic import create_model


def wrap_model(fn: callable):
    return_type = fn.__annotations__.get("return", None)
    if return_type:
        model = create_model(
            'WrappedResponseModel',
            code = (int, 0),
            msg = (str, 'OK'),
            data = (Optional[return_type], None)
        )
        fn.__annotations__['return'] = model

    @wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            if iscoroutinefunction(fn):
                resp = await fn(*args, **kwargs)
            else:
                resp = fn(*args, **kwargs)
            resp = {
                'code': 0,
                'msg': 'OK',
                'data': resp
            }
        except HTTPException as e:
            resp = {
                'code': e.status_code,
                'msg': e.detail,
                'data': None
            }
        return resp
    
    return wrapper