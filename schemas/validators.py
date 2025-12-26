from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional

class UserTemplate(BaseModel):
    name: str = Field(..., description="Template name")
    description: Optional[str] = Field(None, description="Template description")
    fields: List[str] = Field(..., description="List of field names to generate")

    @validator('fields')
    def validate_unique_field_names(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("Field names must be unique")
        return v

# Output validation models for generators

class CreditCardOutput(BaseModel):
    number: str
    expiry: str
    provider: str

class UserOutput(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    birth_date: str
    company: str
    job: str
    credit_card: CreditCardOutput

class PenetrationOutput(BaseModel):
    id: str
    timestamp: str
    source_ip: str
    user_agent: str
    session_id: str
    injected_fields: List[str]
    total_injections: int
    injection_types: List[str]
    # Dynamic optional fields
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    comment: Optional[str] = None
    message: Optional[str] = None
    search_query: Optional[str] = None
    file_path: Optional[str] = None
    url: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    # Vulnerability type fields
    username_vulnerability_type: Optional[str] = None
    password_vulnerability_type: Optional[str] = None
    email_vulnerability_type: Optional[str] = None
    first_name_vulnerability_type: Optional[str] = None
    last_name_vulnerability_type: Optional[str] = None
    comment_vulnerability_type: Optional[str] = None
    message_vulnerability_type: Optional[str] = None
    search_query_vulnerability_type: Optional[str] = None
    file_path_vulnerability_type: Optional[str] = None
    url_vulnerability_type: Optional[str] = None
    phone_vulnerability_type: Optional[str] = None
    address_vulnerability_type: Optional[str] = None
    city_vulnerability_type: Optional[str] = None
    country_vulnerability_type: Optional[str] = None
    description_vulnerability_type: Optional[str] = None

# Base output model for flexibility
class BaseOutput(BaseModel):
    class Config:
        extra = 'allow'  # Allow extra fields for extensibility

# Utility functions
def validate_user_template(template_data: Dict[str, Any]) -> UserTemplate:
    """Validate user JSON template"""
    return UserTemplate(**template_data)

def validate_generator_output(generator_type: str, output_data: Dict[str, Any]) -> BaseModel:
    """Validate generator output based on type"""
    if generator_type == "user":
        return UserOutput(**output_data)
    elif generator_type == "penetration":
        return PenetrationOutput(**output_data)
    else:
        # For other types, use base validation
        return BaseOutput(**output_data)

def filter_output_by_template(output_data: Dict[str, Any], template: UserTemplate) -> Dict[str, Any]:
    """Filter generator output to include only fields specified in the template"""
    filtered = {}
    for field in template.fields:
        if field in output_data:
            filtered[field] = output_data[field]
    return filtered