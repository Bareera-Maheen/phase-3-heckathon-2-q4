from typing import Optional, List
from pydantic import BaseModel, Field

class NeonBranch(BaseModel):
    id: str
    name: str
    project_id: str
    parent_id: Optional[str] = None
    status: str
    host: Optional[str] = None

class NeonProject(BaseModel):
    id: str
    name: str
    region_id: str

class NeonConnectionString(BaseModel):
    uri: str
    pooled_uri: str
    
    @property
    def connection_string(self) -> str:
        return self.pooled_uri
