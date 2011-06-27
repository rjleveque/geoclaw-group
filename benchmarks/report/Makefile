
.PHONY: pdf clean 

pdf:
	pdflatex geoclaw-results

bib: geoclaw-results.tex
	pdflatex geoclaw-results
	bibtex geoclaw-results
	pdflatex geoclaw-results
	pdflatex geoclaw-results

clean:
	rm -f *.aux *.bbl *.log *.blg *.out
