class EmbeddingException(Exception):
    """
    Exception raised for errors that occur in embedding service class
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'