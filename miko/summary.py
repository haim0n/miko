import logging


class Summary(object):
    """Summary class to summarize project findings."""

    def __init__(self, projects, projects_using_lib):
        self.projects_using_lib = [p.name for p in projects_using_lib]
        self.projects = [p.name for p in projects]

    def print_summary(self):
        """Print summary of cleanedup resources."""

        logging.info("============ Summary ============"
                     "\n\t\tScanned {} projects."
                     .format(len(self.projects)))

        logging.info("\n\nProjects using the library:\n\n{}"
                     .format("\n".join(sorted(self.projects_using_lib))))
