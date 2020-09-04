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
		-H "Vary: Cookie" \
		-H "Cookie: session=eyJ0b2tlbiI6MTB9.X1H6_g.ckttpx9rtCj7FJFBWsY28ACBuxs; HttpOnly; Path=/" \
		-d "$$(cat parameters/data.txt)"

verify_json:
	curl 'localhost:5000/verify' \
		-i \
		-X POST \
		-H "Content-Type: application/json" \
		-H "Vary: Cookie" \
		-H "Cookie: session=eyJ0b2tlbiI6MTB9.X1H6_g.ckttpx9rtCj7FJFBWsY28ACBuxs; HttpOnly; Path=/" \
		-d "$$(cat parameters/json_data.txt)"

clean:
	rm -rf $(CORE_LIB)/target/
