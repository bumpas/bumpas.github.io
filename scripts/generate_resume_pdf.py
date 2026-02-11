from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from datetime import date
import re
import os
import argparse


def _strip_tags(s: str) -> str:
    # Very simple tag stripper for inline HTML wrappers in source content
    out = []
    inside = 0
    for ch in s:
        if ch == '<':
            inside += 1
        elif ch == '>':
            if inside:
                inside -= 1
        elif not inside:
            out.append(ch)
    return ''.join(out)


def _to_ascii(s: str) -> str:
    # Remove any non-ASCII characters that may render as boxes in PDF viewers
    try:
        return s.encode('ascii', 'ignore').decode('ascii')
    except Exception:
        return s


def _normalize_contact(s: str) -> str:
    # Replace unsupported icons/emoji and squares with simple ASCII separators
    replacements = {
        '📧': '',
        '📞': '',
        '■': '|',
        '•': '|',
        '‧': '|',
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    # Collapse multiple separators/spaces
    while '||' in s:
        s = s.replace('||', '|')
    # Normalize pipes with spacing
    s = ' | '.join(part.strip() for part in s.split('|'))
    # Force ASCII-only to avoid unknown glyph boxes
    s = _to_ascii(s)
    # Trim
    return ' '.join(s.split())

ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ROOT)
# Use the About page markdown as the source; start-line is configurable via CLI/env
md_path = "/Users/Bumpas/Documents/Freelance/andrewbumpas/2025/bumpas.github.io/src/content/about/-index.md"
# Name the output PDF with the current date in YYYYMMDD format
today_str = date.today().strftime('%Y%m%d')
out_pdf = os.path.join(ROOT, f"Andrew-Bumpas-Resume-{today_str}.pdf")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Header', fontSize=18, leading=22, spaceAfter=2, alignment=1, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='Subheader', fontSize=10, leading=12, spaceAfter=2, alignment=1, textColor='#666666', fontName='Helvetica'))
styles.add(ParagraphStyle(name='H2', fontSize=12, leading=14, spaceBefore=16, spaceAfter=8, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='H3', fontSize=14, leading=13, spaceBefore=10, spaceAfter=6, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='Role', fontSize=10, leading=12, spaceBefore=8, spaceAfter=4, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='Body', fontSize=10, leading=13))
styles.add(ParagraphStyle(name='BulletText', fontSize=10, leading=13, leftIndent=12))


