from app.services.chunking import chunk_file


def test_python_chunker_extracts_symbols() -> None:
    content = """
def outer():
    return 1

class Example:
    def method(self):
        return 2
""".strip()
    chunks = chunk_file(content, "src/example.py", "python")
    symbol_names = {chunk.metadata["symbol_name"] for chunk in chunks}
    assert "outer" in symbol_names
    assert "Example" in symbol_names