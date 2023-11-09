from typing import Optional, List

from pydantic import BaseModel, constr
from ..enums.all import MessageRoles, PromptVersionType


class ModelSettingsBaseModel(BaseModel):
    top_k: float
#     todo: finish this


class PromptTagBaseModel(BaseModel):
    name: str
    data: Optional[dict]

    class Config:
        orm_mode = True


class PromptMessageBaseModel(BaseModel):
    role: MessageRoles
    name: Optional[str]
    content: Optional[str]
    custom_content: Optional[dict]

    class Config:
        orm_mode = True


class PromptVariableBaseModel(BaseModel):
    name: constr(regex=r'^[a-zA-Z_][a-zA-Z0-9_]*$', )
    value: Optional[str]

    class Config:
        orm_mode = True


class PromptVersionBaseModel(BaseModel):
    name: str
    commit_message: Optional[str]
    author_id: int
    context: Optional[str]
    embedding_settings: Optional[dict]
    variables: Optional[List[PromptVariableBaseModel]]
    messages: Optional[List[PromptMessageBaseModel]]
    tags: Optional[List[PromptTagBaseModel]]
    model_settings: Optional[ModelSettingsBaseModel]
    embedding_settings: Optional[dict]  # todo: create model for this field
    type: PromptVersionType

    class Config:
        orm_mode = True


class PromptBaseModel(BaseModel):
    name: str
    description: Optional[str]
    owner_id: int
    versions: Optional[List[PromptVersionBaseModel]]

    class Config:
        orm_mode = True


class AuthorBaseModel(BaseModel):
    id: int
    email: str
