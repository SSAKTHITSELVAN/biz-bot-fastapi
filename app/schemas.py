# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class CreateBizSchema(BaseModel):
    """
    Schema for a business requirement post.
    """
    title: Optional[str] = Field(default=None, description="A concise and compelling title for the business post")
    description: Optional[str] = Field(default=None, description="A detailed description of the business requirement")
    location: Optional[str] = Field(default=None, description="The desired location for the supplier or service")
    quantity: Optional[str] = Field(default=None, description="The total quantity of the product needed")
    unit: Optional[str] = Field(default=None, description="The unit of measurement for the quantity")
    min_budget: Optional[str] = Field(default=None, description="The minimum budget for the entire order")
    max_budget: Optional[str] = Field(default=None, description="The maximum budget for the entire order")
    certifications: Optional[str] = Field(default=None, description="Required certifications or standards")
    
    class Config:
        # This ensures all fields are always included in the response
        extra = 'forbid'