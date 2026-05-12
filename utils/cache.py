import json

import six
from django_redis import get_redis_connection
from django_redis.compressors.identity import IdentityCompressor
from django_redis.exceptions import CompressorError
from django_redis.serializers.pickle import PickleSerializer

from config.settings import CACHE_TTL


class EncodeDecode:
    def __init__(self):
        self._serializer = PickleSerializer(options={})
        self._compressor = IdentityCompressor(options={})

    def decode(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            try:
                value = self._compressor.decompress(value)
            except CompressorError:
                pass

            try:
                value = self._serializer.loads(value)
            except Exception:
                try:
                    value = json.loads(value)
                except (json.decoder.JSONDecodeError, TypeError, AttributeError):
                    value = value.decode("utf-8") if hasattr(value, "decode") else value
        return value

    def encode(self, value):
        if isinstance(value, bool) or not isinstance(value, six.integer_types):
            value = self._serializer.dumps(value)
            value = self._compressor.compress(value)
            return value
        return value


c = EncodeDecode()


def _prefixed_key(key):
    return f"django-api:1:{key}"


def get_cache(key):
    redis = get_redis_connection("default")
    value = redis.get(_prefixed_key(key))
    return c.decode(value) if value else None


def set_cache(key, data, ttl=CACHE_TTL):
    redis = get_redis_connection("default")
    redis.set(_prefixed_key(key), c.encode(data), ttl)


def delete_cache(key):
    redis = get_redis_connection("default")
    redis.delete(_prefixed_key(key))


def delete_by_pattern(pattern):
    redis = get_redis_connection("default")
    match_pattern = f"django-api:1:{pattern}*"

    try:
        for key in redis.scan_iter(match_pattern):
            redis.delete(key)
    except Exception as exc:
        raise Exception(f"Erro ao excluir: {pattern} - {str(exc)}") from exc
