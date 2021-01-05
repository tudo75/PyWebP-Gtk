#
#  MIT License
#
#  Copyright (c) 2019-2021 Nicola Tudino aka tudo75
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#

from unittest import TestCase, main, expectedFailure

from pywebp import helpers


class HelpersTest(TestCase):
    """Helpers Tests.
    """

    def test_sizeof_fmt(self):
        """Format filesize in human-readable format."""
        readable_size = helpers.sizeof_fmt(100)
        self.assertEqual(readable_size, "100B")
        readable_size = helpers.sizeof_fmt(10240)
        self.assertEqual(readable_size, "10.0K")
        huge_size = 1024 ** 8 * 12
        readable_size = helpers.sizeof_fmt(huge_size)
        self.assertEqual(readable_size, "12.0Y")

    def test_error_message(self):
        """Error message popup."""
        # Not much can happen here, if all attributes are set correctly it will
        # also run
        helpers.error_message("Test error", True)

    def test_get_boolean(self):
        is_bool = helpers.get_boolean("TRUE")
        self.assertEqual(is_bool, True)
        is_bool = helpers.get_boolean("YES")
        self.assertEqual(is_bool, True)
        is_not_bool = helpers.get_boolean("FALSE")
        self.assertEqual(is_not_bool, False)
        is_not_bool = helpers.get_boolean("fer")
        self.assertEqual(is_not_bool, False)
        # Raise Exceptions
        self.assertRaises(AttributeError, helpers.get_boolean, 12)

    # TODO missing tests

if __name__ == "__main__":
    main()


