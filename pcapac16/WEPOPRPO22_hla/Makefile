
paper: WEPOPRPO22.pdf
	okular WEPOPRPO22.pdf

clean:
	rm -rf *.aux *.log *.dvi *.pdf

WEPOPRPO22.pdf: WEPOPRPO22.tex WEPOPRPO22f1.eps WEPOPRPO22f2.png WEPOPRPO22f3.png
	pdflatex WEPOPRPO22.tex
	pdflatex WEPOPRPO22.tex

WEPOPRPO22.dvi: WEPOPRPO22.tex WEPOPRPO22f1.eps WEPOPRPO22f2.png WEPOPRPO22f3.png
	latex WEPOPRPO22.tex
	latex WEPOPRPO22.tex
	latex WEPOPRPO22.tex
