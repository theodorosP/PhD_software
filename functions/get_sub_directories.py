#get a list of all suddirectories in a directory
def get_sub_dir(path_of_dir):
    import os
    rootdir = path_of_dir
    list_sub_dir = list()
    for i in os.listdir(rootdir):
        d = os.path.join(rootdir, i)
        if os.path.isdir(d):
            list_sub_dir.append(d)
    return list_sub_dir
