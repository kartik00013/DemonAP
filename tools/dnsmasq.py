#!/usr/bin/env python
# -*- coding: utf-8 -*

from .dependency import Dependency
import subprocess


class Dnsmasq(Dependency):
	dependency_required = True
	dependency_name = 'dnsmasq'
	dependency_url = 'apt-get install dnsmasq'

	def start_dhcp_dns():
		from util.process import Process

		subprocess.call(['dnsmasq', '-C', 'configs/dnsmasq.conf', '-d'])
