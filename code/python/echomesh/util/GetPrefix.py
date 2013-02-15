from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Join

def get_prefix(table, name, allow_prefixes=True):
  result = table.get(name)
  if result:
    return result

  if allow_prefixes:
    results = [(k, v) for (k, v) in table.iteritems() if k.startswith(name)]
    if len(results) is 1:
      return results[0][1]
    elif len(results) > 1:
      words = sorted(x[0] for x in results)
      cmds = Join.join_words(*words)
      raise Exception('"%s" matches multiple commands: %s.' % (name, cmds))

  raise Exception('"%s" is not a valid command.' % name)