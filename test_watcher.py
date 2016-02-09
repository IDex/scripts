import unittest
import shutil
import os
from watcher import Watcher


class TestWatcher(unittest.TestCase):

    def setUp(self):
        self.w = Watcher('', os.path.dirname(
            os.path.realpath(__file__)) + '/test/')
        self.w.savefile = '/test/test_watched.json'
        self.w.watched = []
        self.w.save()

    def tearDown(self):
        try:
            os.remove(os.path.dirname(
                os.path.realpath(__file__)) + self.w.savefile)
        except FileNotFoundError:
            pass

    def test_find(self):
        w = self.w
        w.matches = w.find('')
        self.assertEqual(w.matches[0], 'test.jpg')

    def test_clear(self):
        self.w.watched.append('test.jpg')
        self.w.watched.append('keep.jpg')
        self.w.clear('te')
        assert 'keep.jpg' in self.w.watched
        assert 'test.jpg' not in self.w.watched
        self.w.watched.append('test2.jpg')
        self.w.clear('.')
        self.assertFalse(self.w.watched)

    def test_nosave(self):
        self.w.nosave = True
        self.w.watched.append('test')
        self.w.save()
        assert not self.w.load()

    def test_remove(self):
        shutil.copy(self.w.folder + '/test.jpg', self.w.folder + '/remove')
        self.w.watched.append('remove')
        self.w.watched.append('testdir/')
        self.w.remove()
        assert not os.path.isfile(self.w.folder + '/remove')

    def test_ignore(self):
        self.w.watched.append('test.jpg')
        assert self.w.find('', include_watched=True)

if __name__ == '__main__':
    unittest.main()
