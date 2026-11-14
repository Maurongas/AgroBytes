from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """En Python se escribe snake_case; en el JSON de la API sale camelCase (como lo usa el frontend)."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)
