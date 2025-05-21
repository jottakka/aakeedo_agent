from pydantic import BaseModel, Field, HttpUrl


class UserData(BaseModel):
    """
    Represents the core user-specific data from the WaniKani API /user endpoint.
    Focuses on username and level as per requirements.
    """

    username: str = Field(..., description="The user's WaniKani username.")
    level: int = Field(
        ..., description="The user's current WaniKani level. WaniKani levels range from 1 to 60."
    )

    class Config:
        extra = "ignore"


class UserResponse(BaseModel):
    """
    Represents the main structure of the WaniKani API response for the /user endpoint.
    The actual user details are nested under the 'data' key.
    """

    object: str = Field(..., description="The type of object returned, typically 'user'.")
    url: HttpUrl = Field(..., description="The API URL that was requested.")
    data_updated_at: str | None = Field(
        None, description="Timestamp of when the data for this resource was last updated."
    )
    data: UserData = Field(
        ..., description="The nested object containing the user's specific data."
    )

    class Config:
        extra = "ignore"
