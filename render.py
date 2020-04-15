#!/usr/bin/env python

from functools import partial, reduce

fold = partial(reduce, lambda v, f: f(v))
pipe = lambda *args: fold(args)
select =  lambda f: partial(map, f)
where =  lambda f: partial(filter, f)
doc_name = lambda ext: lambda name: name[0: -len(ext)]
ends_with = lambda ext: where(lambda file: file.lower().endswith(ext))

RENDERED = '_rmd.md'
RMD = '.rmd'

from glob import glob
from os import environ
all = glob('{0}/**md'.format(environ['DOCS']))

# skip file that are already rendered
skip = pipe(
  all,
  ends_with(RENDERED),
  select(doc_name(RENDERED)),
  set
)

from os import path
import subprocess
run = lambda cmd: subprocess.run(cmd, check=True, shell=True)

import warnings
[ warnings.warn(
    '\n{0} is already rendered, skipping..\n'.format(name) +
    'Please delete output and try aaign if you wish to re-render it\n'
  ) for name in skip
]

to_render = pipe(
  all,
  ends_with(RMD),
  where(lambda name: not (doc_name(RMD)(name) in skip)),
  select(lambda file: {
    'dir': path.dirname(file),
    'name': path.basename(file),
    'out': path.basename(file).replace('.', '_')
  }),
  list
)

[ run(('cd {dir} && R -e \'rmarkdown::render("{name}", ' +
    'output_format = rmarkdown::github_document(), ' +
    'output_file = "{out}")\'').format(**file))
  # it's important that render() is called in the same directory as the notebook
  # so that knitr cache is created inside that, which is persisted via docker volume
  for file in to_render
]