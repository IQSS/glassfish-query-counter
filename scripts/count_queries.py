import sys
from os.path import dirname, isdir, isfile, join, basename
from os import listdir
from collections import Counter
from settings_reader import get_settings_dict, PROJ_DIR, INPUT_DIR, OUTPUT_DIR,\
    SETTINGS_KEY_LOG_PATH, SETTINGS_KEY_DELIMITER

class QueryCounter:

    def __init__(self):
        self.load_settings()

    def load_settings(self):
        d = get_settings_dict()
        self.GLASSFISH_LOG_FILE_PATH = d.get(SETTINGS_KEY_LOG_PATH, None)
        self.DELIMITER = d.get(SETTINGS_KEY_DELIMITER, None)


    def count_queries(self, input_fname):
        assert input_fname is not None, "The input file name cannot be None"

        input_fname_fullpath = join(INPUT_DIR, input_fname)

        assert isfile(input_fname_fullpath), 'Unable to find the input file: %s' % self.input_fname_fullpath
        assert isdir(OUTPUT_DIR), 'Could not find output directory: %s' % OUTPUT_DIR

        # Read/Format file contents
        qlines = open(input_fname_fullpath, 'r').readlines()

        # Find lines beginning with SELECT
        qlines = [x.strip() for x in qlines if x.strip().startswith('SELECT')]

        counts = Counter(qlines)

        outlines = []
        line_num = 0
        for item, cnt in counts.most_common():
            line_num += 1
            outlines.append('%s,"%s"' % (cnt, item))
            print '(%d) COUNT: %d   QUERY(truncated): %s' % (line_num, cnt, item[:100])

        output_fname = basename(input_fname_fullpath).replace('.txt', '_counts.csv')
        full_output_fname = join(OUTPUT_DIR, output_fname)
        open(full_output_fname, 'w').write('\n'.join(outlines))
        print '\n\nQuery count file written: %s' % full_output_fname
    
        total = sum(counts.values())
        print '\nTotal number of queries: %d\n' % total

    def show_file_choices(self):
        option_list = []
        for cnt, input_fname in enumerate(self.get_input_file_list(), 1):
            option_list.append('(%d) %s' % (cnt, input_fname))

        if len(option_list) == 0:
            option_msg = '** Sorry, no text files found in: %s' % INPUT_DIR
        else:
            option_msg = '\n'.join(option_list)

        print """
------------------------------
Run query count
------------------------------

Please choose a file:

%s

------------------------------
    """ % (option_msg)


    def get_input_file_list(self):
        assert isdir(INPUT_DIR), 'Could not find input directory: %s' % INPUT_DIR

        l =  [fname for fname in listdir(INPUT_DIR) if fname.endswith('.txt')]
        l.sort()
        return l


    def count_queries_by_file_num(self, fnum):
        assert isinstance(fnum, int), 'fnum must be an "int""'

        file_list = self.get_input_file_list()
        for cnt, input_fname in enumerate(file_list, 1):
            if cnt==fnum:
                self.count_queries(input_fname)
                return

        assert False, "File choice '%d' was not found." % fnum
        

    def pull_last_queries(self, output_fname):
        """
        A bit inefficient but good enough
        """
        assert isfile(self.GLASSFISH_LOG_FILE_PATH), 'Could not find GLASSFISH_LOG_FILE_PATH file: %s\n**Check your settings.json file**' % self.GLASSFISH_LOG_FILE_PATH
        assert self.DELIMITER is not None, 'Could not find DELIMITER.\n**Check your settings.json file.**'

        print 'reading file: %s' % self.GLASSFISH_LOG_FILE_PATH

        outlines = []
        for line in reversed(open(self.GLASSFISH_LOG_FILE_PATH, 'r').readlines()):
            if line.find(self.DELIMITER) > -1:
                break
            outlines.append(line.strip())

        output_fname = '%s.txt' % output_fname
        full_output_fname = join(INPUT_DIR, output_fname)

        open(full_output_fname, 'w').write('\n'.join(outlines))

        print 'input file written: %s' % full_output_fname

        self.count_queries(output_fname)

    def show_instructions(self):
        dashes = 40 * '-'
        print """
%s
Read glassfish log.
 - Find all recent queries
 - Start with last log line
    that contains "%s"
%s

RUN IT:

> python count_queries.py [output file name without extension]

Example: >python count_queries.py dataset-3-files

Expected output files:
 (1) dataset-3-files.txt - Log excerpt containing 'SELECT' statements
 (2) dataset-3-files.csv - List of 'SELECT' statements ordered by count

""" % (dashes, self.DELIMITER, dashes)

if __name__ == '__main__':

    args = sys.argv

    qc = QueryCounter()
    if not len(args)==2:
        qc.show_instructions()
        #qc.show_file_choices()
    else:
        last_arg = args[1]
        if last_arg == 'rerun':
            qc.show_file_choices()
        elif last_arg.isdigit():
            qc.count_queries_by_file_num(int(last_arg))
        else:
            qc.pull_last_queries(last_arg)
