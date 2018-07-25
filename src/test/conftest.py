"""
  ________       .__ ____  __.      .__
 /  _____/_____  |__|    |/ _|____  |__|
/   \  ___\__  \ |  |      < \__  \ |  |
\    \_\  \/ __ \|  |    |  \ / __ \|  |
 \______  (____  /__|____|__ (____  /__|
        \/     \/           \/    \/

Copyright 2013-2018 Gaikai Inc, a Sony Computer Entertainment company
"""


def pytest_generate_tests(metafunc):
    multi = getattr(metafunc.function, 'multi', None)
    if multi is not None:
        assert len(multi.kwargs) == 1
        for name, l in multi.kwargs.items():
            for val in l:
                metafunc.addcall(id=str(val), funcargs={name: val})
