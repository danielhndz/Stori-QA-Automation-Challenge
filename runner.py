from sys import argv
import pytest
from utils import utils


def main():
    if len(argv) >= 3 and argv[1].lower() == '--browser':
        if argv[2].lower() == utils.BROWSER_FIREFOX:
            utils.current_browser = utils.BROWSER_FIREFOX
        elif argv[2].lower() == utils.BROWSER_OPERA:
            utils.current_browser = utils.BROWSER_OPERA
    if len(argv) >= 5 and argv[3].lower() == '--avd-name':
        utils.avd_name = argv[4]
    pytest.main([])


if __name__ == '__main__':
    main()
