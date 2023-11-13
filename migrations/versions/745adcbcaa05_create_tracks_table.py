"""create temp_tracks table

Revision ID: 745adcbcaa05
Revises: 
Create Date: 2023-11-13 13:00:47.432576

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '745adcbcaa05'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(f"""
    CREATE TABLE IF NOT EXISTS const_tracks (
    id SERIAL PRIMARY KEY,
    playlist_id VARCHAR(255),
    track_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    album VARCHAR(255) NOT NULL,
    album_release_date TEXT NOT NULL,
    duration INT NOT NULL,
    valence FLOAT NOT NULL,
    energy FLOAT NOT NULL,
    tempo FLOAT NOT NULL,
    loudness FLOAT NOT NULL,
    danceability FLOAT NOT NULL
);
""")


def downgrade() -> None:
    op.execute(f"""
    DROP TABLE IF EXISTS const_tracks;
""")