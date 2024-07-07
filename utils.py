def get_channel_name(text):
    index = text.find('?')  
    if index != -1:
        return text[index+1:]  
    else:
        return None 