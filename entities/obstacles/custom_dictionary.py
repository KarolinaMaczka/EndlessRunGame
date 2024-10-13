class CustomDictionary(dict):
    """
    The purpose of this class is to transform a list of variables describing objects state
    into a string
    given key is an iterable and is supposed to uniquely identify object's state
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        transformed_key = self.__transform_key(key)
        if transformed_key not in self:
            super().__setitem__(transformed_key, value)

    def __getitem__(self, key):
        transformed_key = self.__transform_key(key)
        return super().__getitem__(transformed_key)

    def __delitem__(self, key):
        transformed_key = self.__transform_key(key)
        super().__delitem__(transformed_key)

    @staticmethod
    def __transform_key(obstacle_type) -> str:
        return "_".join(f"{key}_{value}" for key, value in sorted(obstacle_type.items()) if key not in ["y_position", "difficulty"])
