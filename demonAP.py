#!/usr/bin/env python
# -*- coding: utf-8 -*

from configs.config import Configuration
from tools.dependency import Dependency
from util.color import Color
from attack.rogueap import Rogueap
#from attack.eviltwin import Eviltwin

import os
import sys


class DemonAP(object):

    def __init__(self):
        '''
        Initializes demonAP. Checks that it runs under *nix, with root permissions and ensures dependencies are installed.
        '''

        self.print_banner()

        if os.name == 'nt':
            Color.pl('{!} {R}error: {O}demonAP{R} must be run under a {O}*NIX{W}{R} like OS')
            Configuration.exit_gracefully(0)

        Color.pl('{+} {G}OS is compatible{W} - {O}checked')

        if os.getuid() != 0:
            Color.pl('{!} {R}error: {O}demonAP{R} must be run as {O}root{W}')
            Color.pl('{!} {R}re-run with {O}sudo{W}')
            Configuration.exit_gracefully(0)

        Color.pl('{+} {G}user has root privilages{W} - {O}checked')

        Dependency.run_dependency_check()
        Color.pl('{+} {G}all the required dependencies are available{W} - {O}checked{W}')
        Color.pl('')
        
        Configuration.initialize()
        Color.pl('{+} {G}initialization successful{W} - {O}checked{W}')
        


    def start(self):
        
        if  Configuration.attack_choice == 1:
            Rogueap.start_rogueap()

        elif Configuration.attack_choice == 2:
            print(Configuration.ap_interface, Configuration.mon_interface)


    def print_banner(self):
        '''Displays ASCII art of the highest caliber.'''
        banner = '''
         ____                                _    ____  
        |  _ \  ___ _ __ ___   ___  _ __    / \  |  _ \ 
        | | | |/ _ \ '_ ` _ \ / _ \| '_ \  / _ \ | |_) |
        | |_| |  __/ | | | | | (_) | | | |/ ___ \|  __/ 
        |____/ \___|_| |_| |_|\___/|_| |_/_/   \_\_| 
        
        '''
        Color.pl(banner)
        Color.pl(' {G}DemonAP {D}%s{W}' % Configuration.version)
        Color.pl(' {D}automated rogue AP/Evil Twin auditor{W}')
        Color.pl(' {D}Developer - https://github.com/kartik00013{W}')
        Color.pl('')


    def scan_and_attack(self):
        '''
        1) Scans for targets, asks user to select targets
        2) Attacks each target
        '''
        # from util.scanner import Scanner
        # from attack.all import AttackAll

        # Color.pl('')

        # # Scan
        # s = Scanner()
        # targets = s.select_targets()

        # # Attack
        # attacked_targets = AttackAll.attack_multiple(targets)

        # Color.pl('{+} Finished attacking {C}%d{W} target(s), exiting' % attacked_targets)


##############################################################


def entry_point():
    try:
        demonAP = DemonAP()
        demonAP.start()
    except Exception as e:
        Color.pexception(e)
        Color.pl('\n{!} {R}Exiting{W}\n')

    except KeyboardInterrupt:
        Color.pl('\n{!} {O}Interrupted, Shutting down...{W}')
        Configuration.exit_gracefully(0)


if __name__ == '__main__':
    entry_point()
