"""Rules Schemas"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, RootModel


class SimpleCondition(BaseModel):
    field: str
    op: Literal["$eq", "$lt", "$gt", "$gte", "$lte"]
    value: Any
    transform: Optional[str] = None
    params: Optional[Dict[str, Any]] = None


class FilterCondition(
    RootModel[
        Union[Dict[Literal["$and", "$or"], List["FilterCondition"]], SimpleCondition]
    ]
):
    pass
