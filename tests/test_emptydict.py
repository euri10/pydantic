from typing import Dict, Any

import pytest

from pydantic import PydanticTypeError, BaseModel, ValidationError
from pydantic.validators import dict_validator


class NotEmptyDictError(PydanticTypeError):
    msg_template = 'empty dict not an allowed value'


class NotEmptyDict(Dict):
    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield dict_validator
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> Dict:
        if not v:
            raise NotEmptyDictError()
        return v


def test_empty_dict():
    class Model(BaseModel):
        v: NotEmptyDict

    assert Model(v={"key":"value"}).v == {"key": "value"}

    with pytest.raises(ValidationError):
        Model(v={})

    with pytest.raises(ValidationError):
        Model(v=1)