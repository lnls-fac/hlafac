
paper: WEPOPRPO22poster.pdf
	okular WEPOPRPO22poster.pdf

clean:
	rm -rf *.aux *.log *.dvi *.pdf *.out

WEPOPRPO21poster.pdf: WEPOPRPO22poster.tex
	pdflatex WEPOPRPO22poster.tex
	pdflatex WEPOPRPO22poster.tex

WEPOPRPO21poster.dvi: WEPOPRPO22poster.tex W
	latex WEPOPRPO22poster.tex
	latex WEPOPRPO22poster.tex
	latex WEPOPRPO22poster.tex
