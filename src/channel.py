from data import data, user_with_token, user_with_id, channel_with_id
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    # Retrieve data
    authorised_user = user_with_token(token)
    channel = channel_with_id(channel_id)
    invited_user = user_with_id(u_id)
    
    # Error check
    if channel is None:
        raise InputError
    elif authorised_user is None:
        raise AccessError
    elif invited_user is None:
        raise InputError
    elif authorised_user['id'] not in channel['all_members']:
        raise AccessError
    
    # Append invited user to all_members
    for channel in data['channels']:
        if channel['id'] == channel_id and invited_user['id'] not in channel['all_members']:
            channel['all_members'].append(invited_user['id'])
    
    return {
    }

def channel_details(token, channel_id):
    # Retrieve data
    authorised_user = user_with_token(token)
    channel = channel_with_id(channel_id)
    
    # Error check
    if channel is None:
        raise InputError
    elif authorised_user is None:
        raise AccessError
    elif authorised_user['id'] not in channel['all_members']:
        raise AccessError

    return {
        'name': channel['name'],
        'owner_members': [
            {
                'u_id': owner_id,
                'name_first': user_with_id(owner_id)['name_first'],
                'name_last': user_with_id(owner_id)['name_last'],
            }
            for owner_id in channel['owner_members']
        ],
        'all_members': [
            {
                'u_id': member_id,
                'name_first': user_with_id(member_id)['name_first'],
                'name_last': user_with_id(member_id)['name_last'],
            }
            for member_id in channel['all_members']
        ],
    }

def channel_messages(token, channel_id, start):
    # Retrieve data
    authorised_user = user_with_token(token)
    channel = channel_with_id(channel_id)
    
    # Error check
    if channel is None:
        raise InputError
    elif start >= len(channel['messages']):
        raise InputError
    elif authorised_user is None:
        raise AccessError
    elif authorised_user['id'] not in channel['all_members']:
        raise AccessError
    
    # Messages originally ordered chronologically
    messages = list(reversed(channel['messages']))[start : start + 50 + 1]
    # The end is reached if the first message (message index 0) is included in messages
    end = -1 if any(message['m_id'] == 0 for message in messages) else start + 50

    return {
        'messages': messages,
        'start': start,
        'end': end,
    }

def channel_leave(token, channel_id):
    # Retrieve data
    authorised_user = user_with_token(token)
    channel = channel_with_id(channel_id)

    # Error check
    if channel is None:
        raise InputError
    elif authorised_user is None:
        raise AccessError
    elif authorised_user['id'] not in channel['all_members']:
        raise AccessError

    # Remove user from all_members
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel['all_members'].remove(authorised_user['id'])
    
    # Attempt to remove user from owner_members 
    if authorised_user['id'] in channel['owner_members']:
        # Remove if user is also an owner
        for channel in data['channels']:
            if channel['id'] == channel_id:
                channel['owner_members'].remove(authorised_user['id'])
    
    return {
    }

def channel_join(token, channel_id):
    # Retrieve data
    channel = channel_with_id(channel_id)
    authorised_user = user_with_token(token)

    # Error check
    if channel is None:
        raise InputError
    elif authorised_user is None:
        raise AccessError
    elif not channel['is_public']:
        raise AccessError

    # Adds user to channel
    for channel in data['channels']:
        # Check that user not already in channel (don't want to add duplicate users to list)
        if channel['id'] == channel_id and authorised_user['id'] not in channel['all_members']:
            channel['all_members'].append(authorised_user['id'])
    
    return {
    }

def channel_addowner(token, channel_id, u_id):
    # Retrieve data
    authorised_user = user_with_token(token)    
    channel = channel_with_id(channel_id)
    new_owner = user_with_id(u_id)

    # Error check
    if channel is None:
        raise InputError
    elif authorised_user is None:
        raise AccessError
    elif new_owner is None:
        raise AccessError
    elif authorised_user['id'] not in channel['owner_members']:
        raise AccessError
    elif new_owner['id'] in channel['owner_members']:
        raise InputError

    # Add user as owner
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel['owner_members'].append(new_owner['id'])

    return {
    }

def channel_removeowner(token, channel_id, u_id):
    # Retrieve data
    authorised_user = user_with_token(token)
    channel = channel_with_id(channel_id)
    old_owner = user_with_id(u_id)

    # Error check
    if channel is None:
        raise InputError
    elif authorised_user is None:
        raise AccessError
    elif old_owner is None:
        raise AccessError    
    elif authorised_user['id'] not in channel['owner_members']:
        raise AccessError
    elif old_owner['id'] not in channel['owner_members']:
        raise InputError

    # Remove owner
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel['owner_members'].remove(old_owner['id'])

    return {
    }