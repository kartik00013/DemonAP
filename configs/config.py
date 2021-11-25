#!/usr/bin/env python
# -*- coding: utf-8 -*

import os

from util.color import Color
from util.input import raw_input
from tools.macchanger import Macchanger


class Configuration(object):
    ''' Stores configuration variables and functions for Wifite. '''
    version = '1.0'

    initialized = False # Flag indicating config has been initialized
    temp_dir = None     # Temporary directory
    ap_interface = None
    mon_interface = None
    verbose = 0
 
    @classmethod
    def initialize(cls):
        # Sets up default initial configuration values.
        # Only initialize this class once
        if cls.initialized:
            return
        cls.initialized = True

        cls.kill_conflicting_processes = True

        cls.target_essid = None 

        cls.target_bssid = None 

        cls.target_channel = None

        cls.target_frequency = None # Scan 5Ghz channels

        cls.random_mac = True # Should generate a random Mac address while scanning or deauthing devices on a network

        cls.attack_choice = None

        cls.select_attack_mode()

        cls.get_interface()


    @classmethod
    def select_attack_mode(cls):
        Color.pl(' 1. create - random {C}Rogue AP{W} to further perform {C}MITM Attacks{W}')
        Color.pl(' 2. create - {C}Evil Twin{W} to perform {C}MITM Attacks{W} or capture the original Wi-Fi AP\'s credentials using {C}Fake Captive Portal') 
        Color.pl('')
        Color.p('{?} Select the {R}Attack{W} type({G}1{W}-{G}2{W}): ')
        cls.attack_choice = int(raw_input())


    @classmethod
    def get_interface(cls):
        if cls.ap_interface is None and cls.mon_interface is None:
            from tools.airmon import Airmon
            cls.ap_interface, cls.mon_interface = Airmon.ask(cls.attack_choice)
            

    @classmethod
    def monitor_mode(cls):
        if cls.mon_interface is not None:
            from tools.airmon import Airmon
            if cls.random_mac:
                Macchanger.random(cls.mon_interface)
            Airmon.start(cls.mon_interface)


    @classmethod
    def setup_ap(cls):
            
        with open('configs/hostapd.conf', 'r') as f:
            lines = f.readlines()
        f.close()

        lines[0] = 'interface=' + cls.ap_interface + '\n'
        lines[2] = 'ssid=' + cls.target_essid + '\n'
        lines[3] = 'hw_mode=' + cls.target_frequency + '\n'
        if cls.attack_choice == 1:
            Macchanger.random(cls.ap_interface)
            lines[4] = 'channel=' + cls.target_channel + '\n'
        elif cls.attack_choice == 2:
            Macchanger.custom(cls.ap.interface, cls.target_bssid)
            if cls.target_channel == 3:
               lines[4] = 'channel=4\n'
            else:
               lines[4] = 'channel=3\n'

        with open('configs/hostapd.conf', 'w') as f:
            f.writelines(lines)
        f.close()


    @classmethod
    def temp(cls, subfile=''):
        ''' Creates and/or returns the temporary directory '''
        if cls.temp_dir is None:
            cls.temp_dir = cls.create_temp()
        return cls.temp_dir + subfile

    @staticmethod
    def create_temp():
        ''' Creates and returns a temporary directory '''
        from tempfile import mkdtemp
        tmp = mkdtemp(prefix='wifite')
        if not tmp.endswith(os.sep):
            tmp += os.sep
        return tmp

    @classmethod
    def delete_temp(cls):
        ''' Remove temp files and folder '''
        if cls.temp_dir is None: return
        if os.path.exists(cls.temp_dir):
            for f in os.listdir(cls.temp_dir):
                os.remove(cls.temp_dir + f)
            os.rmdir(cls.temp_dir)


    @classmethod
    def exit_gracefully(cls, code=0):
        Color.pl('{+} {G}all the settings and services will be restored to their original state')
        ''' Deletes temp and exist with the given code '''
        cls.delete_temp()

        if cls.mon_interface is not None:
            Macchanger.reset_if_changed(cls.mon_interface)
        if cls.ap_interface is not None:
            Macchanger.reset_if_changed(cls.ap_interface)

        from tools.airmon import Airmon
        if cls.mon_interface is not None and Airmon.Changed_interface_mode:
            Color.pl('{!} {O}Note:{W} Leaving interface in Monitor Mode!')
            # Color.pl('{!} To disable Monitor Mode when finished: ' +
                    # '{C}airmon-ng stop %s{W}' % cls.mon_interface)

            # Stop monitor mode
            Airmon.stop(cls.mon_interface)

        if Airmon.killed_network_manager:
            Color.pl('{!} automatically restarting NetworkManager when finished')
            Airmon.start_network_manager()

        exit(code)

    @classmethod
    def dump(cls):
        ''' (Colorful) string representation of the configuration '''
        from util.color import Color

        max_len = 20
        for key in cls.__dict__.keys():
            max_len = max(max_len, len(key))

        result  = Color.s('{W}%s  Value{W}\n' % 'cls Key'.ljust(max_len))
        result += Color.s('{W}%s------------------{W}\n' % ('-' * max_len))

        for (key,val) in sorted(cls.__dict__.items()):
            if key.startswith('__') or type(val) in [classmethod, staticmethod] or val is None:
                continue
            result += Color.s('{G}%s {W} {C}%s{W}\n' % (key.ljust(max_len),val))
        return result

if __name__ == '__main__':
    Configuration.initialize(False)
    print(Configuration.dump())
