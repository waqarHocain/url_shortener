class ShortenUrl:
    """
    Conversion between natural number (IDs) and short strings
    """

    _alphabet = \
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    _base = len(_alphabet)

    def encode(self, num):
        string = ""
        while num > 0:
            string = self._alphabet[num % self._base] + string
            num //= self._base

        return string

    def decode(self, string):
        num = 0
        for char in string:
            num = num * self._base + self._alphabet.index(char)
        return num
