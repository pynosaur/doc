genrule(
    name = "doc_bin",
    srcs = glob(["app/**/*.py", "doc/**/*.yaml"]) + [".program"],
    outs = ["doc"],
    cmd = """
        _VER=$$(grep '^version:' $(location .program) | cut -d' ' -f2)
        /opt/homebrew/bin/nuitka \
            --onefile \
            --include-data-dir=doc=doc \
            --onefile-tempdir-spec=/tmp/nuitka-doc-$$_VER \
            --no-progressbar \
            --assume-yes-for-downloads \
            --output-dir=$$(dirname $(location doc)) \
            --output-filename=doc \
            $(location app/main.py)
    """,
    local = 1,
    visibility = ["//visibility:public"],
)






