#!/usr/bin/env python3
# -*- coding: utf-8 -*

from util.color import Color
from configs.config import Configuration
from tools.hostapd import Hostapd
from tools.dnsmasq import Dnsmasq


class Rogueap(object):
	
	@classmethod
	def ap_input(cls):
		Configuration.target_essid = 'hacked'
		Configuration.target_frequency = 'g'
		Configuration.target_channel = '7'


	@classmethod
	def start_rogueap(cls):
		cls.ap_input()
		Configuration.setup_ap()
		Hostapd.start_ap()
		Dnsmasq.start_dhcp_dns()


		