from app.services.input_sanitizer_service import InputSanitizerService


def test_sanitize_group_name_shouldRemoveAllSpecialCharsAndEmojiAndReplaceSpacesWithDashes():
    group_name = "Hello! 😊 @world$ & this is a #test string% with special characters and emojis: 😀"
    expected = "hello-world-this-is-a-test-string-with-special-characters-and-emojis"

    actual = InputSanitizerService.sanitize_group_name(group_name)

    assert actual == expected
