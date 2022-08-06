#!/usr/bin/env python3

import os
import re
import mailbox

class TestMbox:
    def __init__(self):
        self._path = '/tmp/test.mbox'

    def setup(self):
        os.unlink(self._path)
        self._box = mailbox.mbox(self._path)

    def assertEqual(self, actual, expected):
        if actual == expected:
            print("OK!")
        else:
            print(f"exp: {expected}")
            print(f"act: {actual}")

    # Test reading an mbox file with un-prefixed From in body text
    # currently generates 2 messages
    def _test_read_mbox(self, matcher=0, count=2):
        # create a basic mbox file
        self.setup()
        self._box.add('From: foo\n\nHello\n')
        # Add an un-prefixed From to create a second entry
        self._box._file.write(b'From time to time\n')
        self._box.close()
        # re-read it using the provided matcher
        if matcher == 0: # not provided, so omit
            self._box = mailbox.mbox(self._path, create=False)
        else:
            self._box = mailbox.mbox(self._path, create=False, from_matcher=matcher)
        # How many messages were found?
        self.assertEqual(len(self._box.keys()), count)

    def test_read_mbox_omitted(self):
        self._test_read_mbox()

    def test_read_mbox_none(self):
        self._test_read_mbox(None)

    def test_read_mbox_default(self):
        self._test_read_mbox(lambda line: re.match(b'From ', line))

    def test_read_mbox_regex1(self):
        import re
        # stricter matching should only find one message
        self._test_read_mbox(lambda line: re.match(b'From .+ \\d\\d\\d\\d\\r?\\n', line), count=1)

    def test_read_mbox_regex2(self):
        import re
        # invalid, so don't find any messages
        self._test_read_mbox(lambda line: re.match(b'From .+ \\d\\d\\d\\r?\\n', line), count=0)

tm = TestMbox()
tm.test_read_mbox_omitted()
tm.test_read_mbox_none()
tm.test_read_mbox_default()
tm.test_read_mbox_regex1()
tm.test_read_mbox_regex2()