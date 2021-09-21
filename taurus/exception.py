class UserInputError(RuntimeError):
    pass


class NoAddressesEntered(UserInputError):
    pass


class InvalidAddressEntered(UserInputError):
    pass
