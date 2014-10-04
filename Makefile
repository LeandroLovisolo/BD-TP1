BUNDLE       = BD-TP1.tar.gz
BUNDLE_DIR   = BD-TP1
BUNDLE_FILES = src tex Makefile README.md enunciado.pdf informe.pdf

.PHONY: all clean bundle

all: informe.pdf db/facultad.db

informe.pdf:
	make -C tex all
	mv tex/informe.pdf .

db/facultad.db: db/facultad.sql
	echo -e ".read db/facultad.sql\n.save db/facultad.db" | sqlite3 -batch

bundle: clean all
	mkdir $(BUNDLE_DIR)
	cp $(BUNDLE_FILES) $(BUNDLE_DIR) -r
	tar zcf $(BUNDLE) $(BUNDLE_DIR)
	rm -rf $(BUNDLE_DIR)

clean:
	make -C tex clean
	rm -rf informe.pdf src/*.pyc $(BUNDLE) $(BUNDLE_DIR)