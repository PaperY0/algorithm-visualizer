def render_code(code_path: str, highlight_line: int) -> str:
    """渲染带行号高亮的Java代码"""
    with open(code_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    html_lines = []
    for i, line in enumerate(lines, 1):
        # HTML转义
        escaped = (line
                   .replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace(' ', '&nbsp;')
                   .replace('\n', ''))

        if i == highlight_line:
            html_lines.append(
                f'<div style="background-color: #FFF3CD; padding: 2px 8px;">'
                f'<span style="color: #666; margin-right: 12px;">{i:2d}</span>'
                f'<span style="color: #333; font-weight: bold;">{escaped}</span>'
                f'</div>'
            )
        else:
            html_lines.append(
                f'<div style="padding: 2px 8px;">'
                f'<span style="color: #999; margin-right: 12px;">{i:2d}</span>'
                f'<span style="color: #333;">{escaped}</span>'
                f'</div>'
            )

    return (
        '<div style="background-color: #1E1E1E; color: #D4D4D4; '
        'font-family: Consolas, monospace; font-size: 14px; '
        'padding: 12px; border-radius: 8px; overflow-x: auto;">'
        + '\n'.join(html_lines)
        + '</div>'
    )