def parse_md(md_text: str):
    lines = [l.rstrip() for l in md_text.splitlines()]
    content = []
    # Detect and start parsing from the '## Resume' section explicitly
    i = 0
    header = None
    contact = None
    role_line = None
    # Skip leading blank lines
    while i < len(lines) and not lines[i].strip():
        i += 1
    # Skip YAML frontmatter block if present
    if i < len(lines) and lines[i].strip() == '---':
        i += 1
        while i < len(lines) and lines[i].strip() != '---':
            i += 1
        if i < len(lines) and lines[i].strip() == '---':
            i += 1
    # Find the Resume section heading
    resume_idx = None
    for idx, line in enumerate(lines):
        if line.strip() == '## Resume':
            resume_idx = idx
            break
    if resume_idx is not None:
        i = resume_idx + 1
        # Skip any horizontal rules or blank lines immediately after
        while i < len(lines) and (not lines[i].strip() or lines[i].strip() in ('---', '***', '___')):
            i += 1
        # Expect role line as HTML <h3> and contact next
        if i < len(lines) and lines[i].lstrip().startswith('<h3'):
            role_line = _strip_tags(lines[i]).strip()
            i += 1
            # Skip separators/empty
            while i < len(lines) and (not lines[i].strip() or lines[i].strip() in ('---', '***', '___')):
                i += 1
            if i < len(lines):
                contact = _strip_tags(lines[i].strip())
                i += 1
        # Skip separators/empty before actual content sections
        while i < len(lines) and (not lines[i].strip() or lines[i].strip() in ('---', '***', '___')):
            i += 1
    else:
        # Fallback: attempt previous top-of-file detection
        if i < len(lines) and lines[i].startswith('# '):
            header = _strip_tags(lines[i].replace('# ', '').strip())
            i += 1
            while i < len(lines) and (not lines[i].strip() or lines[i].strip() in ('---', '***', '___')):
                i += 1
            if i < len(lines):
                contact = _strip_tags(lines[i].strip())
                i += 1
        elif i < len(lines) and lines[i].lstrip().startswith('<h3'):
            role_line = _strip_tags(lines[i]).strip()
            i += 1
            while i < len(lines) and (not lines[i].strip() or lines[i].strip() in ('---', '***', '___')):
                i += 1
            if i < len(lines) and not lines[i].startswith('## '):
                contact = _strip_tags(lines[i].strip())
                i += 1
    if header:
        content.append(('header', header))
    if role_line:
        content.append(('subheader', role_line))
    if contact:
        content.append(('subheader', _normalize_contact(contact)))

    buffer = []
    section = None

    def flush_paragraphs(style='Body'):
        nonlocal buffer
        text = '\n'.join(buffer).strip()
        if text:
            content.append(('paragraph', text, style, section))
        buffer = []

    while i < len(lines):
        line = lines[i]
        # Skip markdown horizontal rules from output
        if line.strip() in ('---', '***', '___'):
            flush_paragraphs()
            i += 1
            continue
        if line.startswith('## '):
            flush_paragraphs()
            section_name = line[3:].strip()
            # Skip the top-level 'Resume' section heading from PDF output
            if section_name.lower() == 'resume':
                section = None
            else:
                section = section_name
                content.append(('h2', section))
        elif line.lstrip().startswith('<h4'):
            # Company header as HTML h4 followed by a location/date line
            flush_paragraphs()
            company = _strip_tags(line).strip()
            # Look ahead to capture location and dates
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or lines[j].strip() in ('---', '***', '___')):
                j += 1
            location = ''
            dates = ''
            if j < len(lines):
                locline = _strip_tags(lines[j]).strip()
                if locline.endswith(')') and '(' in locline:
                    left, right = locline.rsplit('(', 1)
                    location = left.strip()
                    dates = right[:-1].strip()
                else:
                    location = locline
                # consume the looked-ahead line
                i = j
            # Emit a company_header entry and set current section to the company to group following items
            content.append(('company_header', company, location, dates))
            section = company
        elif line.startswith('### '):
            # Either a regular H3 section heading or a company line
            flush_paragraphs()
            raw = line[4:].strip()
            is_company_like = False
            left = raw
            right = ''
            # Heuristic: treat as company row only if it looks like "Company — Location (Dates)" or has separators
            if raw.endswith(')') and '(' in raw:
                left_tmp, right_tmp = raw.rsplit('(', 1)
                # If there is a dash separator and parentheses, likely a company line
                if (' — ' in left_tmp) or (' - ' in left_tmp):
                    is_company_like = True
                    left, right = left_tmp.strip(), right_tmp[:-1].strip()
            elif (' — ' in raw) or (' - ' in raw):
                # May still be a company/location without dates
                is_company_like = True
            if is_company_like:
                company = left
                location = ''
                if ' — ' in left:
                    company, location = left.split(' — ', 1)
                elif ' - ' in left:
                    company, location = left.split(' - ', 1)
                company = company.strip()
                location = location.strip()
                content.append(('company_header', company, location, right))
                section = company
            else:
                # Regular H3 heading (e.g., Areas of Expertise in some sources)
                content.append(('h3', raw))
        elif line.startswith('**') and '**' in line[2:]:
            flush_paragraphs()
            # Remove bold markers from job title lines even when followed by dates
            content.append(('role', line.replace('**', '').strip()))
        elif re.match(r"^\s*(?:[-*+]\s+|\d+\.\s+)", line):
            # Collect consecutive markdown list items (hyphen/asterisk/plus/numbered) and render as bullets
            bullets = []
            while i < len(lines) and re.match(r"^\s*(?:[-*+]\s+|\d+\.\s+)", lines[i]):
                li = lines[i].lstrip()
                # Strip the list marker
                if li[0] in ('-', '*', '+'):
                    bullets.append(li[2:].strip())
                else:
                    # Numbered like '1. Item' -> treat as bullet
                    bullets.append(re.sub(r"^\d+\.\s+", "", li).strip())
                i += 1
            i -= 1
            for b in bullets:
                content.append(('paragraph', f"• {b}", 'BulletText', section))
        elif line.startswith('# '):
            pass
        elif not line.strip():
            flush_paragraphs()
        else:
            buffer.append(line)
        i += 1
    flush_paragraphs()
    return content


