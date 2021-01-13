'''
Utility functions used in training and pre-processing stage.
'''
def dictkey_chg(dictionary, key_pair):
    '''
    Change dictionary key from old to new according to key_pair

    Parameters
    ----------
    dictionary : Dictionary
        dictionary to modify

    key_pair : Dictionary
        key pair with old (key) and new (value)

    Return
    ----------
    Modified dictionary
    '''
    for old_key in list(key_pair.keys()):
        dictionary[key_pair[old_key]] = dictionary.pop(old_key)
    return dictionary
