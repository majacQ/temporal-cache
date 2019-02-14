from datetime import timedelta, datetime


class TestUtils:
    def test_calc(self):
        from temporalcache.utils import calc
        assert calc(7, 6, 5, 4, 3, 2, 1) == 70002367

    def test_should_expire_seconds(self):
        from temporalcache.utils import should_expire

        now = datetime(2018, 1, 1, 1, 1, 0)
        next_second = now + timedelta(seconds=1)
        next_secondp = now + timedelta(seconds=2)
        assert should_expire(now, now, 1) == False
        assert should_expire(now, next_second, 1) == False
        assert should_expire(now, next_secondp, 1) == True

        now = datetime(2018, 1, 1, 1, 1, 2)
        next_second = now + timedelta(seconds=7)
        next_second2 = now + timedelta(seconds=59)
        next_secondp = now + timedelta(seconds=61)
        assert should_expire(now, now, 1) == False
        assert should_expire(now, next_second, 1) == False
        assert should_expire(now, next_second2, 1) == False
        assert should_expire(now, next_secondp, 1) == True

    def test_should_expire_minutes(self):
        from temporalcache.utils import should_expire

        now = datetime(2018, 1, 1, 1, 0, 1)
        next_min = now + timedelta(minutes=1)
        next_minp = now + timedelta(minutes=2)
        assert should_expire(now, now, 0, 1) == False
        assert should_expire(now, next_min, 0, 1) == False
        assert should_expire(now, next_minp, 0, 1) == True

        now = datetime(2018, 1, 1, 1, 2, 1)
        next_min = now + timedelta(minutes=5)
        next_min2 = now + timedelta(minutes=59)
        next_minp = now + timedelta(minutes=61)
        assert should_expire(now, now, 0, 1) == False
        assert should_expire(now, next_min, 0, 1) == False
        assert should_expire(now, next_min2, 0, 1) == False
        assert should_expire(now, next_minp, 0, 1) == True

    def test_should_expire_seconds_and_minutes(self):
        from temporalcache.utils import should_expire

        now = datetime(2018, 1, 1, 1, 0, 1)
        next_second = now + timedelta(seconds=1)
        next_min = now + timedelta(minutes=1)
        next_minp = now + timedelta(minutes=2, seconds=1)
        assert should_expire(now, now, 1, 1) == False
        assert should_expire(now, next_second, 1, 1) == False
        assert should_expire(now, next_min, 1, 1) == False
        assert should_expire(now, next_minp, 1, 1) == True

        now = datetime(2018, 1, 1, 1, 2, 0)
        next_min = now + timedelta(minutes=5)
        next_min2 = now + timedelta(minutes=59)
        next_minp = now + timedelta(minutes=61)
        next_minp2 = now + timedelta(minutes=60, seconds=1)
        assert should_expire(now, now, 1, 1) == False
        assert should_expire(now, next_min, 1, 1) == False
        assert should_expire(now, next_min2, 1, 1) == False
        assert should_expire(now, next_minp, 1, 1) == True
        assert should_expire(now, next_minp2, 1, 1) == True

    def test_should_expire_boundary(self):
        from temporalcache.utils import should_expire
        now = datetime(1999, 12, 31, 23, 59, 59)
        next_second = now + timedelta(seconds=1)
        next_secondp = now + timedelta(seconds=2)
        assert should_expire(now, now, 0) == False
        assert should_expire(now, next_second, 0) == False
        assert should_expire(now, next_secondp, 0) == True