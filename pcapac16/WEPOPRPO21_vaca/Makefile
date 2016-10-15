
paper: WEPOPRPO21.pdf
	okular WEPOPRPO21.pdf

clean:
	rm -rf *.aux *.log *.dvi *.pdf

WEPOPRPO21.pdf: WEPOPRPO21.tex WEPOPRPO21f1.png
	pdflatex WEPOPRPO21.tex
	pdflatex WEPOPRPO21.tex

WEPOPRPO21.dvi: WEPOPRPO21.tex WEPOPRPO21f1.eps
	latex WEPOPRPO21.tex
	latex WEPOPRPO21.tex
	latex WEPOPRPO21.tex
