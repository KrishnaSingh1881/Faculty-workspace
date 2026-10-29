"""Native pgvector storage with a JSON representation for isolated SQLite tests."""

import json
import math

from sqlalchemy.types import JSON, TypeDecorator, UserDefinedType

MAX_DIMENSIONS = 16000


def checked_vector(value):
    if not isinstance(value, (list, tuple)) or not 1 <= len(value) <= MAX_DIMENSIONS:
        raise ValueError(f"Embedding dimensions must be 1 through {MAX_DIMENSIONS}")
    if any(isinstance(item, bool) or not isinstance(item, (int, float)) or not math.isfinite(item) for item in value):
        raise ValueError("Embedding values must be finite numbers")
    if not any(value):
        raise ValueError("A zero vector cannot be used for cosine search")
    return [float(item) for item in value]


class NativeVector(UserDefinedType):
    cache_ok = True

    def get_col_spec(self, **kwargs):
        # No fixed dimension: exact pgvector search supports all configured model
        # dimensions. Queries always constrain model digest and dimension first.
        return "VECTOR"


class Vector(TypeDecorator):
    impl = JSON
    cache_ok = True

    @property
    def python_type(self):
        return list

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(NativeVector() if dialect.name == "postgresql" else JSON())

    def process_bind_param(self, value, dialect):
        vector = checked_vector(value)
        return json.dumps(vector, separators=(",", ":")) if dialect.name == "postgresql" else vector

    def process_result_value(self, value, dialect):
        return json.loads(value) if isinstance(value, str) else value
