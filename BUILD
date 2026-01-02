genrule(
    name = "doc_bin",
    srcs = glob(["app/**/*.py", "doc/**/*.yaml"]),
    outs = ["doc"],
    cmd = """
        /opt/homebrew/bin/nuitka \
            --onefile \
            --include-data-dir=doc=doc \
            --onefile-tempdir-spec=/tmp/nuitka-doc \
            --no-progressbar \
            --assume-yes-for-downloads \
            --output-dir=$$(dirname $(location doc)) \
            --output-filename=doc \
            $(location app/main.py)
    """,
    local = 1,
    visibility = ["//visibility:public"],
)






