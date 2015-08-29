import unittest
import devedeng.avbase

class TestAVConv(unittest.TestCase):

    def test_ubuntu_14_04(self):
        c = devedeng.avbase.avbase()
        c.check_version_txt("""avconv version 9.18-6:9.18-0ubuntu0.14.04.1, Copyright (c) 2000-2014 the Libav developers
  built on Mar 16 2015 13:19:10 with gcc 4.8 (Ubuntu 4.8.2-19ubuntu1)
avconv 9.18-6:9.18-0ubuntu0.14.04.1
libavutil     52.  3. 0 / 52.  3. 0
libavcodec    54. 35. 0 / 54. 35. 0
libavformat   54. 20. 4 / 54. 20. 4
libavdevice   53.  2. 0 / 53.  2. 0
libavfilter    3.  3. 0 /  3.  3. 0
libavresample  1.  0. 1 /  1.  0. 1
libswscale     2.  1. 1 /  2.  1. 1""".split("\n"))

        self.assertEqual(c.major_version, 9, "Detecting major version for Ubuntu 14.04's AVConv version")
        self.assertEqual(c.minor_version, 18, "Detecting minor version for Ubuntu 14.04's AVConv version")


    def test_ubuntu_14_10(self):
        c = devedeng.avbase.avbase()
        c.check_version_txt("""avconv version 11-6:11-1, Copyright (c) 2000-2014 the Libav developers
  built on Sep 26 2014 14:36:31 with gcc 4.9.1 (Ubuntu 4.9.1-15ubuntu1)
avconv 11-6:11-1
libavutil     54.  3. 0 / 54.  3. 0
libavcodec    56.  1. 0 / 56.  1. 0
libavformat   56.  1. 0 / 56.  1. 0
libavdevice   55.  0. 0 / 55.  0. 0
libavfilter    5.  0. 0 /  5.  0. 0
libavresample  2.  1. 0 /  2.  1. 0
libswscale     3.  0. 0 /  3.  0. 0""".split("\n"))

        self.assertEqual(c.major_version, 11, "Detecting major version for Ubuntu 14.10's AVConv version")
        self.assertEqual(c.minor_version, 0, "Detecting minor version for Ubuntu 14.10's AVConv version")


    def test_ubuntu_15_04(self):
        c = devedeng.avbase.avbase()
        c.check_version_txt("""avconv version 11.2-6:11.2-1, Copyright (c) 2000-2014 the Libav developers
  built on Jan 18 2015 05:12:33 with gcc 4.9.2 (Ubuntu 4.9.2-10ubuntu2)
avconv 11.2-6:11.2-1
libavutil     54.  3. 0 / 54.  3. 0
libavcodec    56.  1. 0 / 56.  1. 0
libavformat   56.  1. 0 / 56.  1. 0
libavdevice   55.  0. 0 / 55.  0. 0
libavfilter    5.  0. 0 /  5.  0. 0
libavresample  2.  1. 0 /  2.  1. 0
libswscale     3.  0. 0 /  3.  0. 0""".split("\n"))

        self.assertEqual(c.major_version, 11, "Detecting major version for Ubuntu 15.04's AVConv version")
        self.assertEqual(c.minor_version, 2, "Detecting minor version for Ubuntu 15.04's AVConv version")


if __name__ == '__main__':
    unittest.main()