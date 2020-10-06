from loguru import logger
import re
import json

def get_contacts_dict(contacts_file):
    contacts_dict = {}
    logger.info('starting')
    with open (f'{contacts_file}', 'r', encoding='utf-8') as contacts_file:
        logger.info(f'file {contacts_file} was opened')
        for contact in contacts_file:
            contact_nickname = contact.split('-')[0]
            contact_name_encoded = contact.split('>')[-1]
            try:
                contact_name_decoded = contact_name_encoded.encode('cp1252', 
                        errors='replace').decode('utf8', 
                        errors='replace').replace('\n', '')
                contacts_dict.update({contact_nickname: {
                                                            'name': contact_name_decoded,
                                                            'conversations': {}
                                                        }})    
            except UnicodeEncodeError:
                logger.error(f'problem with decoding in {contact_name_encoded}')
                continue
    logger.info(f'file {contacts_file} was read')
    logger.info('contacts_dict was created')
    return contacts_dict


def get_conversations(conversations_file, contacts_dict):
    with open (f'{conversations_file}', 'r', encoding='utf-8') as conversations_file:
        logger.info(f'file {conversations_file} was opened')
        logger.info('setting up...')
        for message in conversations_file:
            nicknames = message.split(':')[0].split('->')
            sender = nicknames[0]
            recipient = nicknames[1]
            sender_info = contacts_dict[sender]['conversations']
            try:
                sender_info.update({recipient: sender_info[recipient] + 1}) 
            except KeyError:
                sender_info.update({recipient: 0}) 
    get_result(contacts_dict)
    logger.info('done !')
    return contacts_dict


def get_result(result):
    print(json.dumps(result, indent=4, ensure_ascii=False))


with open ('catched.json', 'w', encoding='utf-8') as catched:
    json.dump(get_conversations('encrypted.txt', 
                                get_contacts_dict('mapping.txt')), 
                                catched,
                                ensure_ascii=False)
