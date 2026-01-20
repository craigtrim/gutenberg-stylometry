"""Tests for the tokenizer module."""

from gutenburg_stylometry.tokenizer import VictorianTokenizer, tokenize


class TestVictorianTokenizer:
    """Tests for VictorianTokenizer."""

    def test_basic_tokenization(self):
        """Test basic word tokenization."""
        text = "Hello world"
        tokens = tokenize(text)
        assert tokens == ["hello", "world"]

    def test_contractions_preserved(self):
        """Test that contractions are kept intact."""
        text = "I don't know what you're saying"
        tokens = tokenize(text)
        assert "don't" in tokens
        assert "you're" in tokens

    def test_hyphenated_compounds(self):
        """Test that hyphenated words stay together."""
        text = "The looking-glass was half-broken"
        tokens = tokenize(text)
        assert "looking-glass" in tokens
        assert "half-broken" in tokens

    def test_possessives(self):
        """Test possessive forms."""
        text = "Alice's adventure"
        tokens = tokenize(text)
        assert "alice's" in tokens

    def test_lowercase_option(self):
        """Test lowercase parameter."""
        text = "Hello World"
        tokens_lower = tokenize(text, lowercase=True)
        tokens_upper = tokenize(text, lowercase=False)
        assert tokens_lower == ["hello", "world"]
        assert tokens_upper == ["Hello", "World"]

    def test_smart_quotes_normalized(self):
        """Test that smart quotes are converted to ASCII."""
        text = "\u201cHello\u201d he said"  # "Hello" with smart quotes
        tokens = tokenize(text)
        assert "hello" in tokens
        assert "said" in tokens

    def test_em_dash_handling(self):
        """Test em-dash doesn't merge words."""
        text = "word\u2014another"  # word—another
        tokens = tokenize(text)
        assert "word" in tokens
        assert "another" in tokens

    def test_min_length_filter(self):
        """Test minimum length filtering."""
        tokenizer = VictorianTokenizer(min_length=3)
        tokens = tokenizer.tokenize("I am a big dog")
        assert "i" not in tokens
        assert "am" not in tokens
        assert "a" not in tokens
        assert "big" in tokens
        assert "dog" in tokens
