import pytest
import key


def test_build():
     s = key.build("ciccio")
     assert(s == "27b4b5b01b0d1fcab2046369720ff75e")
