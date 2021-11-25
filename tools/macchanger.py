#!/usr/bin/env python
# -*- coding: utf-8 -*

from .dependency import Dependency
from .ifconfig import Ifconfig
from util.color import Color

class Macchanger(Dependency):
    dependency_required = True
    dependency_name = 'macchanger'
    dependency_url = 'apt-get install macchanger'

    is_changed = False

    @classmethod
    def down_macch_up(cls, iface, options):
        '''Put interface down, run macchanger with options, put interface up'''
        from util.process import Process

        Color.clear_entire_line()
        Color.p('\r{+} {C}macchanger{W}: taking interface {C}%s{W} down...' % iface)

        Ifconfig.down(iface)

        Color.clear_entire_line()
        Color.p('\r{+} {C}macchanger{W}: changing mac address of interface {C}%s{W}...' % iface)

        command = ['macchanger']
        command.extend(options)
        command.append(iface)
        macch = Process(command)
        macch.wait()
        if macch.poll() != 0:
            Color.pl('\n{!} {R}macchanger{O}: error running {R}%s{O}' % ' '.join(command))
            Color.pl('{!} {R}output: {O}%s, %s{W}' % (macch.stdout(), macch.stderr()))
            return False

        Color.clear_entire_line()
        Color.p('\r{+} {C}macchanger{W}: bringing interface {C}%s{W} up...' % iface)

        Ifconfig.up(iface)

        return True


    @classmethod
    def reset(cls, iface):
        Color.pl('\r{+} {C}macchanger{W}: resetting mac address on %s...' % iface)
        # -p to reset to permanent MAC address
        if cls.down_macch_up(iface, ['-p']):
            new_mac = Ifconfig.get_mac(iface)

            Color.clear_entire_line()
            Color.pl('\r{+} {C}macchanger{W}: reset mac address back to {C}%s{W} on {C}%s{W}' % (new_mac, iface))


    @classmethod
    def random(cls, iface):
        from util.process import Process
        if not Process.exists('macchanger'):
            Color.pl('{!} {R}macchanger: {O}not installed')
            return

        Color.pl('\n{+} {C}macchanger{W}: changing mac address on {C}%s{W}' % iface)

        # -r to use random MAC address
        # -e to keep vendor bytes the same
        if cls.down_macch_up(iface, ['-r']):
            cls.is_changed = True
            new_mac = Ifconfig.get_mac(iface)

            Color.clear_entire_line()
            Color.pl('\r{+} {C}macchanger{W}: changed mac address to {C}%s{W} on {C}%s{W}' % (new_mac, iface))
            Color.pl('')

    @classmethod
    def custom(cls, iface, bssid):
        from util.process import Process
        if not Process.exists('macchanger'):
            Color.pl('{!} {R}macchanger: {O}not installed')
            return

        # -m to use custom MAC address
        if cls.down_macch_up(iface, ['-m', bssid]):
            cls.is_changed = True
            new_mac = Ifconfig.get_mac(iface)

            Color.clear_entire_line()
            Color.pl('\r{+} {C}macchanger{W}: changed mac address to {C}%s{W} on {C}%s{W}' % (new_mac, iface))

    @classmethod
    def reset_if_changed(cls, iface):
        if cls.is_changed:
            cls.reset(iface)