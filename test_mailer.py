import string
from mailer import generate_temporary_password, build_email_message

def test_password_length():
    pwd = generate_temporary_password(15)
    assert len(pwd) == 15

def test_password_character_diversity():
    pwd = generate_temporary_password(25)
    # Verify characters are pulled from valid pool
    allowed = set(string.ascii_letters + string.digits + "!@#$%^&*()-_=+")
    assert all(char in allowed for char in pwd)

def test_message_structure():
    msg = build_email_message("sender@domain.com", "user@domain.com", "SecretPass123!")
    assert msg["To"] == "user@domain.com"
    assert msg["From"] == "sender@domain.com"
    assert "SecretPass123!" in msg.get_content()
