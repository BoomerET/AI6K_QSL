Milestone 7.1

1. Copy files into your repo.
2. Put your API key into config/config.yaml.
3. Add requests>=2.32 to dependencies.
4. Add script:

qsl-test = "qslstudio.test_connection:main"

Run:

python -m pip install -e .
qsl-test
