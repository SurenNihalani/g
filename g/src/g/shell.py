import os
from dataclasses import dataclass
from typing import Optional
import logging
import click
from pathlib import Path
import fnmatch


@dataclass()
class DirectoryEnvironmentVariable(object):
    key_name: str
    separator: str
    prefix: Optional[str]


PATH = DirectoryEnvironmentVariable(
    key_name='PATH',
    separator=':',
    prefix=None
)

LDFLAGS = DirectoryEnvironmentVariable(
    key_name='LDFLAGS',
    separator=' ',
    prefix='-L'
)

CPPFLAGS = DirectoryEnvironmentVariable(
    key_name='CPPFLAGS',
    separator=' ',
    prefix='-I'
)

ALL_FIXES = [
    PATH,
    LDFLAGS,
    CPPFLAGS
]

DIR_SORTING_ORDER = {
    '/bin': 0,
    '/sbin': 1,
    '/usr/bin': 2,
    '/usr/sbin': 3,
    '/usr/local/': 4,
    '/opt/homebrew/': 5,
    '/Library/': 6,
    '/Users/*/Library/': 7,
    '/Applications/': 8,
    '/Users/': 9,
}


@click.group()
@click.option('--verbose/--no-verbose', default=False)
def shell(verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


@shell.command()  # @cli, not @click!
@click.argument('environment-variable-name')
def shell_filter(environment_variable_name):
    """Shell filter that removes invalid directory names.

    input variable key like PATH, LDFLAGS and CPPFLAGS

    """
    found = False
    new_entities = []
    for a_fix in ALL_FIXES:
        if a_fix.key_name != environment_variable_name:
            continue
        found = True
        current_value = os.environ.get(environment_variable_name, '')
        entities = [entity.removeprefix(a_fix.prefix) for entity in current_value.split(sep=a_fix.separator)]
        for directory in entities:
            path_here = Path(directory)
            if not path_here.exists():
                logger.debug(f'Dropping {path_here} from {environment_variable_name} because it doesnt exist.')
                continue
            new_entities.append(directory)
        def directory_to_priority(directory_name):
            all_priorities = [max(DIR_SORTING_ORDER.values()) + 1]
            for glob_pattern, priority in DIR_SORTING_ORDER.items():
                if not fnmatch.fnmatch(directory_name, glob_pattern + '*'):
                    continue
                all_priorities.append(priority)
            return (min(all_priorities), directory_name.count('/'), len(directory_name))
        new_entities = sorted(list(set(new_entities)), key=directory_to_priority)
        new_value = a_fix.separator.join(map(lambda x: a_fix.prefix + x, new_entities))
        print(new_value)
        return
    if not found:
        logger.info(f'We dont work on {environment_variable_name}')
        raise Exception()
