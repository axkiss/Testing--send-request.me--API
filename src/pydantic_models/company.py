from pydantic import BaseModel, Field

from src.enums.company import CompanySatus


class Company(BaseModel):
    company_id: int = Field(gt=0)
    company_name: str
    company_address: str
    company_status: CompanySatus
