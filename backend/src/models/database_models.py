from typing import Optional
import datetime
from sqlmodel import Field, Session, SQLModel, create_engine

class Post(SQLModel, table=True):
	__tablename__: str = 'posts'
	
	id: Optional[int] = Field(default=None, primary_key=True)
	gab_id: int
	content: str
	created_at: datetime.datetime
	revised_at: datetime.datetime
	favourites_count: int
	reblogs_count: int
	replies_count: int
	id_gab_users: int
	reactions_counts: dict
	
	
class Comment(SQLModel, table=True):
	__tablename__: str = 'comments'

	id: Optional[int] = Field(default=None, primary_key=True)
	content: str
	created_at: datetime.datetime
	gab_id: int
	id_gab_users: int
	in_reply_to_id: int
	reblogs_count: int
	replies_count: int
	revised_at: datetime.datetime
	reactions_counts: dict
	
	
class GabUser(SQLModel, table=True):
	__tablename__: str = 'gab_users'

	id: Optional[int] = Field(default=None, primary_key=True)
	gab_id: int
	account_created_at: datetime.datetime
	account_note: str
	created_at: datetime.datetime
	display_name: str
	gab_id: int
	is_verified: int
	name: str
	username: str
	num_followers: int
	is_bot: bool
	is_donor: bool