import sqlalchemy as sa
from szurubooru.model.base import Base
from szurubooru.model.post import Post, PostScore, PostFavorite
from szurubooru.model.comment import Comment


class User(Base):
    __tablename__ = 'user'

    AVATAR_GRAVATAR = 'gravatar'
    AVATAR_MANUAL = 'manual'

    RANK_ANONYMOUS = 'anonymous'
    RANK_RESTRICTED = 'restricted'
    RANK_REGULAR = 'regular'
    RANK_POWER = 'power'
    RANK_MODERATOR = 'moderator'
    RANK_ADMINISTRATOR = 'administrator'
    RANK_NOBODY = 'nobody'  # unattainable, used for privileges

    user_id = sa.Column('id', sa.Integer, primary_key=True)
    creation_time = sa.Column('creation_time', sa.DateTime, nullable=False)
    last_login_time = sa.Column('last_login_time', sa.DateTime)
    version = sa.Column('version', sa.Integer, default=1, nullable=False)
    name = sa.Column('name', sa.Unicode(50), nullable=False, unique=True)
    password_hash = sa.Column('password_hash', sa.Unicode(64), nullable=False)
    password_salt = sa.Column('password_salt', sa.Unicode(32))
    email = sa.Column('email', sa.Unicode(64), nullable=True)
    rank = sa.Column('rank', sa.Unicode(32), nullable=False)
    avatar_style = sa.Column(
        'avatar_style', sa.Unicode(32), nullable=False,
        default=AVATAR_GRAVATAR)

    comments = sa.orm.relationship('Comment')

    @property
    def post_count(self) -> int:
        from szurubooru.db import session
        return (
            session
            .query(sa.sql.expression.func.sum(1))
            .filter(Post.user_id == self.user_id)
            .one()[0] or 0)

    @property
    def comment_count(self) -> int:
        from szurubooru.db import session
        return (
            session
            .query(sa.sql.expression.func.sum(1))
            .filter(Comment.user_id == self.user_id)
            .one()[0] or 0)

    @property
    def favorite_post_count(self) -> int:
        from szurubooru.db import session
        return (
            session
            .query(sa.sql.expression.func.sum(1))
            .filter(PostFavorite.user_id == self.user_id)
            .one()[0] or 0)

    @property
    def liked_post_count(self) -> int:
        from szurubooru.db import session
        return (
            session
            .query(sa.sql.expression.func.sum(1))
            .filter(PostScore.user_id == self.user_id)
            .filter(PostScore.score == 1)
            .one()[0] or 0)

    @property
    def disliked_post_count(self) -> int:
        from szurubooru.db import session
        return (
            session
            .query(sa.sql.expression.func.sum(1))
            .filter(PostScore.user_id == self.user_id)
            .filter(PostScore.score == -1)
            .one()[0] or 0)

    __mapper_args__ = {
        'version_id_col': version,
        'version_id_generator': False,
    }
