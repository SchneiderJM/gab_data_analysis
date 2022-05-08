from typing import Optional
import datetime
from sqlmodel import Field, Session, SQLModel, create_engine

class posts(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	gab_id: int
	content: str
	created_at: datetime.datetime
	revised_at: datetime.datetime
	favourites_count: int
	reblogs_count: int
	replies_count: int
	id_gab_users: int
	
	
class comments(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	content: str
	created_at: datetime.datetime
	gab_id: int
	id_gab_users: int
	in_reply_to_id: int
	reblogs_count: int
	replies_count: int
	revised_at: datetime.datetime
	
	
class gab_users(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	account_created_at: datetime.datetime
	account_note: str
	created_at: datetime.datetime
	display_name: str
	gab_id: int
	is_verified: int
	name: str
	username: str