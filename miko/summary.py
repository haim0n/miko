import logging


class Summary(object):
    """Summary class to summarize project findings."""

    def __init__(self, projects_counter, projects):

        self.projects_counter = projects_counter
        self.projects_using_lib = [project.name for project in projects
                                   if project.found_library]
        self.projects_not_using_lib = [project.name for project in projects
                                       if not project.found_library]

    def print_summary(self):
        """Print summary of cleanedup resources."""

        logging.info("============ Summary ============"
                     "\n\t\tScanned {} projects."
                     .format(self.projects_counter))

        logging.debug("\n\nProjects not using the library:\n\n{}"
                      .format("\n".join(self.projects_not_using_lib)))

        logging.info("\n\nProjects using the library:\n\n{}"
                     .format("\n".join(self.projects_using_lib)))
