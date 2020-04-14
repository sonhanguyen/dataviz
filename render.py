#!/usr/bin/env python

import subprocess

run = lambda cmd: subprocess.run(cmd, check=True, shell=True)

from os import environ
DOCS = environ['DOCS']
REQUIREMENTS = '{dir}/{name}'\
  .format(dir=DOCS, name=environ['REQUIREMENTS'])

run(
  '[ -f {name} ] && pip install -r {name} || exit 0'\
    .format(name=REQUIREMENTS)
  # install python dependencies that are required for the notebooks
)

from functools import partial, reduce

fold = partial(reduce, lambda v, f: f(v))
pipe = lambda *args: fold(args)
select =  lambda f: partial(map, f)
where =  lambda f: partial(filter, f)
doc_name: lambda ext: lambda name: name[0: -len(ext)]
ends_with = lambda ext: where(lambda file: file.lower().endswith(ext))

MD = '.md'
RMD = '.rmd'

from glob import glob
all = glob('{0}/**md'.format(DOCS))

# skip file that are already rendered
skip = pipe(
  all,
  ends_with(MD),
  select(doc_name(MD)),
  set
)

from os import path

pipe(
  all,
  ends_with(RMD),
  where(lambda name: not doc_name(RMD)(name) in skip),
  select(lambda file: {
    'dir': path.dirname(file),
    'name': path.basename(file)
  }),
  select(lambda file: run(
    'cd {dir} && R -e \'rmarkdown::render("{name}", run_pandoc=FALSE)\''\
    # it's important that render() is called in the same directory as the notebook
    # so that knitr cache is created inside that, which is persisted via docker volume
      .format(**file)
  )),
  list # force strict iteration on lazy list
)
