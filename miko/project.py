class Project(object):
    """An Project object is a collection of information

    about the OpenStack project.
    """

    def __init__(self, name, requirements_urls, found_library=False):

        self.name = name
        self.requirement_urls = requirements_urls
        self.found_library = found_library
