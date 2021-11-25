#!/usr/bin/env python
# -*- coding: utf-8 -*

from .dependency import Dependency
import subprocess

class Hostapd(Dependency):
	dependency_required = True
	dependency_name = 'hostapd'
	dependency_url = 'apt-get install hostapd'
	
	@classmethod
	def start_ap(cls):
		from util.process import Process
		from .airmon import Airmon

		Airmon.terminate_conflicting_processes()
		subprocess.call(['hostapd', 'configs/hostapd.conf'])
