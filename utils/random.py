def get_random_key():
    import uuid
    return uuid.uuid4().hex[:8]
