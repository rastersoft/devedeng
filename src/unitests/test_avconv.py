import unittest
import devedeng.avbase
import devedeng.avprobe

class TestAVConv(unittest.TestCase):

    def test_ubuntu_14_04(self):
        c = devedeng.avbase.avbase()
        text = """avconv version 9.18-6:9.18-0ubuntu0.14.04.1, Copyright (c) 2000-2014 the Libav developers
  built on Mar 16 2015 13:19:10 with gcc 4.8 (Ubuntu 4.8.2-19ubuntu1)
avconv 9.18-6:9.18-0ubuntu0.14.04.1
libavutil     52.  3. 0 / 52.  3. 0
libavcodec    54. 35. 0 / 54. 35. 0
libavformat   54. 20. 4 / 54. 20. 4
libavdevice   53.  2. 0 / 53.  2. 0
libavfilter    3.  3. 0 /  3.  3. 0
libavresample  1.  0. 1 /  1.  0. 1
libswscale     2.  1. 1 /  2.  1. 1""".split("\n")
        text.append(9)
        c.check_version_txt(text)

        self.assertEqual(c.major_version, 9, "Detecting major version for Ubuntu 14.04's AVConv version")
        self.assertEqual(c.minor_version, 18, "Detecting minor version for Ubuntu 14.04's AVConv version")


    def test_ubuntu_14_10(self):
        c = devedeng.avbase.avbase()
        text = """avconv version 11-6:11-1, Copyright (c) 2000-2014 the Libav developers
  built on Sep 26 2014 14:36:31 with gcc 4.9.1 (Ubuntu 4.9.1-15ubuntu1)
avconv 11-6:11-1
libavutil     54.  3. 0 / 54.  3. 0
libavcodec    56.  1. 0 / 56.  1. 0
libavformat   56.  1. 0 / 56.  1. 0
libavdevice   55.  0. 0 / 55.  0. 0
libavfilter    5.  0. 0 /  5.  0. 0
libavresample  2.  1. 0 /  2.  1. 0
libswscale     3.  0. 0 /  3.  0. 0""".split("\n")
        text.append(9)
        c.check_version_txt(text)

        self.assertEqual(c.major_version, 11, "Detecting major version for Ubuntu 14.10's AVConv version")
        self.assertEqual(c.minor_version, 0, "Detecting minor version for Ubuntu 14.10's AVConv version")


    def test_ubuntu_15_04(self):
        c = devedeng.avbase.avbase()
        text = """avconv version 11.2-6:11.2-1, Copyright (c) 2000-2014 the Libav developers
  built on Jan 18 2015 05:12:33 with gcc 4.9.2 (Ubuntu 4.9.2-10ubuntu2)
avconv 11.2-6:11.2-1
libavutil     54.  3. 0 / 54.  3. 0
libavcodec    56.  1. 0 / 56.  1. 0
libavformat   56.  1. 0 / 56.  1. 0
libavdevice   55.  0. 0 / 55.  0. 0
libavfilter    5.  0. 0 /  5.  0. 0
libavresample  2.  1. 0 /  2.  1. 0
libswscale     3.  0. 0 /  3.  0. 0""".split("\n")
        text.append(9)
        c.check_version_txt(text)

        self.assertEqual(c.major_version, 11, "Detecting major version for Ubuntu 15.04's AVConv version")
        self.assertEqual(c.minor_version, 2, "Detecting minor version for Ubuntu 15.04's AVConv version")


    def test_mkv1(self):


        c = devedeng.avprobe.avprobe()
        json_test = """{
    "streams": [
        {
            "index": 0,
            "codec_name": "aac",
            "codec_long_name": "AAC (Advanced Audio Coding)",
            "profile": "LC",
            "codec_type": "audio",
            "codec_time_base": "1/44100",
            "codec_tag_string": "mp4a",
            "codec_tag": "0x6134706d",
            "sample_fmt": "fltp",
            "sample_rate": "44100",
            "channels": 2,
            "channel_layout": "stereo",
            "bits_per_sample": 0,
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/44100",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 3771392,
            "duration": "85.519093",
            "bit_rate": "115596",
            "nb_frames": "3683",
            "disposition": {
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0
            },
            "tags": {
                "creation_time": "2005-12-20 20:20:15",
                "language": "eng",
                "handler_name": "Apple Sound Media Handler"
            }
        },
        {
            "index": 1,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "profile": "Constrained Baseline",
            "codec_type": "video",
            "codec_time_base": "1/2000",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "width": 320,
            "height": 240,
            "has_b_frames": 0,
            "sample_aspect_ratio": "0:1",
            "display_aspect_ratio": "0:1",
            "pix_fmt": "yuv420p",
            "level": 13,
            "color_range": "tv",
            "color_space": "smpte170m",
            "color_transfer": "bt709",
            "color_primaries": "smpte170m",
            "chroma_location": "topleft",
            "is_avc": "1",
            "nal_length_size": "4",
            "r_frame_rate": "10/1",
            "avg_frame_rate": "10/1",
            "time_base": "1/1000",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 85500,
            "duration": "85.500000",
            "bit_rate": "90795",
            "bits_per_raw_sample": "8",
            "nb_frames": "855",
            "disposition": {
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0
            },
            "tags": {
                "creation_time": "2005-12-20 20:20:15",
                "language": "eng",
                "handler_name": "Apple Video Media Handler"
            }
        }
    ]
}"""
        retval = c.process_json(json_test,"filename.mkv")
        self.assertFalse(retval)
        self.assertEqual(c.audio_streams, 1, "Checking number of audio streams")
        self.assertEqual(c.audio_list[0], 0, "Checking audio stream 1")
        self.assertEqual(c.video_streams, 1, "Checking number of video streams")
        self.assertEqual(c.video_list[0], 1, "Checking video stream 1")

if __name__ == '__main__':
    unittest.main()