#!/usr/bin/env python

import csv
import numpy as np
import argparse

def main():
    
    parser = argparse.ArgumentParser(description='Create a LaTeX table for a SOP from a tab-separated table file')
    parser.add_argument("tablefile", type=str, help='The input table file')
    parser.add_argument("-c", type=str, default="1.5in", help='Width of Command Description field')
    parser.add_argument("-d", type=str, default="3.0in", help='Width of Description field')
    parser.add_argument("-p", type=str, default="2.1in", help='Width of Title field')
    parser.add_argument("-t", type=str, default="1.7in", help='Width of Telemetry EGSE field')
    parser.add_argument("-l", type=str, default="27", help='Maximum number of lines per page, '
                                                           'can either be a single value or '
                                                           'a comma-separated list')
    parser.add_argument("-f", type=str, default="",
                        help='File to write to. Default is to change the suffix of the input file.')
    
    args = parser.parse_args()
    
    cwidth = 'p{%s}' % args.c
    dwidth = 'p{%s}' % args.d
    pwidth = 'p{%s}' % args.p
    twidth = 'p{%s}' % args.t
    pline = 18 # height of line in points
    lmax = np.array(args.l.split(',')).astype("int")
    
    table_footer = ["\\hline\n", "\\end{tabular}\n", "\\end{table}\n", "\\end{landscape}\n"]
    
    def make_latex_table(page, pageno, rows, align):
        outlines = ["\\newpage\n", "\\begin{landscape}\n",
                    "\\setcounter{table}{0}\n", "\\begin{table}[t]\n",
                    "\\caption[ ]{\\bf\\footnotesize \\tablecaptiontext (Page %d)}\n" % pageno,
                    "\\begin{tabular}[t]{%s}\n" % align, "\\hline\n"]
        if page == "left":
            rows[1][1] = "(Revision %s)" % rows[1][1]
        outlines.append(" & ".join(['\\hc{\\bf\\footnotesize %s}' % elem for elem in rows[0]]) + " \\\\\n")
        outlines.append(" & ".join(['\\hc{\\bf\\footnotesize %s}' % elem for elem in rows[1]]) + " \\\\\n")
        outlines.append("\\hline\n\\hline\n")
        for i in range(2, len(rows)):
            if page == "left":
                rows[i][2] = '\\hc{%s}' % rows[i][2]
                if "parbox" not in rows[i][1]:
                    rows[i][1] = "{\\raggedright %s}" % rows[i][1]
            else:
                if "cmdResult" in rows[i][2]:
                    rows[i][2] = '{\\raggedright %s}' % rows[i][2]
                if "terminationCode" in rows[i][5]:
                    rows[i][5] = '{\\raggedright %s}' % rows[i][5]
            if len(rows[i][0].strip(" ")) > 0 and "." not in rows[i][0]:
                rows[i][1] = "\\bf{%s}" % rows[i][1]
            outlines.append(" & ".join(rows[i])+" \\\\\n")
            if i+1 != len(rows):
                if len(rows[i+1][0].strip(" ")) > 0:
                    outlines.append("\\hline\n")
                    if "." not in rows[i+1][0]:
                        outlines.append("\\hline\n")
        return outlines
    
    # Read in the table
    fn = args.tablefile
    f = open(fn, 'r')
    t = csv.reader(f, dialect="excel-tab")
    rows = [row for row in t]
    f.close()
    
    # Pad each row with empty columns so they
    # all match
    table_width = len(rows[0])
    for row in rows:
        if len(row) < table_width:
            row += ['']*(table_width-len(row))
    
    # Determine the total time
    total_time = 0
    for row in rows[2:]:
        if row[2].strip(' ') != '':
            total_time += int(row[2])
    num_rows = len(rows)
    
    nleft = 8
    nright = 10
    
    ttime_left = ' & '.join(['','Total time:',str(total_time)]+['']*(nleft-3))+" \\\\\n"
    ttime_right = ' & '.join(['']*(nright+1))+" \\\\\n"
    
    rows = np.array(rows).astype("|U80")
    
    # Set columns and alignment for left and right
    cols_left = [0,1,2,3,4,7,8,9]
    cols_right = [0,10,11,12,13,14,15,16,17,18,19]
    align_left = '|l|%s|p{0.2in}|%s|l|l|l|l|' % (pwidth, cwidth)
    align_right = '|c|c|%s|l|c|%s|l|c|c|c|c|' % (twidth, dwidth)
    
    # Select columns
    left_rows = rows[:, cols_left]
    right_rows = rows[:, cols_right]
    
    # Now figure out which rows need to take up two rows
    # and how we need to split the table up into pages
    warnpage = False
    pages = []
    nline = 0
    last_nline = 0 
    last_i = 0
    page_i = 0
    for i in range(num_rows):
        lbl = not np.all(np.char.count(left_rows[i], '\\\\') == 0)
        lbr = not np.all(np.char.count(right_rows[i], '\\\\') == 0)
        if lbl and not lbr:
            if right_rows[i][1].strip(" ") == '':
                right_rows[i][1] = "\\parbox[t][%dpt]{0.2in}{}" % pline
            else:
                right_rows[i][1] = "{%s \\\\}" % right_rows[i][1]
        elif lbr and not lbl:
            if left_rows[i][1].strip(" ") == '':
                left_rows[i][1] = "\\parbox[t][%dpt]{0.2in}{}" % pline
            else:
                left_rows[i][1] += " \\\\"
        nline += 1 + int(lbl or lbr)
        npages = len(pages)
        if lmax.size == 1:
            maxlines = lmax[0]
        else:
            if page_i >= len(lmax):
                if warnpage:
                    print("WARNING: Number of pages is now greater "
                          "than that specified in the '-l' argument. "
                          "Using the last entry of '-l' for page %d." % (page_i+1))
                    warnpage = False
                maxlines = lmax[-1]
            else:
                maxlines = lmax[page_i]
        if nline - last_nline >= maxlines-int(npages > 0)*2:
            warnpage = True
            page_i += 1
            pages.append([last_i, i])
            last_i = i
            last_nline = nline
    pages.append([last_i, num_rows])
    npages = len(pages)
    
    # Beginning of the file we're going to write
    outlines = ["\\newcommand*\\pgf{\\color{red}}\n",
                "\\newcommand*\\jaz{\\color{blue}}\n",
                "\\newcommand{\\hc}[1]{\\multicolumn{1}{|c|}{#1}}\n",
                "\\newcommand{\\mc}[2]{\\multicolumn{#1}{|l|}{#2}}\n"]
    
    for i, page in enumerate(pages):
        row_idxs = list(range(page[0], page[1]))
        if i > 0:
            row_idxs = [0, 1] + row_idxs
        nr = len(row_idxs)
        outlines += make_latex_table("left", i+1, left_rows[row_idxs], align_left)
        if i+1 == npages:
            outlines += ["\\hline\n",ttime_left]
        outlines += table_footer
        outlines += make_latex_table("right", i+1, right_rows[row_idxs], align_right)
        if i+1 == npages:
            outlines += ["\\hline\n",ttime_right]
        outlines += table_footer
    
    # Write the LaTeX table
    if args.f == "":
        outfn = fn[:-4]+".tab"
    else:
        outfn = args.f
    with open(outfn, 'w') as fd:
        fd.writelines(outlines)
        fd.close()


if __name__ == "__main__":
    main()