
The file geoclaw-results.tex is the main latex driver.

It contains lines
\include{bp1}
\include{bp2}
etc.

that reads in the files bp1.tex, bp2.tex, etc.

If there's a line of the form
\includeonly{bp7}

Then only the file(s) listed are read in, useful when working one file.

------------

To create the pdf file:
   make pdf
The first time, or after modifying the citations or references.bib file, you
will need to instead do:
   make bib


Or you can just type
   pdflatex geoclaw-results

Either way, the result is in geoclaw-results.pdf


Directories such as bp7 contain figures for the indicated benchmark problem.
