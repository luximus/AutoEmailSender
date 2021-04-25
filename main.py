import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
from passlib.context import CryptContext
import sys
import os
import re


os.chdir(os.path.dirname(__file__))
pwd_context = CryptContext(
    schemes=['pbkdf2_sha256', 'sha256_crypt', 'md5_crypt'],
    deprecated='auto'
)

email_validator = re.compile(
    r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
)


def update_accounts():
    with open('.accounts.txt') as fp:
        accounts = [x.split(';') for x in fp.readlines()]
    for i in range(len(accounts)):
        accounts[i] = [x.strip() for x in accounts[i]]
    return accounts


def option_select(prompt, *options):
    option = None
    while option not in range(1, len(options) + 1):
        print(prompt, *([f'({x}) {y}' for x, y in enumerate(options, start=1)]), sep='\n')
        try:
            option = int(input())
        except ValueError:
            option = None
    return option


def fetch_contacts(filename):
    contacts_list = dict()
    with open(filename, mode='r', encoding='utf-8') as fp:
        contacts = fp.read().splitlines(keepends=False)
        fp.seek(0)
        first = fp.read()
        if first == '':
            print('Contacts file is empty.')
            return

    for item in contacts:
        contacts_list[item.split(';')[0].strip()] = item.split(';')[1].strip()
    return contacts_list


def read_message(filename):
    with open(filename, mode='r', encoding='utf-8') as template:
        template_content = template.read()
        template.seek(0)
        if template_content == '':
            print('Message file is empty.')
            return

    subject = template_content.splitlines()[0].rstrip()

    return subject, '\n'.join(template_content.split('\n')[1:])


def main():
    accounts = update_accounts()
    while True:
        option = option_select('What do you want to do?',
                               'Send messages',
                               'Manage registered e-mail accounts',
                               'Exit')

        if option == 1:
            users = [x[0] for x in accounts]
            while True:
                manual_entry = True
                if len(users) != 0:
                    option = option_select('Which account do you want to use?',
                                           *users,
                                           'Other',
                                           'Back')
                    if option == len(users) + 2:
                        break
                    if option != len(users) + 1:
                        address = users[option - 1]
                        index = option - 1
                        manual_entry = False

                option = 1
                while True:
                    if manual_entry:
                        address = input('E-mail address: ')
                        if email_validator.match(address) is None:
                            print('That e-mail address is invalid.')
                            continue
                    password = getpass()
                    if option != len(users) + 1:
                        if pwd_context.verify(password, accounts[option - 1][1]):
                            break
                        else:
                            print('Incorrect password.')
                            option = option_select('Try again?',
                                                   'Yes',
                                                   'No')
                            if option == 2:
                                break
                    else:
                        break
                if option == 2:
                    continue
                with smtplib.SMTP('smtp.gmail.com', 587) as mail:
                    mail.ehlo()
                    mail.starttls()
                    try:
                        mail.login(address, password)
                    except smtplib.SMTPAuthenticationError:
                        print('Incorrect address and/or password.')
                        option = option_select('Try again?',
                                               'Yes',
                                               'No')
                        if option == 2:
                            break
                        continue

                    contacts = fetch_contacts('contacts.txt')
                    subject, template_content = read_message('message.txt')
                    if all(x is not None for x in (contacts, subject, template_content)):
                        print(contacts)
                        print(subject, template_content)

                        for contact_mail in list(contacts):
                            msg = MIMEMultipart()
                            msg_body = template_content.format(*tuple(contacts[contact_mail]), accounts[index][2])

                            msg['From'] = address
                            msg['To'] = contact_mail
                            msg['Subject'] = subject

                            msg.attach(MIMEText(msg_body, 'plain'))
                            print(msg)
                            # mail.sendmail(address, contact_mail, msg.as_string())
                            print("Sent successfully!")
        elif option == 2:
            while True:
                option = option_select('What do you want to do?',
                                       'Register an account',
                                       'Update account data',
                                       'Unregister an account',
                                       'Back')
                if option == 1:
                    name = input('Name (will be used in the e-mail\'s signature): ')

                    while True:
                        address = input('E-mail address: ')

                        if email_validator.match(address) is None:
                            print('That e-mail address is invalid.')
                            continue

                        password = getpass()
                        with smtplib.SMTP('smtp.gmail.com', 587) as mail:
                            mail.ehlo()
                            mail.starttls()
                            try:
                                mail.login(address, password)
                                with open('.accounts.txt', mode='a', encoding='utf-8') as fp:
                                    fp.write(f'{address}; {pwd_context.hash(password)}; {name}\n')
                                print('Registered account.')
                                accounts = update_accounts()
                                break
                            except smtplib.SMTPAuthenticationError:
                                print('Incorrect address and/or password.')
                                option = option_select('Try again?',
                                                       'Yes',
                                                       'No')
                                if option == 2:
                                    break
                elif option == 2:
                    users = [x[0] for x in accounts]
                    option = option_select('Which account do you want to modify?',
                                           *users,
                                           'Back')
                    if option == len(users) + 1:
                        continue

                    index = option - 1
                    while True:
                        option = option_select('Which field do you want to modify?',
                                               'E-mail address',
                                               'Password',
                                               'Name',
                                               'Back')

                        if option in (1, 2):
                            if option == 1:
                                new_address = input('New e-mail address: ')
                                new_password = getpass()
                            elif option == 2:
                                new_address = users[index]
                                new_password = getpass(prompt='New password: ')

                            with smtplib.SMTP('smtp.gmail.com', 587) as mail:
                                mail.ehlo()
                                mail.starttls()
                                try:
                                    mail.login(new_address, new_password)
                                    accounts[index][0] = new_address
                                    accounts[index][1] = pwd_context.hash(new_password)
                                    new_list = ['; '.join(x) for x in accounts]
                                    with open('.accounts.txt', mode='w') as fp:
                                        fp.writelines(new_list)
                                    accounts = update_accounts()
                                    users = [x[0] for x in accounts]
                                except smtplib.SMTPAuthenticationError:
                                    print('Incorrect address and/or password.')
                                    option = option_select('Try again?',
                                                           'Yes',
                                                           'No')
                                    if option == 2:
                                        break
                        elif option == 3:
                            accounts[index][2] = input('New name: ')
                            new_list = ['; '.join(x) for x in accounts]
                            with open('.accounts.txt', mode='w') as fp:
                                fp.writelines(new_list)
                            accounts = update_accounts()
                            users = [x[0] for x in accounts]
                        else:
                            break
                elif option == 3:
                    users = [x[0] for x in accounts]
                    while True:
                        option = option_select('Which account do you want to unregister?',
                                               *users,
                                               'Back')

                        if option == len(users) + 1:
                            break
                        index = option - 1
                        option = option_select(f'Are you sure you want to unregister {users[option - 1]}?',
                                               'Yes',
                                               'No')
                        if option == 1:
                            del accounts[index]
                            new_list = ['; '.join(x) for x in accounts]
                            with open('.accounts.txt', mode='w') as fp:
                                fp.writelines(new_list)
                            accounts = update_accounts()
                            users = [x[0] for x in accounts]
                else:
                    break
        else:
            exit(0)


if __name__ == '__main__':
    main()
