SOURCEDOCUMENT=monografia
PDFVIEWER=xpdf -z page
CAPITULOS=$(wildcard *.tex)

#######################################

all: $(SOURCEDOCUMENT).pdf

view: $(SOURCEDOCUMENT).pdf
	$(PDFVIEWER) $(SOURCEDOCUMENT).pdf &

$(SOURCEDOCUMENT).pdf: $(SOURCEDOCUMENT).tex $(CAPITULOS) $(SOURCEDOCUMENT).bib
	pdflatex $< && \
	makeindex -s tabela-simbolos.ist -o $(SOURCEDOCUMENT).sigla $(SOURCEDOCUMENT).siglax && \
	bibtex $(SOURCEDOCUMENT) && \
	pdflatex $< && \
	pdflatex $< || \
	$(RM) $@

clean:
	$(RM) *.aux *.bbl *.blg *.lof *.lot *.log $(SOURCEDOCUMENT).pdf *~ \
	*.toc *.ilg *.sigla *.siglax *.symbols *.symbolsx
