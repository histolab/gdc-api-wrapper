# encoding: utf-8


def copyfileobj(fsrc, fdst, progressbar, length=16 * 1024):
    """copy data from file-like object fsrc to file-like object fdst"""
    while 1:
        buf = fsrc.read(length)
        progressbar.update(len(buf))
        if not buf:
            break
        fdst.write(buf)
