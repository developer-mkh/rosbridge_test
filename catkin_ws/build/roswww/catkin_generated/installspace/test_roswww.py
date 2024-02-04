#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Software License Agreement (BSD License)
#
# Copyright (c) 2015, Tokyo Opensource Robotics Kyokai Association
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Tokyo Opensource Robotics Kyokai Association. nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Isaac I.Y. Saito
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

import argparse
import rospy
import rostest
import sys
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from std_msgs.msg import String

class TestClient(unittest.TestCase):

    def setUp(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--no-headless', action='store_true',
                            help='start webdriver with headless mode')
        args, unknown = parser.parse_known_args()

        self.url_base = rospy.get_param("url_roswww_testserver")

        opts = webdriver.firefox.options.Options()
        if not args.no_headless:
            opts.add_argument('-headless')
        self.browser = webdriver.Firefox(options=opts)

        self.wait = webdriver.support.ui.WebDriverWait(self.browser, 10)
        # maximize screen
        self.browser.find_element_by_tag_name("html").send_keys(Keys.F11)

        #
        self.msg_received = 0
        self.msg = None
        self.sub = rospy.Subscriber('/chatter', String, self.cb)
        self.pub = rospy.Publisher('/chatter', String, queue_size=1)

    def cb(self, msg):
        rospy.logwarn("Received {}".format(msg))
        self.msg = msg
        self.msg_received = self.msg_received + 1

    def tearDown(self):
        try:
            self.browser.close()
            self.browser.quit()
        except:
            pass

    def _check_index(self, url):
        rospy.logwarn("Accessing to %s" % url)

        self.browser.get(url)
        self.wait.until(EC.presence_of_element_located((By.ID, "title")))

        title = self.browser.find_element_by_id("title")
        self.assertIsNotNone(title, "Object id=title not found")

        # check load other resouces
        self.wait.until(EC.presence_of_element_located((By.ID, "relative-link-check")))
        check = self.browser.find_element_by_id("relative-link-check")
        self.assertIsNotNone(check, "Object id=relative-link-check not found")
        self.assertEqual(check.text, "Relative link is loaded",
                         "Loading 'css/index.css' from 'index.html' failed")

    def test_index_served(self):
        url = '%s/roswww/' % (self.url_base)
        self._check_index(url)

    def test_index_redirected(self):
        url = '%s/roswww' % (self.url_base)
        self._check_index(url)

    def test_talker(self):
        url = '%s/roswww/talker.html' % (self.url_base)
        rospy.logwarn("Accessing to %s" % url)
        self.browser.get(url)

        # clock button to publish /chatter
        self.wait.until(EC.presence_of_element_located((By.ID, "button")))
        button = self.browser.find_element_by_id("button")
        self.assertIsNotNone(button, "Object id=button not found")

        while not rospy.is_shutdown() and self.msg_received < 5:
            rospy.logwarn('Wait for /chatter message')
            rospy.sleep(1)
            button.click()

    def test_listener(self):
        url = '%s/roswww/listener.html' % (self.url_base)
        rospy.logwarn("Accessing to %s" % url)
        self.browser.get(url)

        # clock button to publish /chatter
        self.wait.until(EC.presence_of_element_located((By.ID, "textArea")))
        text_area = self.browser.find_element_by_id("textArea")
        self.assertIsNotNone(text_area, "Object id=textArea not found")

        text_received = 0
        text = ""
        while not rospy.is_shutdown() and text_received < 5:
            self.pub.publish("Hello World {}".format(rospy.get_time()))
            rospy.logwarn('Wait for /chatter message')
            rospy.sleep(1)
            if text != text_area.text:
                text = text_area.text
                text_received = text_received + 1



if __name__ == '__main__':
    rospy.init_node("test_client")
    exit(rostest.rosrun("roswww", "test_client", TestClient, sys.argv))
