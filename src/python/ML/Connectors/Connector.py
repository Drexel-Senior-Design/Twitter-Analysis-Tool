class Connector:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'retrieve'):
            raise TypeError(f'{cls} does not implement retrieve().')
        if not hasattr(cls, 'train_test_split'):
            raise TypeError(f'{cls} does not implement train_test_split().')
