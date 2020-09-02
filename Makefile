MAIN_PROGRAM := main.py
CORE_LIB := aias-core/ffi/

run: build
	python $(MAIN_PROGRAM)

build:
	cd $(CORE_LIB) && cargo build --release

clean:
	rm -rf $(CORE_LIB)/target/