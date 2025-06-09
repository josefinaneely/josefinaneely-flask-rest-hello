from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Text, Float, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# Tabla asociativa para Post y Tag (muchos a muchos)
post_tag = db.Table(
    'post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey(
        'post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# Tabla asociativa para Product y Tag (muchos a muchos)
product_tag = db.Table(
    'product_tag',
    db.Column('product_id', db.Integer, db.ForeignKey(
        'product.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relación uno a muchos: User -> Post, Comment, Product
    posts = relationship("Post", backref="user")
    comments = relationship("Comment", backref="user")
    products = relationship("Product", backref="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Relación muchos a muchos con Tag
    tags = relationship("Tag", secondary=post_tag, backref="posts")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_url": self.image_url,
            "description": self.description,
            "tags": [tag.serialize() for tag in self.tags]
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    post = relationship("Post", backref="comments")

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "content": self.content,
        }


class Product(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    pricing: Mapped[float] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relación muchos a muchos con Tag
    tags = relationship("Tag", secondary=product_tag, backref="products")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "pricing": self.pricing,
            "weight": self.weight,
            "color": self.color,
            "tags": [tag.serialize() for tag in self.tags]
        }


class Tag(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
