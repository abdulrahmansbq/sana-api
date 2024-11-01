class DownloadingException(Exception):
    """
    Exception raised for errors that occur in downloading service class
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'