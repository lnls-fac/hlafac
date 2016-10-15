
paper: WEPOPRPO21poster.pdf
	okular WEPOPRPO21poster.pdf

clean:
	rm -rf *.aux *.log *.dvi *.pdf *.out

WEPOPRPO21poster.pdf: WEPOPRPO21poster.tex
	pdflatex WEPOPRPO21poster.tex
	pdflatex WEPOPRPO21poster.tex

WEPOPRPO21poster.dvi: WEPOPRPO21poster.tex W
	latex WEPOPRPO21poster.tex
	latex WEPOPRPO21poster.tex
	latex WEPOPRPO21poster.tex
