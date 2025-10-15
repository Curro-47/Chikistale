from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

def loadfont(fontpath, private=True, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.

    `private`     if True, other processes cannot see this font, and this
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts

    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

    '''
    # This function was taken from
    # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
    # This function is written for Python 2.x. For 3.x, you
    # have to convert the isinstance checks to bytes and str
    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    else:
        raise TypeError('fontpath must be of type byteStr (bytes) for example:  b\"hello\"')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)


def char(chr):
    pos = [0, 0]
    if type(chr) == int and chr >= 0 and chr < 10:
        basePos0 = [-0.14,-13.71]
        basePos1 = [-1.1,-13.71]
        basePos2 = [-2,-13.71]
        difference = 1.096

        if chr == 0: pos = basePos0
        elif chr == 1: pos = basePos1
        elif chr >= 2: pos = [basePos2[0] - (chr-2)*difference, basePos2[1]]
    
    return pos