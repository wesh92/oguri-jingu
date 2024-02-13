from pydantic import BaseModel, Field, model_validator


class MetaModel(BaseModel):
    """
    A model for the meta data of a model
    """

    name: str = Field(..., description="The name of the model", alias="n")
    asset_hash: str = Field(..., description="The hash of the model", alias="h")
    meta_group: str = Field(..., description="The meta group of the model", alias="m")
    folder_key: str | None
    region: str

    # Set the folder key by getting the first 2 characters of the asset hash
    @model_validator(mode="before")
    @classmethod
    def set_folder_key(cls, values) -> dict | None:
        values["folder_key"] = values["h"][:2]
        return values
