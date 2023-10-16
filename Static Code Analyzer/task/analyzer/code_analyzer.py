class LineError(Exception):
    def __init__(self):
        self.issues = []

    def print_issues(self):
        if self.issues:
            for issue in self.issues:
                print(issue)


if __name__ == '__main__':

    error_tracker = LineError()

    try:
        with open(input().strip(), 'r') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if len(line) > 79:
                    message = f'Line {line_number}: S001 Too long'
                    error_tracker.issues.append(message)

    except FileNotFoundError:
        print("File not found.")

    error_tracker.print_issues()
