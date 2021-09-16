"""djLint Attempt to logically shrink html."""

import regex as re

from ..settings import Config


def _clean_line(line: str) -> str:
    """Clean up a line of html.

    * remove duplicate spaces
    * remove trailing spaces

    """
    return re.sub(r" {2,}", " ", line.strip())


def _strip_html_whitespace(html: str, config: Config) -> str:
    """Remove unnecessary whitespace from text."""
    rawcode_flat = ""
    is_block_ignored = False
    is_group_ignored = False

    for item in html.strip().splitlines():

        # start of ignored block. If we are already in an ingored block, keep true.
        is_group_ignored = is_group_ignored or bool(
            re.search(config.ignored_group_opening, item, re.IGNORECASE | re.VERBOSE)
        )

        # find ignored blocks and retain indentation, otherwise strip white space
        if re.findall(
            r"(?:%s)" % config.ignored_inline_blocks,
            item,
            flags=re.IGNORECASE | re.VERBOSE,
        ):
            tmp = _clean_line(item)

        elif (
            re.search(config.ignored_block_closing, item, re.IGNORECASE | re.VERBOSE)
            and is_group_ignored is False
        ):
            # do not format ignored lines
            tmp = _clean_line(item)
            is_block_ignored = False

        elif (
            re.search(config.ignored_block_opening, item, re.IGNORECASE | re.VERBOSE)
            and is_group_ignored is False
        ):
            # do not format ignored lines
            tmp = _clean_line(item)
            is_block_ignored = True

        elif is_group_ignored or is_block_ignored:
            tmp = item

        else:
            tmp = _clean_line(item)

        # end of ignore raw code
        if bool(
            re.search(config.ignored_group_closing, item, re.IGNORECASE | re.VERBOSE)
        ):
            is_group_ignored = False

        rawcode_flat = rawcode_flat + tmp + "\n"

    return rawcode_flat


def compress_html(html: str, config: Config) -> str:
    """Compress back tags that do not need to be expanded."""
    # put empty tags on one line
    html = _strip_html_whitespace(html, config)

    html = re.sub(
        r"(<([\w]+)[^>]*>)\s+?(<\/\2>)",
        r"\1\3",
        html,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    # put empty template tags on one line
    html = re.sub(
        r"({%-?[ ]*?("
        + re.sub(r"\s", "", config.start_template_tags)
        + r")[^}]+?-?%})\s+?(\{\%-?[ ]end[^}]*?\%\})",
        r"\1\3",
        html,
        re.MULTILINE,
    )

    # put short single line tags on one line
    # verbose doesn't seem to work with replace groups.
    slt_html = re.sub(r"\s", "", config.single_line_html_tags)

    html = re.sub(
        r"(<(%s)>)\s*([^<\n]{,80})\s*?(</(\2)>)" % slt_html,
        r"\1\3\4",
        html,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    html = re.sub(
        r"(<(%s)>)\s*?([^<\n]{,80})\s*?(</(\2)>)" % slt_html,
        r"\1\3\4",
        html,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    html = re.sub(
        r"(<(%s)[ ][^\n]{,80}>)\s*([^<\n]{,80})\s*?(</(\2)>)" % slt_html,
        r"\1\3\4",
        html,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    # cannot use verbose when replacing with var. 🤕
    html = re.sub(
        r"({%-?[ ]*?("
        + re.sub(r"\s", "", config.single_line_template_tags)
        + r")[ ]+?[^\n]{,30}%})\s*([^%\n]{,50})\s*?({%-?[ ]+?end(\2)[ ]*?%})",
        r"\1\3\4",
        html,
        re.IGNORECASE | re.MULTILINE,
    )

    return html