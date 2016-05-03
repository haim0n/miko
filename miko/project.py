class Project(object):
    """An Project object is a collection of information

    about the OpenStack project.
    """

    def __init__(self, name, requirements_urls):
        self.name = name
        self.requirement_urls = requirements_urls
        self.lib_list = []
