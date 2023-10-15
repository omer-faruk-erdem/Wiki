
from django.core.files.storage import default_storage

def delete_entry(title):
    '''
    Deletes the entry that is specified by title
    '''
    file_name = f"entries/{title}.md"
    if default_storage.exists(file_name):
        default_storage.delete(file_name)
        return  f"Entry {title} is deleted. "
    else:
        return "there is no such file"


title = "Css"
print( delete_entry(title) ) 
