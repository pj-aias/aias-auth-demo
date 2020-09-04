MAIN_PROGRAM := main.py
CORE_LIB := aias-auth-sdk/ffi/

run: build
	python $(MAIN_PROGRAM)

build:
	cd $(CORE_LIB) && cargo build --release

verify:
	curl 'localhost:5000/verify' \
		-i \
		-X POST \
		-H "Content-Type: application/json" \
		-d "$$(cat parameters/data.txt)"

clean:
	rm -rf $(CORE_LIB)/target/
