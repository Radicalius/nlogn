import re

TOKENS = ["\\\\", "\\\\.", "@", "\n+", "#", "##", "###", "_", "__", "-", "--", "---", "\\*\\*", "[\t ]+", "[\t ]*\\*", "~", "~~", "```", "```[a-z]*", "`", "``", ">", "> ", "\\!", "\\!\\[", "\\[","\\]", "[a-zA-Z0-9 ,.!$%^&(){}=;'+:/\"]+"]

def tokenize(md):
    tokens = []
    indentation = 0
    newline = False
    while len(md) > 0:
        ahead = 1
        last_matched = ""
        while ahead < len(md):
            matched = False
            for i in TOKENS:
                match = re.match(i, md[:ahead])
                if match and match.end() == ahead:
                    matched = True
                    last_matched = i
            if not matched:
                break
            else:
                ahead += 1

        if last_matched == "[\t ]+" and newline:
            if ahead - 1 > indentation:
                last_matched = "INDENT"
                indentation = ahead-1
            elif ahead - 1 < indentation:
                last_matched = "DEDENT"
                indentation = ahead-1
            else:
                md = md[max(1,ahead-1):]
                ahead = 1
                continue
            newline = False

        elif newline and indentation > 0:
            print(last_matched)
            indentation = 0
            tokens.append(("DEDENT",""))
            newline = False

        if last_matched == "\n+":
            newline = True

        tokens.append((last_matched, md[:ahead-1]))
        md = md[max(1,ahead-1):]
        ahead = 1
    return tokens

def parse(tokens):
    text = ""
    if not tokens:
        return ""
    if tokens[0][0] == "":
        return tokens.pop(0)[1]
    if tokens[0][0] == "\\\\.":
        return str(tokens.pop(0)[1][1])
    elif tokens[0][0] == "[a-zA-Z0-9 ,.!$%^&(){}=;'+:/\"]+":
        return tokens.pop(0)[1]
    elif tokens[0][0] == "@":
        text+=parse_tag(tokens)
    elif tokens[0][0] in ["#", "##", "###"]:
        text += parse_header(tokens)
    elif tokens[0][0] == "\n+":
        text += "<br/>"*len(tokens[0][1])
        tokens.pop(0)
    elif tokens[0][0] == "[\t ]*\\*":
         text += parse_list(tokens)
    elif tokens[0][0] in ["\\*\\*", "--", "~~", "__"]:
        text += parse_style(tokens)
    elif tokens[0][0] == "> ":
        text += parse_quote(tokens)
    elif tokens[0][0] == "`":
        text += parse_inline_code(tokens)
    elif tokens[0][0] == "```[a-z]*":
        text += parse_code_block(tokens)
    elif tokens[0][0] == "\\[":
        text += parse_link(tokens)
    elif tokens[0][0] == "\\!\\[":
        text += parse_image(tokens)
    elif tokens[0][0] == "---":
        text += "<hr/>\n"
    else:
        text += tokens.pop(0)[0]
    return text

def parse_style(tokens):
    type = tokens.pop(0)[0]
    styles = {"\\*\\*": "b", "--": "i", "~~": "s", "__":"u"}
    text = "<{0}>".format(styles[type])
    while tokens and tokens[0][0] != type:
        text += parse(tokens)
    if tokens:
        tokens.pop(0)
    text += "</{0}>".format(styles[type])
    return text

def parse_inline_code(tokens):
    text = "<code>"
    tokens.pop(0)
    while tokens and tokens[0][0] != "`" and tokens[0][0] != "\n+":
        text += tokens.pop(0)[1]
    if tokens:
        tokens.pop(0)
    text += "</code>"
    return text

def parse_code_block(tokens):
    text = "<pre class='{0}'><code>".format(tokens[0][1].replace("```", ""))
    tokens.pop(0)
    while tokens and tokens[0][0] != "```[a-z]*":
        text += tokens.pop(0)[1]
    if tokens:
        tokens.pop(0)
    text += "</code></pre>"
    return text

def parse_quote(tokens):
    text = "<blockquote>"
    while tokens and tokens[0][0] == "> ":
        tokens.pop(0)
        while tokens and tokens[0][0] != "\n+":
            text += parse(tokens)
        if len(tokens) >= 2 and tokens[1][0] == "> ":
            text += parse(tokens)
        else:
            tokens.pop(0)
    text += "</blockquote>"
    return text

def parse_header(tokens):
    text = ""
    heads = {"#": "h1", "##": "h2", "###": "h3"}
    type = tokens.pop(0)[0]
    text += "<{0}>".format(heads[type])
    while tokens and tokens[0][0] != "\n+":
        text += tokens[0][1]
        tokens.pop(0)
    tokens.pop(0)
    text += "</{0}>\n".format(heads[type])
    return text

def parse_until(tokens, pred):
    text = ""
    while tokens:
        if pred(tokens[0]):
            break
        else:
            if tokens[0][0] == "\\\\.":
                text += tokens[0][1][1]
            else:
                text += tokens[0][1]
            tokens.pop(0)
    return text

def safe_pop(tokens):
    if tokens:
        tokens.pop(0)

def parse_link(tokens):
    if len(tokens) < 4:
        return "["
    i = 3
    safe_pop(tokens)
    link_text = parse_until(tokens, lambda x: x[0] == "\\]")
    safe_pop(tokens)
    href = parse_until(tokens, lambda x: ")" in x[1])
    post_text = ""
    if tokens:
        href += tokens[0][1].split(")")[0]
        post_text = tokens[0][1].split(")")[1]
    safe_pop(tokens)
    return "<a href={0}>{1}</a> {2}".format(href[1:], link_text, post_text)

def parse_image(tokens):
    if len(tokens) < 4:
        return "!["
    src = tokens[3][1][1:-1]
    desc = tokens[1][1]
    for i in range(4):
        tokens.pop(0)
    return "<br/><img src={0} desc={1} /><br/>".format(src, desc)

def parse_tag(tokens):
    tokens.pop(0)
    print(tokens[0])
    if tokens[0][0] == "[a-zA-Z0-9 ,.!$%^&(){}=;'+:/]+\"":
        return "<tag>"+tokens.pop(0)[1].strip()+"</tag>&nbsp;"
    return "@"

def parse_list(tokens):
    ret = "<ul>"
    tokens.pop(0)
    while True:
        ret += "<li>"
        while tokens and tokens[0][0] != "\n+":
            ret += parse(tokens)
        if tokens:
            tokens.pop(0)
        ret += "</li>"
        if tokens and tokens[0][0] == "[\t ]*\\*":
            tokens.pop(0)
        else:
            break
    return ret+"</ul>"


def render_html(md_file):
    md = open(md_file).read()
    html = ""
    tokens = tokenize(md)
    l = len(tokens)
    while len(tokens):
        html += parse(tokens)
        if len(tokens) == l:
            tokens.pop(0)
        else:
            l = len(tokens)
    return html
