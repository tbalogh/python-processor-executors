import os, codecs


def read_lines(path):
    with codecs.open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    return lines


def append(content, path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with codecs.open(path, "a+", encoding='utf8') as f:
        f.write(content)


class Logger:
    def __init__(self, path):
        self.path = path
        self.sep = ';'
        self.markers = {
            'info': 'INFO',
            'error': 'ERROR'
        }

    def path(self):
        return self.path

    def clean(self):
        if os.path.isfile(self.path):
            os.remove(self.path)

    def info(self, tag, message):
        content = self.info_line(tag, message)
        append(content, self.path)

    def error(self, tag, message):
        content = self.error_line(tag, message)
        append(content, self.path)

    def info_line(self, tag, message):
        return self.markers['info'] + self.sep + tag + self.sep + message + os.linesep

    def error_line(self, tag, message):
        return self.markers['error'] + self.sep + tag + self.sep + message + os.linesep

    def structure_lines(self, lines):
        return [line.strip().split(self.sep) for line in lines]

    def current_content(self):
        lines = read_lines(self.path)
        return self.structure_lines(lines)

    def current_info_by_tag(self, tag):
        lines = read_lines(self.path)
        structured_lines = self.structure_lines(lines)
        info_lines = self.filter_infos(structured_lines)
        return self.filter_tag(info_lines, tag)

    def info_by_tag(self, structured_lines, tag):
        info_lines = self.filter_infos(structured_lines)
        return self.filter_tag(info_lines, tag)

    def filter_infos(self, structured_lines):
        return [line for line in structured_lines if line[0] == self.markers['info']]

    def filter_tag(self, structured_lines, tag):
        return [line for line in structured_lines if line[1] == tag]


class ProcessedFileLogger:
    def __init__(self, path):
        self.log = Logger(path)

    def processed(self, path):
        self.log.info("PROCESSED", path)

    def failed(self, path):
        self.log.error("FAILED", path)

    def get_processed_files(self):
        log_lines = self.log.current_info_by_tag("PROCESSED")
        processed_files = [log_line[2] for log_line in log_lines]
        return processed_files


def get_all_processed_files(log_files):
    all_processed_files = []
    for log_file in log_files:
        logger = ProcessedFileLogger(log_file)
        all_processed_files.extend(logger.get_processed_files())
    return all_processed_files


def calculate_unporcessed_files(all_files, log_files):
    all_files = set(os.path.abspath(model_path) for model_path in all_files)
    processed_files = set(get_all_processed_files(log_files))
    unprocessed_files = all_files - processed_files
    return list(unprocessed_files)
