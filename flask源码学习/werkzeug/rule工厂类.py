"""
结果实验可以得出结论？：只能管括号外部的，在括号内的不可以被忽略
"""

import re

_rule_re = re.compile(
    r"""
    (?P<static>[^<]*)                           # static rule data
    <
    (?:
        (?P<converter>[a-zA-Z_][a-zA-Z0-9_]*)   # converter name
        (?:\((?P<args>.*?)\))?                  # converter arguments
        \:                                      # variable delimiter
    )?
    (?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)        # variable name
    >
    """,
    re.VERBOSE,
)
"""
这里的正则表达式中？：这个表达的不捕获其中内容，只匹配。
可是下面的groupdict中很明显包含其中的内容
"""
def parse_rule(rule):
    """Parse a rule and return it as generator. Each iteration yields tuples
    in the form ``(converter, arguments, variable)``. If the converter is
    `None` it's a static url part, otherwise it's a dynamic one.

    :internal:
    """
    pos = 0
    end = len(rule)
    do_match = _rule_re.match
    used_names = set()
    while pos < end:
        m = do_match(rule, pos)
        if m is None:
            break
        data = m.groupdict()
        if data["static"]:
            yield None, None, data["static"]
        variable = data["variable"]
        converter = data["converter"] or "default"
        if variable in used_names:
            raise ValueError("variable name %r used twice." % variable)
        used_names.add(variable)
        yield converter, data["args"] or None, variable
        pos = m.end()
    if pos < end:
        remaining = rule[pos:]
        if ">" in remaining or "<" in remaining:
            raise ValueError("malformed url rule: %r" % rule)
        yield None, None, remaining


# **************************** 检验 ******************************** #
"""
事实证明？：的忽略作用在这似乎不起效
"""
pa = r"""(?:(?P<arg>[0-9]{9}))"""
s = '123456789:123456789'
res = re.compile(pa).match(s).group(1)
print(res)

print('#' + '*'*7)
"""
下面这种忽略了
"""
pa = r'(?:\d)([a-z])'
s = '3a'
res = re.compile(pa).match(s).group(1)
print(res) # a
"""
下面这种没有被忽略
"""
pa = r'(?:(\d))([a-z])'
s = '3a'
res = re.compile(pa).match(s).group(1)
print(res) # 3
"""
下面这种z被忽略
"""
pa = r'(?:(\d)[a-z])([a-z])'
s = '3za'
res = re.compile(pa).match(s).group(2)
print(res) # a