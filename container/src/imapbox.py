#!/usr/bin/python3
#-*- coding:utf-8 -*-

from mailboxresource import save_emails, get_folder_fist
import argparse
from six.moves import configparser
import os
import getpass


def load_configuration(args):
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(['./config.cfg', '/etc/imapbox/config.cfg', os.path.expanduser('~/.config/imapbox/config.cfg')])

    options = {
        'days': None,
        'local_folder': '.',
        'unsynced_folder': '/unsynced',
        'wkhtmltopdf': None,
        'accounts': []
    }

    if (config.has_section('imapbox')):
        if config.has_option('imapbox', 'days'):
            options['days'] = config.getint('imapbox', 'days')

        if config.has_option('imapbox', 'local_folder'):
            options['local_folder'] = os.path.expanduser(config.get('imapbox', 'local_folder'))

        if config.has_option('imapbox', 'unsynced_folder'):
            options['unsynced_folder'] = os.path.expanduser(config.get('imapbox', 'unsynced_folder'))

        if config.has_option('imapbox', 'wkhtmltopdf'):
            options['wkhtmltopdf'] = os.path.expanduser(config.get('imapbox', 'wkhtmltopdf'))


    for section in config.sections():

        if ('imapbox' == section):
            continue

        if (args.specific_account and (args.specific_account != section)):
            continue

        account = {
            'name': section,
            'remote_folder': 'INBOX',
            'port': 993,
            'ssl': False
        }

        account['host'] = config.get(section, 'host')
        if config.has_option(section, 'port'):
            account['port'] = config.get(section, 'port')

        account['username'] = config.get(section, 'username')
        if config.has_option(section, 'password'):
            account['password'] = config.get(section, 'password')
        else:
            prompt=('Password for ' + account['username'] + ':' + account['host'] + ': ')
            account['password'] = getpass.getpass(prompt=prompt)

        if config.has_option(section, 'ssl'):
            if config.get(section, 'ssl').lower() == "true":
                account['ssl'] = True

        if config.has_option(section, 'remote_folder'):
            account['remote_folder'] = config.get(section, 'remote_folder')

        if (None == account['host'] or None == account['username'] or None == account['password']):
            continue

        options['accounts'].append(account)

    if (args.local_folder):
        options['local_folder'] = args.local_folder

    if (args.unsynced_folder):
        options['unsynced_folder'] = args.unsynced_folder

    if (args.days):
        options['days'] = args.days

    if (args.wkhtmltopdf):
        options['wkhtmltopdf'] = args.wkhtmltopdf

    return options




def main():
    argparser = argparse.ArgumentParser(description="Dump a IMAP folder into .eml files")
    argparser.add_argument('-l', dest='local_folder', help="Local folder where to create the email folders")
    argparser.add_argument('-u', dest='unsynced_folder', help="Folder where all newly created emails are copied, so they can be synced into a search tool")
    argparser.add_argument('-d', dest='days', help="Number of days back to get in the IMAP account", type=int)
    argparser.add_argument('-w', dest='wkhtmltopdf', help="The location of the wkhtmltopdf binary")
    argparser.add_argument('-a', dest='specific_account', help="Select a specific account to backup")
    args = argparser.parse_args()
    options = load_configuration(args)

    for account in options['accounts']:

        print('{}/{} (on {})'.format(account['name'], account['remote_folder'], account['host']),"\n", flush=True)
        basedir = options['local_folder']
        baseUnsyncedDir = options['unsynced_folder']

        if account['remote_folder'] == "__ALL__":
            folders = []
            for folder_entry in get_folder_fist(account):
                folders.append(folder_entry.decode().replace("/",".").split(' "." ')[1])
            # Remove Gmail parent folder from array otherwise the script fails:
            if '"[Gmail]"' in folders: folders.remove('"[Gmail]"')
            # Remove Gmail "All Mail" folder which just duplicates emails:
            if '"[Gmail].All Mail"' in folders: folders.remove('"[Gmail].All Mail"')
        else:
            folders = str.split(account['remote_folder'], ',')
        for folder_entry in folders:
            print("Saving folder: " + folder_entry,"\n", flush=True)
            account['remote_folder'] = folder_entry
            options['local_folder'] = os.path.join(basedir, folder_entry.replace('"', ''))
            options['unsynced_folder'] = os.path.join(baseUnsyncedDir, folder_entry.replace('"', ''))
            save_emails(account, options)

if __name__ == '__main__':
    main()
