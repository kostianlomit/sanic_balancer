from pydantic import BaseModel


# для чтения серверов-origin
class Origin(BaseModel):
    id: int
    url_server: str