def build_pdf(content):
    doc = SimpleDocTemplate(out_pdf, pagesize=LETTER, leftMargin=0.7*inch, rightMargin=0.7*inch, topMargin=0.7*inch, bottomMargin=0.7*inch)
    story = []

    # Render top block (header + first two subheaders) as one grouped element with a bottom border
    i = 0
    if i < len(content) and isinstance(content[i], tuple) and content[i][0] == 'header':
        header_text = content[i][1]
        i += 1
        subheaders = []
        while i < len(content) and isinstance(content[i], tuple) and content[i][0] == 'subheader' and len(subheaders) < 2:
            subheaders.append(content[i][1])
            i += 1
        rows = [[Paragraph(header_text, styles['Header'])]]
        for sh in subheaders:
            rows.append([Paragraph(sh, styles['Subheader'])])
        tbl = Table(rows, colWidths=[doc.width])
        tbl.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            # Add extra space after the last subheader line before the divider
            ('BOTTOMPADDING', (0, len(rows)-1), (-1, len(rows)-1), 6),
            ('LINEBELOW', (0, len(rows)-1), (0, len(rows)-1), 0.7, colors.HexColor('#CCCCCC')),
        ]))
    story.append(tbl)
    story.append(Spacer(1, 4))
    # Continue rendering remaining items
    company_header_count = 0
    while i < len(content):
        item = content[i]
        kind = item[0]
        if kind == 'h2':
            story.append(Paragraph(item[1], styles['H2']))
        elif kind == 'h3':
            story.append(Paragraph(item[1], styles['H3']))
        elif kind == 'company_header':
            # Add a bit of top spacing starting from the second company header
            company_header_count += 1
            if company_header_count >= 2:
                story.append(Spacer(1, 10))
            # Render as two columns: left = company + location (location smaller, not bold), right = dates right-aligned
            company, location, dates = item[1], item[2], item[3]
            left_html = f"<font name='Helvetica-Bold'>{company}</font>"
            if location:
                # Location smaller and unbold, slightly gray
                left_html += f" — <font name='Helvetica' size='10' color='#666666'>{location}</font>"
            # Build table
            tbl = Table(
                [[Paragraph(left_html, styles['H2']), Paragraph(dates, styles['Subheader'])]],
                colWidths=[doc.width * 0.68, doc.width * 0.32]
            )
            tbl.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('ALIGN', (1,0), (1,0), 'RIGHT'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                # Slight nudge to the right so company headers don't appear too far left
                ('LEFTPADDING', (0,0), (0,0), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(tbl)
        elif kind == 'role':
            # If the role line contains a pipe separator with dates, style the dates like Subheader without changing alignment
            role_text = item[1]
            if '|' in role_text:
                title, dates = role_text.split('|', 1)
                title = title.strip()
                dates = dates.strip()
                html = f"<font name='Helvetica-Bold'>{title}</font> <font name='Helvetica' color='#666666'>{'| ' + dates}</font>"
                story.append(Paragraph(html, styles['Role']))
            else:
                story.append(Paragraph(role_text, styles['Role']))
        elif kind == 'paragraph':
            # item = ('paragraph', text, styleName, section)
            style_name = item[2] if isinstance(item, tuple) and len(item) > 2 else 'Body'
            section = item[3] if isinstance(item, tuple) and len(item) > 3 else None
            text = item[1]

            # Minimal Markdown to ReportLab markup: bold **text** -> <b>text</b>
            def _md_to_para_markup(s: str) -> str:
                return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)

            if style_name == 'BulletText' and section and section.lower() == 'technical skills' and text.startswith('• '):
                bullet_body_raw = text[2:].strip()
                # If colon exists, try to bold the label before colon unless it's already bolded via MD
                if ':' in bullet_body_raw:
                    label_raw, rest_raw = bullet_body_raw.split(':', 1)
                    label_md = _md_to_para_markup(label_raw.strip())
                    rest_md = _md_to_para_markup(rest_raw.strip())
                    if '<b>' in label_md:
                        # Respect existing MD bold for the label
                        text = f"• {label_md}: {rest_md}"
                    else:
                        text = f"• <font name='Helvetica-Bold'>{label_raw.strip()}:</font> {rest_md}"
                else:
                    # No colon; just convert MD bold if present
                    text = f"• {_md_to_para_markup(bullet_body_raw)}"
            else:
                text = _md_to_para_markup(text)

            story.append(Paragraph(text, styles[style_name]))
        story.append(Spacer(1, 2))
        i += 1
    doc.build(story)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate ATS resume PDF')
    parser.add_argument('--start-line', type=int, default=int(os.environ.get('ATS_START_LINE', '14')),
                        help='1-based line number in the source markdown to start parsing from (default from ATS_START_LINE env or 14).')
    parser.add_argument('--source', type=str, default=os.environ.get('ATS_SOURCE_MD', md_path),
                        help='Path to the source markdown file (default from ATS_SOURCE_MD env or the About page).')
    parser.add_argument('--header', type=str, default=os.environ.get('ATS_HEADER', ''),
                        help='Optional header text (e.g., name) to render above the contact line. If provided, overrides any header in source.')
    args = parser.parse_args()

    source_path = args.source
    start_line = args.start_line
    header_override = args.header.strip()

    with open(source_path, 'r', encoding='utf-8') as f:
        md = f.read()
    content = parse_md(md)
    # If a header override is provided, ensure it is used as the first header
    if header_override:
        # Remove any existing 'header' entries
        content = [item for item in content if not (isinstance(item, tuple) and item[0] == 'header')]
        content.insert(0, ('header', header_override))
    build_pdf(content)
    print('Wrote', out_pdf)
