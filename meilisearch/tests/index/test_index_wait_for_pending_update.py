from datetime import datetime
import pytest

class TestUpdate:

    """ TESTS: wait_for_pending_update method """

    def test_wait_for_pending_update_default(self, indexed_small_movies):
        """Tests waiting for an update with default parameters"""
        response = indexed_small_movies[0].add_documents([{'id': 1, 'title': 'Le Petit Prince'}])
        assert 'updateId' in response
        update = indexed_small_movies[0].wait_for_pending_update(response['updateId'])
        assert isinstance(update, object)
        assert 'status' in update
        assert update['status'] != 'enqueued'

    def test_wait_for_pending_update_timeout(self, indexed_small_movies, small_movies):
        """Tests timeout risen by waiting for an update"""
        with pytest.raises(TimeoutError):
            indexed_small_movies[0].wait_for_pending_update(2, timeout_in_ms=0)

    def test_wait_for_pending_update_interval_custom(self, indexed_small_movies, small_movies):
        """Tests call to wait for an update with custom interval"""
        response = indexed_small_movies[0].add_documents(small_movies)
        assert 'updateId' in response
        start_time = datetime.now()
        wait_update = indexed_small_movies[0].wait_for_pending_update(
            response['updateId'],
            interval_in_ms=1000,
            timeout_in_ms=6000
        )
        time_delta = datetime.now() - start_time
        assert isinstance(wait_update, object)
        assert 'status' in wait_update
        assert wait_update['status'] != 'enqueued'
        assert time_delta.seconds >= 1

    def test_wait_for_pending_update_interval_zero(self, indexed_small_movies, small_movies):
        """Tests call to wait for an update with custom interval"""
        response = indexed_small_movies[0].add_documents(small_movies)
        assert 'updateId' in response
        wait_update = indexed_small_movies[0].wait_for_pending_update(
            response['updateId'],
            interval_in_ms=0,
            timeout_in_ms=6000
        )
        assert isinstance(wait_update, object)
        assert 'status' in wait_update
        assert wait_update['status'] != 'enqueued'
