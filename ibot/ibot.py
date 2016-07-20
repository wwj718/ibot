# -*- coding: utf-8 -*-
# six
from distutils.log import warn as printf
import sys
def main():
    query = " ".join(sys.argv[1:])
    printf(query)

if __name__ == '__main__':
    main()
