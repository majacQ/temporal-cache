import datetime
from mock import patch, MagicMock


class TestExpire:
    def setup(self):
        self._olddatetime = datetime.datetime

        class NewDateTime(datetime.datetime):
            @classmethod
            def now(cls):
                ret = self._now + self._delay
                print(self._now)
                print(ret)
                return ret

        datetime.datetime = NewDateTime

    def teardown(self):
        datetime.datetime = self._olddatetime

    def test_blank(self):
        from random import random
        from temporalcache import expire

        self._now = datetime.datetime(2018, 1, 1, 1, 1, 0)
        self._delay = datetime.timedelta(seconds=0)
 
        @expire(1)
        def foo():
            return random()

        print('running first')
        x = foo()
        print('checking cached')
        assert x == foo()

        # expire
        self._delay = datetime.timedelta(seconds=2)
        print('checking cache expired')
        assert x != foo()
        print('success')

    def test_mutable(self):
        from random import random
        from temporalcache import expire

        self._now = datetime.datetime(2018, 1, 1, 1, 1, 1)
        self._delay = datetime.timedelta(seconds=0)

        @expire()
        def foo(*args, **kwargs):
            return random()

        print('running first')
        x = foo([1, 2, 3], test={'a': 1, 'b': 2})
        print('checking cached')
        assert x == foo([1, 2, 3], test={'a': 1, 'b': 2})

        # expire
        self._delay = datetime.timedelta(seconds=61)
        print('checking cache expired')
        assert x != foo([1, 2, 3], test={'a': 1, 'b': 2})
        print('success')

    def test_seconds(self):
        from random import random
        from temporalcache import expire

        self._now = datetime.datetime(2018, 1, 1, 1, 1, 1)
        self._delay = datetime.timedelta(seconds=0)

        @expire()
        def foo():
            return random()

        print('running first')
        x = foo()

        print('checking cached')
        self._delay = datetime.timedelta(seconds=59)
        assert x == foo()

        print('checking cached')

        # expire
        self._delay = datetime.timedelta(seconds=61)
        print('checking cache expired')
        assert x == foo()
        print('success')

    def test_checks(self):
        from random import random
        from temporalcache import expire, TCException

        try:
            @expire(60)
            def foo():
                return random()
            raise Exception('')
        except TCException:
            pass

        try:
            @expire(minute=60)
            def foo():
                return random()
            raise Exception('')
        except TCException:
            pass

        try:
            @expire(hour=24)
            def foo():
                return random()
            raise Exception('')
        except TCException:
            pass

        try:
            @expire(day=0)
            def foo():
                return random()
            raise Exception('')
        except TCException:
            pass


        try:
            @expire(day=32)
            def foo():
                return random()
            raise Exception('')
        except TCException:
            pass

        try:
            @expire(week=0)
            def foo():
                return random()
            raise Exception('')
        except TCException:
            pass


        try:
            @expire(week=6)
            def foo():
                return random()
            raise Exception('')
        except TCException:
            pass

        try:
            @expire(month=0)
            def foo():
                return random()
            raise Exception('')
        except TCException:
            pass

        try:
            @expire(month=13)
            def foo():
                return random()
            raise Exception('')
        except TCException:
            pass