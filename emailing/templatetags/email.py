import textwrap

from django import template
from django.utils.html import format_html

register = template.Library()

COLOR_COCONUT_CREAM = '#fcfaed'
COLOR_WILD_TIDE = '#87e1d1'
COLOR_FUN_GREEN = '#007120'
COLOR_BLACK_OLIVE = '#253017'
COLOR_DANGER = '#f00'

MAX_WIDTH = "600px"
FONT_STYLE = "font-family:'Open Sans',sans-serif;"
WORD_BREAK_STYLE = "overflow-wrap: break-word;word-break: break-word; word-wrap: break-word;"
TABLE_DEFAULTS = "role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" \
    width=\"100%\" border=\"0\""
TEXT_COLOR_STYLE = "color: {}".format(COLOR_BLACK_OLIVE)

STATIC_CONTEXT = {
    'COLOR_BLACK_OLIVE': COLOR_BLACK_OLIVE,
    'COLOR_COCONUT_CREAM': COLOR_COCONUT_CREAM,
    'COLOR_FUN_GREEN': COLOR_FUN_GREEN,
    'COLOR_WILD_TIDE': COLOR_WILD_TIDE,
    'FONT_STYLE': FONT_STYLE,
    'MAX_WIDTH': MAX_WIDTH,
    'TABLE_DEFAULTS': TABLE_DEFAULTS,
    'TEXT_COLOR_STYLE': TEXT_COLOR_STYLE,
    'WORD_BREAK_STYLE': WORD_BREAK_STYLE,
}


@register.filter
def email_table_container(content):
    markup = """
        <table style="{FONT_STYLE}" {TABLE_DEFAULTS}>
            <tbody>
                <tr>
                    {content}
                </tr>
            </tbody>
        </table>
    """
    return format_html(markup.format(
        content=content,
        **STATIC_CONTEXT,
    ))


@register.filter
def email_divider(divider_type):
    # Solid border, separate types of content
    cell_padding = '1px 15px 5px'
    border_top = '1px solid #bbb'

    if divider_type == 'padder':
        # Dashed border, separate sections of content
        cell_padding = '0px'
        border_top = '1px dashed #ccc'

    markup = """
      <td style="{WORD_BREAK_STYLE}padding:{cell_padding};{FONT_STYLE}" align="left">
        <table height="0px" align="center" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: {border_top};-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%" {TABLE_DEFAULTS}>
          <tbody>
            <tr style="vertical-align: top">
              <td style="{WORD_BREAK_STYLE}border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
                <span>&#160;</span>
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    """  # noqa
    return email_table_container(format_html(markup.format(
        border_top=border_top,
        cell_padding=cell_padding,
        **STATIC_CONTEXT,
    )))


@register.filter
def email_body(content, block_type=None):
    background_color = COLOR_COCONUT_CREAM
    if block_type == 'post_scriptum':
        background_color = 'transparent'
    markup = """
        <div class="email-row-container" style="padding: 0px 10px;">
          <div style="Margin: 0 auto;min-width: 320px;max-width: {MAX_WIDTH};{WORD_BREAK_STYLE}background-color: {background_color};" class="email-row">
            <div style="border-collapse: collapse;display: table;width: 100%;background-color: {background_color};">
              <!--[if (mso)|(IE)]><table {TABLE_DEFAULTS}><tr><td style="padding: 0px 10px;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:{MAX_WIDTH};"><tr style="background-color: {background_color};"><![endif]-->
                <!--[if (mso)|(IE)]><td align="center" width="600" style="width: {MAX_WIDTH};padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]-->
                  {content}
                <!--[if (mso)|(IE)]></td><![endif]-->
              <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
            </div>
          </div>
        </div>
    """  # noqa
    return format_html(markup.format(
        content=content,
        background_color=background_color,
        **STATIC_CONTEXT,
    ))


def text_div(content):
    text_style = "{WORD_BREAK_STYLE}; {TEXT_COLOR_STYLE};".format(**STATIC_CONTEXT)
    markup = """
        <div style="{text_style} line-height: 140%; text-align: left;">
          {content}
        </div>
    """
    return markup.format(
        content=content,
        text_style=text_style,
        **STATIC_CONTEXT
    )


@register.filter
def email_title(content):
    def format_line(line):
        line_markup = """
            <p style="font-size: 14px; line-height: 140%; text-align: center;">
                <span style="font-size: 30px; line-height: 42px; {FONT_STYLE}">
                    {line}
                </span>
            </p>
        """
        return line_markup.format(line=line, **STATIC_CONTEXT)

    lines = map(format_line, textwrap.wrap(content, width=30))
    markup = """
        <td style="{FONT_STYLE};{WORD_BREAK_STYLE};padding:20px 15px 15px;" align="left">
            {title_markup}
        </td>
    """

    return email_table_container(markup.format(
        title_markup=text_div(''.join(lines)),
        **STATIC_CONTEXT,
    ))


@register.filter
def email_text_block(content):
    markup = """
        <td style="{FONT_STYLE};{WORD_BREAK_STYLE};padding:20px;" align="left">
            {content}
        </td>
    """
    return email_table_container(markup.format(
        content=text_div(content),
        **STATIC_CONTEXT,
    ))


@register.filter
def email_paragraph(content, variant='normal'):
    color = COLOR_BLACK_OLIVE
    size = '14px'
    if variant == 'inverse':
        color = COLOR_COCONUT_CREAM
        size = '12px'
    elif variant == 'lead':
        size = '16px'

    text_style = "color: {color}; font-size: {size};".format(color=color, size=size)
    markup = """
        <p style="{text_style} line-height: 140%; text-align: center;">
            <span style="{text_style}; line-height: 19.6px;">
                {content}
            </span>
        </p>
    """
    return email_table_container(markup.format(
        content=content,
        text_style=text_style,
        **STATIC_CONTEXT,
    ))


@register.filter
def email_text_highlight(content, variant='secondary'):
    color = COLOR_WILD_TIDE
    if variant == 'primary':
        color = COLOR_FUN_GREEN
    elif variant == 'danger':
        color = COLOR_DANGER
    markup = "<span style=\"color: {color}\">{content}</span>"
    return format_html(markup.format(
        content=content,
        color=color,
        **STATIC_CONTEXT,
    ))
