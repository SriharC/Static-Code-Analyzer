class LineError(Exception):
    def __init__(self):
        self.issues = []

    def add_issue(self, band_num, issue_code, issue_message):
        self.issues.append(f'Line {band_num}: {issue_code} {issue_message}')

    def print_issues(self):
        if self.issues:
            for issue in self.issues:
                print(issue)


def check_length(band, band_num, error):
    if len(band) > 79:
        error.add_issue(band_num, 'S001', 'Too long')


def check_indent(band, band_num, error):
    if band.startswith(' ') and (len(band) - len(band.lstrip())) % 4 != 0:
        error.add_issue(band_num, 'S002', 'Indentation is not a multiple of four')


def check_semicolon(band, band_num, error):
    # Split the line into code and comment parts, if a comment exists.
    parts = band.split('#', 1)
    code = parts[0].rstrip()  # Remove trailing whitespace from code part.

    # Check if the code part ends with a semicolon.
    if code.endswith(';'):
        # Add condition here if deciding not to flag semicolons before comments as unnecessary.
        error.add_issue(band_num, 'S003', 'Unnecessary semicolon')


def check_inline_spacing(band, band_num, error):
    if '#' in band:
        # Split the line at the first occurrence of '#' to differentiate code from comment.
        parts = band.split('#', 1)
        code_part = parts[0]
        comment_part = '#' + parts[1] if len(parts) > 1 else ''

        # Check if the line contains actual code followed by a comment.
        if code_part.strip() and comment_part:
            # Count the trailing spaces of the code part.
            trailing_spaces = len(code_part) - len(code_part.rstrip(' '))

            # Flag if there are fewer than two spaces before the comment.
            if trailing_spaces < 2:
                error.add_issue(band_num, 'S004', 'At least two spaces required before inline comments')


def check_todo(band, band_num, error):
    if '#' in band and 'todo' in band.split('#')[1].lower():
        error.add_issue(band_num, 'S005', 'TODO found')


def check_blank_lines(band_num, error, blank_bands_count):
    if blank_bands_count > 2:
        error.add_issue(band_num, 'S006', 'More than two blank lines used before this line')


if __name__ == '__main__':

    error_tracker = LineError()

    try:
        filename = input().strip()
        with open(filename, 'r') as file:
            lines = file.readlines()

            blank_lines_count = 0
            for line_number, line in enumerate(lines, start=1):
                check_length(line, line_number, error_tracker)
                check_indent(line, line_number, error_tracker)
                check_semicolon(line, line_number, error_tracker)
                check_inline_spacing(line, line_number, error_tracker)
                check_todo(line, line_number, error_tracker)
                if line.strip() == '':
                    blank_lines_count += 1
                else:
                    if blank_lines_count > 2:
                        check_blank_lines(line_number, error_tracker, blank_lines_count)
                    blank_lines_count = 0

    except FileNotFoundError:
        print("File not found.")

    error_tracker.print_issues()
