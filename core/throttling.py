from rest_framework.throttling import UserRateThrottle


class LowMinuteUserRateThrottle(UserRateThrottle):
    scope = 'low-minute-user'


class LowSecondUserRateThrottle(UserRateThrottle):
    scope = 'low-second-user'


class PublicMinuteUserRateThrottle(UserRateThrottle):
    scope = 'public-minute-user'


class PublicSecondUserRateThrottle(UserRateThrottle):
    scope = 'public-second-user'


class PaginationMinuteUserRateThrottle(UserRateThrottle):
    scope = 'pagination-minute-user'


class PaginationSecondUserRateThrottle(UserRateThrottle):
    scope = 'pagination-second-user'


class OnePerSecondRateThrottle(UserRateThrottle):
    scope = 'one-per-second'


class FivePerMinuteRateThrottle(UserRateThrottle):
    scope = 'five-per-minute'
