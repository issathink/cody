from src.tool import get_time_links, get_time_low

def test(filename):
    print '\n'.join(map(str, get_time_links(filename)))

def test_time(filename, time):
    print '\n'.join(map(str, get_time_low(get_time_links(filename), time)))