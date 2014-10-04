BUNDLE                      = BD-TP1.tar.gz
BUNDLE_DIR                  = BD-TP1
BUNDLE_FILES_CLEAN          = src tex db diagramas Makefile README.md enunciado.pdf 
BUNDLE_FILES_AFTER_MAKE_ALL = informe.pdf

.PHONY: all clean bundle

all: informe.pdf db/facultad.db

informe.pdf:
	make -C tex all
	mv tex/informe.pdf .

db/facultad.db: db/facultad.sql
	echo -e ".read db/facultad.sql\n.save db/facultad.db" | sqlite3 -batch

bundle: clean
	mkdir $(BUNDLE_DIR)
	cp $(BUNDLE_FILES_CLEAN) $(BUNDLE_DIR) -r
	make all
	cp $(BUNDLE_FILES_AFTER_MAKE_ALL) $(BUNDLE_DIR) -r
	tar zcf $(BUNDLE) $(BUNDLE_DIR)
	rm -rf $(BUNDLE_DIR)

clean:
	make -C tex clean
	rm -rf informe.pdf src/*.pyc $(BUNDLE) $(BUNDLE_DIR)