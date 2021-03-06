import subprocess
import shlex
import argparse
import os
import tarfile
import shutil
import time

class pluginInstaller:
    installLogPath = "/home/cyberpanel/modSecInstallLog"
    tempRulesFile = "/home/cyberpanel/tempModSecRules"
    mirrorPath = "cyberpanel.net"

    @staticmethod
    def stdOut(message):
        print("\n\n")
        print ("[" + time.strftime(
            "%I-%M-%S-%a-%b-%Y") + "] #########################################################################\n")
        print("[" + time.strftime("%I-%M-%S-%a-%b-%Y") + "] " + message + "\n")
        print ("[" + time.strftime(
            "%I-%M-%S-%a-%b-%Y") + "] #########################################################################\n")

    ### Functions Related to plugin installation.

    @staticmethod
    def extractPlugin(pluginName):
        pathToPlugin = pluginName + '.zip'
        command = 'unzip ' + pathToPlugin + ' -d /usr/local/CyberCP'
        subprocess.call(shlex.split(command))

    @staticmethod
    def upgradingSettingsFile(pluginName):
        data = open("/usr/local/CyberCP/CyberCP/settings.py", 'r').readlines()
        writeToFile = open("/usr/local/CyberCP/CyberCP/settings.py", 'w')

        for items in data:
            if items.find("'emailPremium',") > -1:
                writeToFile.writelines(items)
                writeToFile.writelines("    '" + pluginName + "',\n")
            else:
                writeToFile.writelines(items)

        writeToFile.close()

    @staticmethod
    def upgradingURLs(pluginName):
        data = open("/usr/local/CyberCP/CyberCP/urls.py", 'r').readlines()
        writeToFile = open("/usr/local/CyberCP/CyberCP/urls.py", 'w')
        print('hello world')

        for items in data:
            if items.find("manageservices") > -1:
                writeToFile.writelines(items)
                writeToFile.writelines("    url(r'^" + pluginName + "/',include('" + pluginName + ".urls')),\n")
                print('hello world')
            else:
                writeToFile.writelines(items)

        writeToFile.close()

    @staticmethod
    def informCyberPanel(pluginName):
        pluginPath = '/home/cyberpanel/plugins'

        if not os.path.exists(pluginPath):
            os.mkdir(pluginPath)

        pluginFile = pluginPath + '/' + pluginName
        command = 'touch ' + pluginFile
        subprocess.call(shlex.split(command))

    @staticmethod
    def addInterfaceLink(pluginName):
        data = open("/usr/local/CyberCP/baseTemplate/templates/baseTemplate/index.html", 'r').readlines()
        writeToFile = open("/usr/local/CyberCP/baseTemplate/templates/baseTemplate/index.html", 'w')

        pluginCheck = 0

        for items in data:
            if items.find('<span>{% trans "Plugins" %}</span>') > -1:
                pluginCheck = 1
            elif pluginCheck == 1 and items.find('<ul>'):
                writeToFile.writelines(items)
                writeToFile.writelines('<li><a href="{% url \'' + pluginName + '\' %}" title="{% trans \'' + pluginName + '\' %}"><span>{% trans "' + pluginName + '" %}</span></a></li>')
                pluginCheck = 0
            else:
                writeToFile.writelines(items)

        writeToFile.close()

    @staticmethod
    def installPlugin(pluginName):
        try:
            ##

            pluginInstaller.stdOut('Extracting plugin.')
            pluginInstaller.extractPlugin(pluginName)
            pluginInstaller.stdOut('Plugin extracted.')

            ##

            pluginInstaller.stdOut('Restoring settings file.')
            pluginInstaller.upgradingSettingsFile(pluginName)
            pluginInstaller.stdOut('Settings file restored.')

            ###

            pluginInstaller.stdOut('Upgrading URLs')
            pluginInstaller.upgradingURLs(pluginName)
            pluginInstaller.stdOut('URLs upgraded.')

            ##

            pluginInstaller.stdOut('Informing CyberPanel about plugin.')
            pluginInstaller.informCyberPanel(pluginName)
            pluginInstaller.stdOut('CyberPanel core informed about the plugin.')

            ##

            ##

            pluginInstaller.stdOut('Adding interface link..')
            pluginInstaller.addInterfaceLink(pluginName)
            pluginInstaller.stdOut('Interface link added.')

            ##

            pluginInstaller.restartGunicorn()

            pluginInstaller.stdOut('Plugin successfully installed.')

        except BaseException, msg:
            pluginInstaller.stdOut(str(msg))

    ### Functions Related to plugin installation.

    @staticmethod
    def removeFiles(pluginName):
        pluginPath = '/usr/local/CyberCP/' + pluginName
        if os.path.exists(pluginPath):
            shutil.rmtree(pluginPath)

    @staticmethod
    def removeFromSettings(pluginName):
        data = open("/usr/local/CyberCP/CyberCP/settings.py", 'r').readlines()
        writeToFile = open("/usr/local/CyberCP/CyberCP/settings.py", 'w')

        for items in data:
            if items.find(pluginName) > -1:
                continue
            else:
                writeToFile.writelines(items)
        writeToFile.close()

    @staticmethod
    def removeFromURLs(pluginName):
        data = open("/usr/local/CyberCP/CyberCP/urls.py", 'r').readlines()
        writeToFile = open("/usr/local/CyberCP/CyberCP/urls.py", 'w')

        for items in data:
            if items.find(pluginName) > -1:
                continue
            else:
                writeToFile.writelines(items)

        writeToFile.close()

    @staticmethod
    def informCyberPanelRemoval(pluginName):
        pluginPath = '/home/cyberpanel/plugins'
        pluginFile = pluginPath + '/' + pluginName
        if os.path.exists(pluginFile):
            os.remove(pluginFile)

    @staticmethod
    def removeInterfaceLink(pluginName):
        data = open("/usr/local/CyberCP/baseTemplate/templates/baseTemplate/index.html", 'r').readlines()
        writeToFile = open("/usr/local/CyberCP/baseTemplate/templates/baseTemplate/index.html", 'w')

        for items in data:
            if items.find(pluginName) > -1 and items.find('<li>') > -1:
                continue
            else:
                writeToFile.writelines(items)
        writeToFile.close()

    @staticmethod
    def removePlugin(pluginName):
        try:
            ##

            pluginInstaller.stdOut('Removing files..')
            pluginInstaller.removeFiles(pluginName)
            pluginInstaller.stdOut('Files removed..')

            ##

            pluginInstaller.stdOut('Restoring settings file.')
            pluginInstaller.removeFromSettings(pluginName)
            pluginInstaller.stdOut('Settings file restored.')

            ###

            pluginInstaller.stdOut('Upgrading URLs')
            pluginInstaller.removeFromURLs(pluginName)
            pluginInstaller.stdOut('URLs upgraded.')

            ##

            pluginInstaller.stdOut('Informing CyberPanel about plugin removal.')
            pluginInstaller.informCyberPanelRemoval(pluginName)
            pluginInstaller.stdOut('CyberPanel core informed about the plugin removal.')

            ##

            pluginInstaller.stdOut('Remove interface link..')
            pluginInstaller.removeInterfaceLink(pluginName)
            pluginInstaller.stdOut('Interface link removed.')

            ##

            pluginInstaller.restartGunicorn()

            pluginInstaller.stdOut('Plugin successfully removed.')

        except BaseException, msg:
            pluginInstaller.stdOut(str(msg))

    ####

    @staticmethod
    def restartGunicorn():
        command = 'systemctl restart gunicorn.socket'
        subprocess.call(shlex.split(command))



def main():

    parser = argparse.ArgumentParser(description='CyberPanel Installer')
    parser.add_argument('function', help='Specify a function to call!')

    parser.add_argument('--pluginName', help='Temporary path to configurations data!')


    args = parser.parse_args()
    if args.function == 'install':
        pluginInstaller.installPlugin(args.pluginName)
    else:
        pluginInstaller.removePlugin(args.pluginName)

if __name__ == "__main__":
    main()