FROM ocaml/opam:ubuntu-24.04-ocaml-4.13 AS build

USER opam
WORKDIR /home/opam/marina

COPY --chown=opam:opam . .

RUN opam install -y ocamlfind ounit2 \
    && eval $(opam env) \
    && make

FROM ubuntu:24.04

WORKDIR /app
COPY --from=build /home/opam/marina/marina .

ENTRYPOINT ["./marina"]